import sqlite3
import os

class DB:
    DB_PATH = os.path.expanduser("~/.cache/xkcd-viewer/cache.db")

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()

    def get_conn(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.conn.close()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS comics (
                id INTEGER PRIMARY KEY,
                num INTEGER,
                month TEXT,
                day TEXT,
                year TEXT,
                title TEXT,
                alt TEXT,
                image_url TEXT
            )
        """)
        self.conn.commit()