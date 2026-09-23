import sqlite3
from datetime import datetime


DB_NAME = "study_memory.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_memory(memory_text):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (memory, created_at)
        VALUES (?, ?)
        """,
        (
            memory_text,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_memories(limit=10):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory
        FROM memories
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = cursor.fetchall()

    connection.close()

    return [row[0] for row in results]


def search_memories(keyword, limit=10):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory
        FROM memories
        WHERE memory LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (f"%{keyword}%", limit)
    )

    results = cursor.fetchall()

    connection.close()

    return [row[0] for row in results]
