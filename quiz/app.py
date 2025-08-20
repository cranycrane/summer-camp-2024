import sqlite3, json, os
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import flash
from datetime import datetime, timedelta
import glob

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASE_DIR, "quiz.db")
GAMIFY_DIR = os.path.join(BASE_DIR, "gamify")

# --- konfig ---
def load_levels():
    path = os.path.join(GAMIFY_DIR, "levels.json")
    try:
        data = json.load(open(path, encoding="utf-8"))
        levels = sorted(data["levels"], key=lambda x: x["min_points"])
        return levels
    except Exception:
        # fallback
        return [
            {"code":"L1","min_points":0,"title":"Nováček","icon":"🌱"},
            {"code":"L2","min_points":100,"title":"Průzkumník","icon":"🧭"},
            {"code":"L3","min_points":250,"title":"Expert","icon":"🧠"},
            {"code":"L4","min_points":500,"title":"Mistr","icon":"🏆"},
        ]

def load_badges():
    path = os.path.join(GAMIFY_DIR, "badges.json")
    try:
        return json.load(open(path, encoding="utf-8"))["badges"]
    except Exception:
        return []
    


LEVELS = load_levels()
BADGES = load_badges()
BADGES_BY_CODE = {b["code"]: b for b in BADGES}

# --- body / odznaky ---
def get_user_badges(db, user_id):
    rows = db.execute(
        "SELECT badge_code FROM user_badges WHERE user_id=? ORDER BY created_at ASC",
        (user_id,)
    ).fetchall()
    result = []
    for r in rows:
        b = BADGES_BY_CODE.get(r["badge_code"])
        if b:
            # vezmeme jen pole potřebná pro UI
            result.append({"code": b["code"], "name": b["name"], "desc": b["desc"], "icon": b["icon"]})
        else:
            # fallback, kdyby byl v DB starý/unknown kód
            result.append({"code": r["badge_code"], "name": r["badge_code"], "desc": "", "icon": "🏅"})
    return result


def ensure_user_points(db, user_id):
    db.execute("INSERT OR IGNORE INTO user_points (user_id, total_points) VALUES (?,0)", (user_id,))
    db.commit()

def get_total_points(db, user_id):
    row = db.execute("SELECT total_points FROM user_points WHERE user_id=?", (user_id,)).fetchone()
    return row["total_points"] if row else 0

def add_points(db, user_id, delta, reason, meta=None):
    ensure_user_points(db, user_id)
    db.execute("INSERT INTO points_ledger (user_id, delta, reason, meta_json) VALUES (?,?,?,?)",
               (user_id, delta, reason, json.dumps(meta or {}, ensure_ascii=False)))
    db.execute("UPDATE user_points SET total_points = total_points + ? WHERE user_id=?", (delta, user_id))
    db.commit()

def get_level_for_points(total_points):
    current = LEVELS[0]
    next_level = None
    for lvl in LEVELS:
        if total_points >= lvl["min_points"]:
            current = lvl
        else:
            next_level = lvl
            break
    return current, next_level

def grant_badge_once(db, user_id, badge_code):
    try:
        db.execute("INSERT INTO user_badges (user_id, badge_code) VALUES (?,?)", (user_id, badge_code))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def user_quiz_count(db, user_id):
    return db.execute("SELECT COUNT(*) AS c FROM results WHERE user_id=?", (user_id,)).fetchone()["c"]

def eval_badges_after_quiz(db, user_id, score, total):
    unlocked = []

    # pomocné hodnoty
    total_points = get_total_points(db, user_id)
    quizzes_done = user_quiz_count(db, user_id)

    for b in BADGES:
        r = b.get("rule", {})
        t = r.get("type")
        ok = False
        if t == "perfect_score":
            ok = (total > 0 and score == total)
        elif t == "quizzes_completed":
            ok = (quizzes_done >= int(r.get("min", 1)))
        elif t == "total_points":
            ok = (total_points >= int(r.get("min", 0)))
        # sem můžeš snadno doplnit další typy (streak apod.)

        if ok and grant_badge_once(db, user_id, b["code"]):
            unlocked.append(b)

    return unlocked

def load_all_quizzes():
    quizzes = []
    for path in glob.glob(os.path.join(QUIZ_FOLDER, "*.json")):
        quiz_id = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        quizzes.append({
            "id": quiz_id,
            "title": data.get("title", "Bez názvu"),
            "description": data.get("description", ""),
            "questions": data.get("questions", [])
        })
    return quizzes

