#!/usr/bin/env python3
"""
Edukativní demo aplikace (Flask)
---------------------------------
Ukazuje, jak NE/ukládat hesla:
 - Registrace uloží heslo v plaintextu i bezpečně (bcrypt hash) -> srovnání na /admin.
 - Cíl: demonstrovat, že admin webu může vidět hesla, pokud je ukládá špatně.


Spuštění:
  pip install flask bcrypt
  python app.py
  Otevři: http://127.0.0.1:5000
  Admin pohled: http://127.0.0.1:5000/admin?key=teacher
  Reset dat:    http://127.0.0.1:5000/reset?key=teacher

Pozn.: Admin klíč si změň v ADMIN_KEY níže.


@todo udelat hinty do javascriptu a udelat moznost stranku hackovat

"""

from __future__ import annotations
from flask import Flask, request, redirect, url_for, render_template_string, abort
from datetime import datetime
import bcrypt
import html
from jinja2 import DictLoader
from collections import defaultdict
import json
import time
from flask import Response
import threading

SCORES = defaultdict(int)   # user -> best_score
SCORES_LOCK = threading.Lock()



# --- šablony (Tailwind přes CDN) ---
BASE = r"""
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ title }}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    // jednoduchý meter síly hesla
    function strengthScore(p){
      let s = 0;
      if(!p) return 0;
      if(p.length >= 8) s++;
      if(/[A-Z]/.test(p)) s++;
      if(/[a-z]/.test(p)) s++;
      if(/[0-9]/.test(p)) s++;
      if(/[^A-Za-z0-9]/.test(p)) s++;
      return Math.min(s,5);
    }
    function updateMeter(){
      const p = document.getElementById('pwd')?.value || '';
      const s = strengthScore(p);
      const bar = document.getElementById('meter');
      const label = document.getElementById('meterLabel');
      const colors = ['bg-gray-300','bg-red-500','bg-orange-500','bg-yellow-500','bg-green-500','bg-emerald-600'];
      bar.className = 'h-2 rounded transition-all ' + colors[s];
      bar.style.width = (s*20)+'%';
      const txt = ['(prázdné)','velmi slabé','slabé','OK','silné','velmi silné'][s];
      label.textContent = txt;
    }
    document.addEventListener('DOMContentLoaded', ()=>{
      const pwd = document.getElementById('pwd');
      pwd && pwd.addEventListener('input', updateMeter);
      updateMeter();
    });
  </script>
</head>
<body class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-emerald-50">
  <header class="p-6">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-black tracking-tight text-indigo-900">{{ title }}</h1>
    </div>
  </header>
  <main class="max-w-4xl mx-auto p-6">
    {% block content %}{% endblock %}
  </main>
</body>
</html>
"""



app = Flask(__name__)
app.jinja_loader = DictLoader({
    "base.html": BASE,  # BASE je tvůj dlouhý HTML řetězec se skeletonem
})

# --- "databáze" v paměti (na demo stačí) ---
DB: list[dict] = []

# --- nastavení ---
ADMIN_KEY = "teacher"  # změň si pro lekci
APP_TITLE = "Kočičí útěk!" 

INDEX = r"""
{% extends 'base.html' %}
{% block content %}
  <div>
    <div class="bg-white/80 backdrop-blur shadow rounded-2xl p-6 border border-slate-100">

      <!-- 🔔 DISCLAIMER -->
      <div class="mb-4 p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-sm">
        <strong>Upozornění:</strong> Toto je <u>edukativní aplikace</u> ukazující rizika při zadávání hesel. 
        <br>
        <strong>Nikdy zde nezadávejte své skutečné heslo!</strong>
      </div>

      <h2 class="text-xl font-bold mb-4">Registrace do hry</h2>

      <form id="regForm" method="post" action="{{ url_for('register') }}" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700">Uživatelské jméno</label>
          <input name="user" required maxlength="40"
            class="border-2 p-2 mt-1 w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500"
            placeholder="např. superhrdina" />
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700">Heslo</label>
          <input id="pwd" name="pwd" type="password" required
            class="border-2 p-2 mt-1 w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500"
            placeholder="vaše heslo" />
          <div class="mt-2 h-2 w-full bg-slate-200 rounded">
            <div id="meter" class="h-2 rounded"></div>
          </div>
          <div id="meterLabel" class="text-xs text-slate-600 mt-1"> </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700">Potvrzení hesla</label>
          <input id="pwd2" type="password" required
            class="border-2 p-2 mt-1 w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500"
            placeholder="zadejte heslo znovu" />
          <div id="pwdMismatch" class="text-xs text-red-600 mt-1 hidden">Hesla se neshodují</div>
        </div>

        <button class="w-full py-2 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 shadow">
          Registrovat
        </button>
      </form>
    </div>
  </div>

  <script>
  const form = document.getElementById('regForm');
  const pwd = document.getElementById('pwd');
  const pwd2 = document.getElementById('pwd2');
  const mismatch = document.getElementById('pwdMismatch');

  function checkMatch() {
    if (pwd.value && pwd2.value && pwd.value !== pwd2.value) {
      mismatch.classList.remove('hidden');
      return false;
    } else {
      mismatch.classList.add('hidden');
      return true;
    }
  }

  pwd2.addEventListener('input', checkMatch);
  pwd.addEventListener('input', checkMatch);

  form.addEventListener('submit', (e) => {
    if (!checkMatch()) {
      e.preventDefault();
      pwd2.focus();
    }
  });
  </script>
{% endblock %}
"""


