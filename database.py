import sqlite3
from datetime import datetime

DATABASE = "qr_history.db"


def create_table():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS qr_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_history(action, content):
    connection = sqlite3.connect(DATABASE)

    connection.execute(
        """
        INSERT INTO qr_history (action, content, created_at)
        VALUES (?, ?, ?)
        """,
        (action, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    history = connection.execute(
        "SELECT * FROM qr_history ORDER BY id DESC"
    ).fetchall()

    connection.close()
    return history