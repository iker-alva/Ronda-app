"""SQLite storage for Ronda.

Zero dependencies: the whole backend runs on the Python standard library.
Datetimes are stored as local naive ISO strings ("YYYY-MM-DDTHH:MM").
"""
from __future__ import annotations

import os
import sqlite3
import sys
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_HOME = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR


def _data_dir() -> str:
    """Use a writable folder next to Ronda.exe, falling back to LOCALAPPDATA."""
    if os.environ.get("RONDA_DATA"):
        return os.path.abspath(os.environ["RONDA_DATA"])
    if getattr(sys, "frozen", False):
        preferred = os.path.join(APP_HOME, "Ronda data")
    else:
        preferred = os.path.join(BASE_DIR, "data")
    try:
        os.makedirs(preferred, exist_ok=True)
        probe = os.path.join(preferred, ".write-test")
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(probe)
        return preferred
    except OSError:
        fallback = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Ronda")
        os.makedirs(fallback, exist_ok=True)
        return fallback


DATA_DIR = _data_dir()
DB_PATH = os.environ.get("RONDA_DB", os.path.join(DATA_DIR, "ronda.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    username       TEXT NOT NULL UNIQUE,
    pass_hash      TEXT NOT NULL,
    pass_salt      TEXT NOT NULL,
    age            INTEGER NOT NULL DEFAULT 24,
    zone           TEXT NOT NULL DEFAULT 'Malasaña',
    city           TEXT NOT NULL DEFAULT 'Madrid',
    lat            REAL,
    lon            REAL,
    location_exact INTEGER NOT NULL DEFAULT 0,
    bio            TEXT NOT NULL DEFAULT '',
    avatar         TEXT NOT NULL DEFAULT '🦋',
    variant        INTEGER NOT NULL DEFAULT 0,
    interests      TEXT NOT NULL DEFAULT '[]',
    looking_for    TEXT NOT NULL DEFAULT '',
    status_note    TEXT NOT NULL DEFAULT '',
    max_distance   INTEGER NOT NULL DEFAULT 20,
    age_min        INTEGER NOT NULL DEFAULT 18,
    age_max        INTEGER NOT NULL DEFAULT 45,
    coins          INTEGER NOT NULL DEFAULT 0,
    welcome_bonus  INTEGER NOT NULL DEFAULT 0,
    last_daily     TEXT,
    created_at     TEXT NOT NULL,
    last_seen      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token      TEXT PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    category    TEXT NOT NULL DEFAULT 'planes',
    emoji       TEXT NOT NULL DEFAULT '✨',
    description TEXT NOT NULL DEFAULT '',
    start_at    TEXT NOT NULL,
    zone        TEXT NOT NULL,
    city        TEXT NOT NULL DEFAULT 'Madrid',
    lat         REAL,
    lon         REAL,
    venue       TEXT NOT NULL DEFAULT '',
    venue_id    INTEGER,
    spots       INTEGER NOT NULL DEFAULT 2,
    approval    INTEGER NOT NULL DEFAULT 0,
    vibe        TEXT NOT NULL DEFAULT '[]',
    status      TEXT NOT NULL DEFAULT 'open',   -- open | full | cancelled | done
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_plans_start ON plans(status, start_at);

CREATE TABLE IF NOT EXISTS venues (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    city     TEXT NOT NULL,
    area     TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'planes',
    emoji    TEXT NOT NULL DEFAULT '📍',
    lat      REAL NOT NULL,
    lon      REAL NOT NULL,
    blurb    TEXT NOT NULL DEFAULT '',
    UNIQUE(name, city)
);
CREATE INDEX IF NOT EXISTS idx_venues_city ON venues(city);

CREATE TABLE IF NOT EXISTS plan_members (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id   INTEGER NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role      TEXT NOT NULL DEFAULT 'member',   -- host | member
    status    TEXT NOT NULL DEFAULT 'joined',   -- joined | pending | declined
    note      TEXT NOT NULL DEFAULT '',
    joined_at TEXT NOT NULL,
    UNIQUE(plan_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_members_plan ON plan_members(plan_id, status);

CREATE TABLE IF NOT EXISTS swipes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    to_user    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action     TEXT NOT NULL,                   -- like | pass | super
    created_at TEXT NOT NULL,
    UNIQUE(from_user, to_user)
);

CREATE TABLE IF NOT EXISTS matches (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_a     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_b     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    thread_id  INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(user_a, user_b)
);

CREATE TABLE IF NOT EXISTS threads (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    kind       TEXT NOT NULL,                   -- match | plan
    plan_id    INTEGER REFERENCES plans(id) ON DELETE CASCADE,
    title      TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    last_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS thread_members (
    thread_id INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (thread_id, user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id  INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    user_id    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    body       TEXT NOT NULL,
    kind       TEXT NOT NULL DEFAULT 'text',    -- text | system
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_thread ON messages(thread_id, id);

CREATE TABLE IF NOT EXISTS reads (
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    thread_id    INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    last_read_id INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, thread_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind       TEXT NOT NULL,
    text       TEXT NOT NULL,
    plan_id    INTEGER,
    thread_id  INTEGER,
    read       INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications(user_id, read, id DESC);

CREATE TABLE IF NOT EXISTS coin_ledger (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    delta         INTEGER NOT NULL,
    kind          TEXT NOT NULL,                -- welcome | daily | like | superlike
    note          TEXT NOT NULL DEFAULT '',
    balance_after INTEGER NOT NULL,
    created_at    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ledger_user ON coin_ledger(user_id, id DESC);
"""


@contextmanager
def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
        # Lightweight migrations for databases created before the coin economy.
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
        if "coins" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN coins INTEGER NOT NULL DEFAULT 0")
        if "welcome_bonus" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN welcome_bonus INTEGER NOT NULL DEFAULT 0")
        if "last_daily" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN last_daily TEXT")
        if "city" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN city TEXT NOT NULL DEFAULT 'Madrid'")
        if "lat" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN lat REAL")
        if "lon" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN lon REAL")
        if "location_exact" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN location_exact INTEGER NOT NULL DEFAULT 0")
        plan_columns = {row["name"] for row in conn.execute("PRAGMA table_info(plans)")}
        if "city" not in plan_columns:
            conn.execute("ALTER TABLE plans ADD COLUMN city TEXT NOT NULL DEFAULT 'Madrid'")
        if "lat" not in plan_columns:
            conn.execute("ALTER TABLE plans ADD COLUMN lat REAL")
        if "lon" not in plan_columns:
            conn.execute("ALTER TABLE plans ADD COLUMN lon REAL")
        if "venue_id" not in plan_columns:
            conn.execute("ALTER TABLE plans ADD COLUMN venue_id INTEGER")
