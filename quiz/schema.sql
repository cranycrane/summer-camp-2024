CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT DEFAULT NULL,
    profile_image TEXT,
    background_theme TEXT DEFAULT NULL,
    points_spent INTEGER DEFAULT 0
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    quiz_id TEXT,
    score INTEGER,
    answers_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Body
CREATE TABLE IF NOT EXISTS user_points (
  user_id INTEGER PRIMARY KEY,
  total_points INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS points_ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  delta INTEGER NOT NULL,
  reason TEXT NOT NULL,
  meta_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Odznaky
CREATE TABLE IF NOT EXISTS user_badges (
  user_id INTEGER NOT NULL,
  badge_code TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(user_id, badge_code),
  FOREIGN KEY(user_id) REFERENCES users(id)
);


INSERT OR IGNORE INTO users (username, password_hash)
VALUES (
    'admin',
    '$pbkdf2-sha256$29000$Fj7N2Q8oYkUEVQvABnKZVQ$9zKtdqCmUXL4g4G3xkhnKH5XjzkR9XJYBo0mG43vBBk'
);