def load_quiz(quiz_id):
    path = os.path.join(QUIZ_FOLDER, f"{quiz_id}.json")
    if not os.path.exists(path):
        return None, None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    quiz = {
        "id": quiz_id,
        "title": data.get("title", "Bez názvu"),
        "description": data.get("description", "")
    }
    return quiz, data



app = Flask(__name__)
app.secret_key = "tajneheslo"
DB = "quiz.db"
QUIZ_FOLDER = "quizzes"

@app.before_request
def load_ui_user():
    g.ui_user = None
    uid = session.get("user_id")
    if not uid:
        return
    db = get_db()
    row = db.execute("""
        SELECT id, username, 
               COALESCE(profile_image, '') AS profile_image,
               COALESCE(background_theme, '') AS background_theme
        FROM users WHERE id=?
    """, (uid,)).fetchone()
    if row:
        g.ui_user = {
            "id": row["id"],
            "username": row["username"],
            "profile_image": row["profile_image"],       # např. "cat.png" (ve /static/avatars/)
            "background_theme": row["background_theme"], # např. "space.jpg" (ve /static/themes/)
        }

@app.context_processor
def inject_ui_user():
    # Bude dostupné v KAŽDÉ šabloně jako 'ui_user'
    return {"ui_user": g.get("ui_user")}

# --- DB helper ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

# --- Init databáze ---
def init_db():
    db = get_db()
    db.executescript(open("schema.sql", encoding="utf-8").read())
    db.commit()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        uid = session.get("user_id")
        if not uid:
            return redirect(url_for("login", next=request.path))

        # 🛡️ kontrola, že user stále existuje
        db = get_db()
        user = db.execute("SELECT id, username FROM users WHERE id=?", (uid,)).fetchone()
        if not user:
            session.clear()
            flash("Tvůj účet už neexistuje, přihlas se znovu.")
            return redirect(url_for("login", next=request.path))

        # nastav do session jméno (kdyby se někde měnilo v DB)
        session["username"] = user["username"]

        return view(*args, **kwargs)
    return wrapped



# --- Autentizace ---
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u, p = request.form["user"], request.form["pwd"]
        p2 = request.form.get("pwd2","")
        if p != p2:
            flash("Hesla se neshodují.")
            return render_template("login_register.html", action="register")
        # (volitelně) ověř i pravidla síly hesla na serveru
        db = get_db()
        db.execute("INSERT INTO users (username, password_hash) VALUES (?,?)",
                   (u, generate_password_hash(p)))
        db.commit()
        return redirect(url_for("login"))
    return render_template("login_register.html", action="register")


@app.route("/login", methods=["GET","POST"])
def login():
    next_url = request.args.get("next") or url_for("index")
    if request.method == "POST":
        u, p = request.form["user"], request.form["pwd"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (u,)).fetchone()
        if user and check_password_hash(user["password_hash"], p):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            # upřednostni hidden pole next z formuláře, jinak parametr z URL
            dest = request.form.get("next") or next_url
            return redirect(dest)
        else:
            flash("Neplatné přihlašovací údaje.")
    return render_template("login_register.html", action="login", next=next_url)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Domů: seznam kvízů ---
@app.route("/")
@login_required
def index():
    db = get_db()
    user_id = session["user_id"]

    # načti jméno uživatele
    username = db.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()["username"]

    # načti všechny kvízy...
    quizzes = load_all_quizzes()
    for q in quizzes:
        last = db.execute(
            "SELECT id, created_at FROM results WHERE user_id=? AND quiz_id=? ORDER BY created_at DESC LIMIT 1",
            (user_id, q["id"])
        ).fetchone()
        q["last_result_id"] = last["id"] if last else None

        if last:
            from datetime import datetime, timedelta
            cooldown = timedelta(hours=12)
            diff = datetime.utcnow() - datetime.fromisoformat(last["created_at"])
            q["can_start"] = diff > cooldown
            q["remaining"] = None if q["can_start"] else (cooldown - diff)
        else:
            q["can_start"] = True
            q["remaining"] = None

        q["count"] = db.execute("SELECT COUNT(*) FROM results WHERE quiz_id=?", (q["id"],)).fetchone()[0]

    # body + level
    points_row = db.execute("SELECT total_points FROM user_points WHERE user_id=?", (user_id,)).fetchone()
    total_points = points_row["total_points"] if points_row else 0
    level, next_level = get_level_for_points(total_points)
    if next_level:
        span = max(1, next_level["min_points"] - level["min_points"])
        progress_pct = int((total_points - level["min_points"]) * 100 / span)
        to_next = next_level["min_points"] - total_points
    else:
        progress_pct = 100
        to_next = 0

    badges = get_user_badges(db, user_id)

    return render_template("index.html",
        username=username,
        quizzes=quizzes,
        total_points=total_points,
        level=level,
        progress_pct=progress_pct,
        to_next=to_next,
        badges=badges
    )


