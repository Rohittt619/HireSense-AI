import sqlite3
import os
from pathlib import Path

class ResumeDB:

    def __init__(self):
        db_dir = Path(__file__).resolve().parent
        os.makedirs(db_dir, exist_ok=True)
        db_path = db_dir / "resumes.db"

        self.conn = sqlite3.connect(
            str(db_path),
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