"""SQLite storage: users, sessions, messages, memories, advice."""
import datetime as dt
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
  session_no INTEGER, sim_date TEXT, started TEXT, ended TEXT, summary TEXT);
CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER,
  role TEXT, content TEXT, created TEXT);
CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
  session_id INTEGER, session_no INTEGER, category TEXT, content TEXT, importance INTEGER, created TEXT);
CREATE TABLE IF NOT EXISTS advice(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
  session_id INTEGER, session_no INTEGER, text TEXT, metric TEXT, direction TEXT, target REAL,
  baseline REAL, status TEXT DEFAULT 'open', current REAL, change_pct REAL, outcome_session_no INTEGER);
"""


def now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


class Database:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    # generic helpers
    def q(self, sql, params=()):
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def x(self, sql, params=()):
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur.lastrowid

    # users / sessions
    def ensure_user(self, user_id, name):
        self.x("INSERT OR IGNORE INTO users(id,name) VALUES(?,?)", (user_id, name))

    def user(self, user_id):
        r = self.q("SELECT * FROM users WHERE id=?", (user_id,))
        return r[0] if r else None

    def new_session(self, user_id, sim_date):
        n = self.session_count(user_id) + 1
        sid = self.x("INSERT INTO sessions(user_id,session_no,sim_date,started) VALUES(?,?,?,?)",
                     (user_id, n, str(sim_date), now()))
        return {"id": sid, "session_no": n, "sim_date": sim_date}

    def session_count(self, user_id):
        return self.q("SELECT COUNT(*) c FROM sessions WHERE user_id=?", (user_id,))[0]["c"]

    def end_session(self, session_id, summary):
        self.x("UPDATE sessions SET ended=?, summary=? WHERE id=?", (now(), summary, session_id))

    def sessions(self, user_id):
        return self.q("SELECT * FROM sessions WHERE user_id=? ORDER BY session_no", (user_id,))

    # messages
    def add_message(self, session_id, role, content):
        self.x("INSERT INTO messages(session_id,role,content,created) VALUES(?,?,?,?)",
               (session_id, role, content, now()))

    def messages(self, session_id):
        return self.q("SELECT role,content FROM messages WHERE session_id=? ORDER BY id", (session_id,))

    # memories
    def add_memory(self, user_id, session, category, content, importance):
        self.x("INSERT INTO memories(user_id,session_id,session_no,category,content,importance,created)"
               " VALUES(?,?,?,?,?,?,?)",
               (user_id, session["id"], session["session_no"], category, content, importance, now()))

    def memories(self, user_id):
        return self.q("SELECT * FROM memories WHERE user_id=? ORDER BY id", (user_id,))

    # advice
    def add_advice(self, user_id, session, text, metric, direction, target, baseline):
        return self.x("INSERT INTO advice(user_id,session_id,session_no,text,metric,direction,target,baseline)"
                      " VALUES(?,?,?,?,?,?,?,?)",
                      (user_id, session["id"], session["session_no"], text, metric, direction, target, baseline))

    def advice(self, user_id):
        return self.q("SELECT * FROM advice WHERE user_id=? ORDER BY id", (user_id,))

    def update_advice(self, advice_id, status, current, change_pct, outcome_session_no):
        self.x("UPDATE advice SET status=?,current=?,change_pct=?,outcome_session_no=? WHERE id=?",
               (status, current, change_pct, outcome_session_no, advice_id))

    def reset_user(self, user_id):
        for t in ("memories", "advice"):
            self.x(f"DELETE FROM {t} WHERE user_id=?", (user_id,))
        self.x("DELETE FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE user_id=?)", (user_id,))
        self.x("DELETE FROM sessions WHERE user_id=?", (user_id,))