@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    db = get_db()
    user_id = session["user_id"]

    row = db.execute("SELECT total_points, COALESCE(points_spent,0) AS spent, "
                     "COALESCE(profile_image,'') AS profile_image, "
                     "COALESCE(background_theme,'') AS background_theme "
                     "FROM users u LEFT JOIN user_points p ON u.id=p.user_id "
                     "WHERE u.id=?", (user_id,)).fetchone()

    total_points = row["total_points"] if row and row["total_points"] else 0
    spent = row["spent"] if row else 0
    available = total_points - spent

    items = json.load(open("gamify/shop.json"))["items"]

    # přidej informaci, zda už to má
    for item in items:
        if item["type"] == "profile_image":
            item["owned"] = (row["profile_image"] == item["value"])
        elif item["type"] == "background":
            item["owned"] = (row["background_theme"] == item["value"])
        else:
            item["owned"] = False

    if request.method == "POST":
        code = request.form["code"]
        item = next((i for i in items if i["code"] == code), None)
        if item and available >= item["cost"] and not item["owned"]:
            if item["type"] == "background":
                db.execute("UPDATE users SET background_theme=?, points_spent=points_spent+? WHERE id=?",
                           (item["value"], item["cost"], user_id))
            elif item["type"] == "profile_image":
                db.execute("UPDATE users SET profile_image=?, points_spent=points_spent+? WHERE id=?",
                           (item["value"], item["cost"], user_id))
            db.commit()
            flash("Koupeno! 🎉")
        else:
            flash("Nemůžeš to koupit.", "error")

        return redirect(url_for("shop"))

    return render_template("shop.html", items=items, available=available)



# --- Zobrazení kvízu ---
@app.route("/quiz/<quiz_id>", methods=["GET","POST"])
@login_required
def quiz(quiz_id):
    quiz, data = load_quiz(quiz_id)
    if not quiz:
        flash("Kvíz nebyl nalezen.")
        return redirect(url_for("index"))

    if request.method == "POST":
        answers = {}
        score = 0
        for i, q in enumerate(data["questions"]):
            choice = request.form.get(f"q{i}")
            answers[str(i)] = choice
            if choice == q.get("correct"):
                score += 1

        db = get_db()
        cur = db.execute(
            "INSERT INTO results (user_id, quiz_id, score, answers_json) VALUES (?,?,?,?)",
            (session["user_id"], quiz_id, score, json.dumps(answers, ensure_ascii=False))
        )
        db.commit()
        result_id = cur.lastrowid

        # --- GAMIFICATION ---
        total_questions = len(data["questions"])
        base = score * 10
        bonus = 20                      # za dokončení
        perfect_bonus = 30 if score == total_questions and total_questions > 0 else 0
        earned = base + bonus + perfect_bonus

        # level před/po
        before_total = get_total_points(db, session["user_id"])
        before_level, _ = get_level_for_points(before_total)

        add_points(db, session["user_id"], earned, reason="quiz_completed",
                   meta={"quiz_id": quiz_id, "score": score, "total": total_questions})

        after_total = before_total + earned
        after_level, next_level = get_level_for_points(after_total)
        leveled_up = (after_level["code"] != before_level["code"])

        # odznaky (PO přičtení bodů, protože některé závisí na total_points)
        unlocked = eval_badges_after_quiz(db, session["user_id"], score, total_questions)

        # předáme do šablony → zobrazíme animace/hlášky
        return render_template(
            "result.html",
            quiz=quiz,
            score=score,
            total=total_questions,
            result_id=result_id,
            questions=data["questions"],
            answers=answers,
            earned_points=earned,
            total_points=after_total,
            level=after_level,
            next_level=next_level,
            leveled_up=leveled_up,
            unlocked_badges=unlocked
        )

    return render_template("quiz.html", quiz=quiz, data=data)


