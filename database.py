import sqlite3

DB_PATH = "edr.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            pid       INTEGER NOT NULL,
            name      TEXT    NOT NULL,
            username  TEXT,
            cpu       REAL,
            memory    REAL,
            timestamp TEXT    NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            local_ip    TEXT,
            local_port  INTEGER,
            remote_ip   TEXT,
            remote_port INTEGER,
            status      TEXT,
            timestamp   TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_events (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            path      TEXT    NOT NULL,
            event     TEXT    NOT NULL,
            timestamp TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()