ADMIN = r"""
{% extends 'base.html' %}
{% block content %}
  <div class="bg-white/90 backdrop-blur shadow rounded-2xl p-6 border border-slate-100">
    <div class="flex items-center justify-between gap-3">
      <h2 class="text-2xl font-bold">Admin pohled (edukativní)</h2>
      <div class="flex gap-2">
        <a class="px-3 py-2 rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200" href="{{ url_for('index') }}">↩︎ Zpět</a>
        <a class="px-3 py-2 rounded-lg text-rose-700 bg-rose-50 hover:bg-rose-100" href="{{ url_for('reset') }}?key={{ key }}">Reset</a>
      </div>
    </div>
    <p class="text-sm text-slate-600 mt-1">Takhle by <strong>neměl</strong> vypadat reálný web: vidíš všechna hesla v prostém textu.</p>

    <div class="mt-4 overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left text-slate-600">
            <th class="py-2">Uživatel</th>
            <th class="py-2">Plaintext (špatně)</th>
            <th class="py-2">Hash (správně)</th>
            <th class="py-2">IP</th>
            <th class="py-2">Čas</th>
          </tr>
        </thead>
        <tbody>
          {% for r in rows %}
          {% set pw = r.password_plain %}
          {% if pw|length >= 3 %}
            {% set masked = pw[0] ~ ('*' * (pw|length - 2)) ~ pw[-1] %}
          {% else %}
            {% set masked = '*' * (pw|length) %}
          {% endif %}
          <tr class="border-t">
            <td class="py-2 font-medium">{{ r.user }}</td>
            <td class="py-2 text-rose-700">
              <span class="plaintext"
                    data-full="{{ pw }}"
                    data-masked="{{ masked }}">
                {{ masked }}
              </span>
              <button class="ml-2 text-xs text-blue-600 hover:underline toggle-btn">👁 Zobrazit</button>
            </td>
            <td class="py-2 text-slate-500 text-xs break-all">{{ r.password_hash }}</td>
            <td class="py-2 text-slate-600">{{ r.ip }}</td>
            <td class="py-2 text-slate-600">{{ r.created_at }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    {% if not rows %}
      <p class="text-slate-500 mt-4">Zatím žádná data.</p>
    {% endif %}

    <div class="mt-6 bg-amber-50 border border-amber-200 rounded-xl p-4 text-amber-900">
      <strong>Poučení:</strong>
      <ul class="list-disc pl-5 mt-2 space-y-1">
        <li>Provozovatel <em>může</em> vidět heslo, pokud ho ukládá špatně.</li>
        <li>Správně se ukládá pouze <strong>hash</strong> (nevratný otisk) – zde zobrazen pro srovnání.</li>
        <li>Nikdy nezadávejte svá reálná hesla na neznámé stránky.</li>
      </ul>
    </div>
  </div>

  <script>
    document.querySelectorAll('.toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const span = btn.previousElementSibling;
        const isMasked = span.textContent.includes('*');

        if (isMasked) {
          span.textContent = span.dataset.full;
          btn.textContent = "👁‍🗨 Skrýt";
        } else {
          span.textContent = span.dataset.masked;
          btn.textContent = "👁 Zobrazit";
        }
      });
    });
  </script>
{% endblock %}
"""


THANKS = r"""
{% extends 'base.html' %}
{% block content %}
  <div class="mx-auto max-w-lg bg-white/90 backdrop-blur shadow rounded-2xl p-6 border border-slate-100 text-center">
    <div class="text-4xl">🎉</div>
    <h2 class="text-xl font-bold mt-2">Díky za registraci, {{ user }}!</h2>
    <p class="text-slate-600 mt-2">Tak co, jdeme na to?</p>
    <div class="mt-4 flex gap-2 justify-center">
      <a class="px-4 py-2 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700"
   href="{{ url_for('game', user=user) }}">▶︎ Hrát hru</a>
    </div>
  </div>
{% endblock %}
"""

