import sqlite3


class ResumeDB:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/resumes.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume TEXT,

            ats REAL,

            similarity REAL,

            skill REAL,

            overall REAL,

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.conn.commit()

    def save(
        self,
        resume,
        ats,
        similarity,
        skill,
        overall
    ):

        self.cursor.execute("""

        INSERT INTO history(

        resume,
        ats,
        similarity,
        skill,
        overall

        )

        VALUES(?,?,?,?,?)

        """, (

            resume,
            ats,
            similarity,
            skill,
            overall

        ))

        self.conn.commit()

    def fetch(self):

        self.cursor.execute("""

        SELECT *

        FROM history

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()