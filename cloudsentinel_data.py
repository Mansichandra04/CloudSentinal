
import sqlite3
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

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

def create_user(username, password):
    """Create a user account with a hashed password."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, generate_password_hash(password))
        )

        connection.commit()
    finally:
        connection.close()


def verify_user(username, password):
    """Check a user's password without storing plain-text passwords."""
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()

        if result is None:
            return False

        return check_password_hash(result[0], password)
    finally:
        connection.close()