GAME = r"""
{% extends 'base.html' %}
{% block content %}
<div class="grid md:grid-cols-[1fr] gap-4">
  <div class="bg-white/90 backdrop-blur shadow rounded-2xl p-6 border border-slate-100">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold">Kočičí útěk – hráč {{ user or 'Host' }}</h2>
      <div class="text-slate-600 text-sm">
        Ovládání: <kbd class="px-1 py-0.5 border rounded">SPACE</kbd> / <kbd class="px-1 py-0.5 border rounded">↑</kbd> skok,
        <kbd class="px-1 py-0.5 border rounded">R</kbd> restart
      </div>
    </div>
  <div class="mt-3 flex flex-col gap-4">
    <div>
      <canvas id="game" width="800" height="250"
        class="w-full max-w-[800px] bg-slate-100 rounded-lg border border-slate-200"></canvas>
    </div>
    <div class="bg-white/80 rounded-lg border p-4">
      <h3 class="font-semibold mb-2">Živé skóre (TOP 10)</h3>
      <ol id="leaderboard" class="text-sm space-y-1"></ol>
    </div>
  </div>
    <div class="mt-3 flex items-center justify-between">
      <div class="text-slate-700">Skóre: <span id="score">0</span></div>
      <a href="{{ url_for('index') }}" class="px-3 py-2 rounded-lg bg-slate-100 hover:bg-slate-200">↩︎ Zpět</a>
    </div>
  </div>
</div>

<!-- těsně před game.js -->
<script>
  window.GAME_USER = "{{ (user or 'Host')|e }}";
</script>
<script src="{{ url_for('static', filename='game.js') }}" defer></script>


{% endblock %}
"""

STATS = r"""
{% extends 'base.html' %}
{% block content %}
<div class="bg-white/95 backdrop-blur shadow rounded-2xl p-8 border border-slate-200 max-w-3xl mx-auto">
  <h2 class="text-3xl font-bold mb-6 text-center">Živé statistiky</h2>
  <ol id="leaderboard" class="text-lg space-y-2 font-mono"></ol>
</div>

<script>
(() => {
  const lb = document.getElementById('leaderboard');
  const es = new EventSource("/scores_stream");
  es.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      const list = data.leaderboard || [];
      lb.innerHTML = list.map((row, i) =>
        `<li class="flex justify-between border-b border-slate-200 pb-1">
           <span class="text-slate-800">${i+1}. ${escapeHtml(row.user)}</span>
           <span class="font-bold tabular-nums">${row.score}</span>
         </li>`
      ).join("") || '<li class="text-slate-500">Zatím žádná skóre.</li>';
    } catch(e) {
      console.error(e);
    }
  };

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => (
      {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]
    ));
  }
})();
</script>
{% endblock %}
"""



# --- helpery ---
def hash_password(pw: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    h = bcrypt.hashpw(pw.encode('utf-8'), salt)
    return h.decode('utf-8')

# --- routy ---
@app.route("/", methods=["GET"])
def index():
    recent = list(reversed(DB[-5:]))
    return render_template_string(INDEX, title=APP_TITLE, recent=recent)

@app.route("/register", methods=["POST"])
def register():
    user = request.form.get("user", "").strip()
    pwd  = request.form.get("pwd", "")
    if not user or not pwd:
        return redirect(url_for('index'))
    row = {
        'user': html.escape(user),
        'password_plain': pwd,  # záměrně špatně – pro demo
        'password_hash': hash_password(pwd),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr or '?'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    DB.append(row)
    return render_template_string(THANKS, title=APP_TITLE, user=row['user'])

@app.route("/admin")
def admin():
    key = request.args.get('key','')
    if key != ADMIN_KEY:
        abort(403)
    return render_template_string(ADMIN, title=f"Admin – {APP_TITLE}", rows=DB, key=key)

@app.route("/reset")
def reset():
    key = request.args.get('key','')
    if key != ADMIN_KEY:
        abort(403)
    DB.clear()
    return redirect(url_for('admin', key=key))

@app.route("/game")
def game():
    user = request.args.get("user", "Host")
    return render_template_string(GAME, title=f"Hra – {APP_TITLE}", user=user)

@app.route("/score", methods=["POST"])
def score():
    data = request.get_json(force=True, silent=True) or {}
    user = (data.get("user") or "Host")[:40]
    score = int(data.get("score") or 0)

    with SCORES_LOCK:
        if score > SCORES[user]:
            SCORES[user] = score
    return {"ok": True, "best": SCORES[user]}

def make_leaderboard(top_n=10):
    with SCORES_LOCK:
        items = sorted(SCORES.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    return [{"user": u, "score": s} for u, s in items]

@app.route("/scores_stream")
def scores_stream():
    def event_stream():
        # posílej každých ~1 s
        while True:
            payload = json.dumps({"leaderboard": make_leaderboard(10)}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
            time.sleep(1)
    return Response(event_stream(), mimetype="text/event-stream")

# --- route pro promítání ---
@app.route("/stats")
def stats():
    return render_template_string(STATS, title=f"Živé statistiky – {APP_TITLE}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
