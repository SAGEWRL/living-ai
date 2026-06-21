# core/memory_db.py

import sqlite3
import time

DB_NAME = "living_ai.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT,

        text TEXT,

        emotion TEXT,

        timestamp REAL
    )

    """)

    conn.commit()

    conn.close()


def save_memory(user_id, text, emotion):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO memory (

        user_id,
        text,
        emotion,
        timestamp

    )

    VALUES (?, ?, ?, ?)

    """, (

        user_id,
        text,
        emotion,
        time.time()

    ))

    conn.commit()

    conn.close()


def get_recent(user_id, limit=5):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT text, emotion

    FROM memory

    WHERE user_id = ?

    ORDER BY id DESC

    LIMIT ?

    """, (

        user_id,
        limit

    ))

    data = cursor.fetchall()

    conn.close()

    return data