
import sqlite3
from datetime import datetime
from pathlib import Path

# Use the database file in the same folder as this Python file.
DATABASE_PATH = Path(__file__).resolve().parent / "cloudsentinel.db"


def get_login_records():
    """Return login records, newest first."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, username, ip_address, status, event_time
            FROM login_logs
            ORDER BY event_time DESC, id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def add_login_record(username, ip_address, status):
    """Insert one login event into the database."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO login_logs (username, ip_address, status, event_time)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                ip_address,
                status,
                datetime.now().isoformat(timespec="seconds")
            )
        )
        connection.commit()
    finally:
        connection.close()