# --- Zobrazení review ---
@app.route("/review/<result_id>")
@login_required
def review(result_id):
    db = get_db()
    r = db.execute("SELECT * FROM results WHERE id=? AND user_id=?", 
                   (result_id, session["user_id"])).fetchone()
    if not r:
        flash("Výsledek nenalezen nebo k němu nemáš přístup.")
        return redirect(url_for("index"))

    quiz, data = load_quiz(r["quiz_id"])
    answers = json.loads(r["answers_json"])

    return render_template(
        "result.html",
        quiz=quiz,
        score=r["score"],
        total=len(data["questions"]),
        result_id=result_id,
        questions=data["questions"],
        answers=answers
    )


# --- Statistiky ---
@app.route("/quiz/<quiz_id>/stats")
@login_required
def quiz_stats(quiz_id):
    quiz, _ = load_quiz(quiz_id)
    if not quiz:
        return redirect(url_for("index"))

    db = get_db()

    user_scores = db.execute("""
            WITH last AS (
            SELECT user_id, MAX(created_at) AS max_created_at
            FROM results
            WHERE quiz_id=?
            GROUP BY user_id
            )
            SELECT u.id AS user_id,
                u.username,
                r.score,
                r.created_at,
                COALESCE(u.profile_image, '') AS profile_image
            FROM results r
            JOIN last l 
            ON l.user_id = r.user_id AND l.max_created_at = r.created_at
            JOIN users u 
            ON u.id = r.user_id
            WHERE r.quiz_id=?
            ORDER BY r.score DESC, r.created_at DESC


    """, (quiz_id, quiz_id)).fetchall()

    users = []
    for row in user_scores:
        tp = get_total_points(db, row["user_id"])  # 👈 načteme body přes helper
        level, next_level = get_level_for_points(tp)

        if next_level:
            span = max(1, next_level["min_points"] - level["min_points"])
            prog = int(max(0, min(100, (tp - level["min_points"]) * 100 / span)))
            to_next = max(0, next_level["min_points"] - tp)
        else:
            prog = 100
            to_next = 0

        users.append({
            "id": row["user_id"],
            "username": row["username"],
            "profile_image": row["profile_image"],
            "total_points": tp,
            "level": level,
            "next_level": next_level,
            "progress_pct": prog,
            "to_next": to_next,
            "score": row["score"],
            "created_at": row["created_at"]
        })



    return render_template("quiz_stats.html", quiz=quiz, users=users)



@app.route("/stats")
@login_required
def stats():
    db = get_db()

    # dynamicky načtené kvízy (kvůli fajfkám/křížkům)
    quizzes = load_all_quizzes()

    # souhrny uživatelů vč. celkových bodů
    users_raw = db.execute("""
        SELECT u.id, u.username,
            COALESCE(u.profile_image, '') AS profile_image,
            COALESCE(up.total_points, 0)  AS total_points,
            COALESCE(SUM(r.score), 0)     AS total_score,
            COUNT(r.id)                   AS quiz_count
        FROM users u
        LEFT JOIN user_points up ON up.user_id = u.id
        LEFT JOIN results r      ON r.user_id  = u.id
        GROUP BY u.id
        ORDER BY total_points DESC, total_score DESC, u.username ASC
    """).fetchall()


    # kdo vyplnil který kvíz (kvůli ✅/❌ sloupci)
    done = db.execute("""
        SELECT user_id, quiz_id
        FROM results
        GROUP BY user_id, quiz_id
    """).fetchall()
    done_map = {(row["user_id"], row["quiz_id"]) for row in done}

    # obohať uživatele o level a progres (→ next level)
    users = []
    for r in users_raw:
        tp = r["total_points"] or 0
        level, next_level = get_level_for_points(tp)
        if next_level:
            span = max(1, next_level["min_points"] - level["min_points"])
            prog = int( max(0, min(100, (tp - level["min_points"]) * 100 / span)) )
            to_next = max(0, next_level["min_points"] - tp)
        else:
            prog = 100
            to_next = 0
        users.append({
            "id": r["id"],
            "username": r["username"],
            "profile_image": r["profile_image"],  # 👈 přidáno
            "total_points": tp,
            "total_score": r["total_score"],
            "quiz_count": r["quiz_count"],
            "level": level,
            "next_level": next_level,
            "progress_pct": prog,
            "to_next": to_next
        })

    return render_template("stats.html",
                           users=users,
                           quizzes=quizzes,
                           done_map=done_map)



if __name__ == "__main__":
    if not os.path.exists(DB):
        with app.app_context():
            init_db()

    app.run(debug=True)
