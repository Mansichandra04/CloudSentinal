
import sqlite3
from datetime import datetime, timedelta

connection = sqlite3.connect("cloudsentinel.db")
cursor = connection.cursor()

# Recreate the practice table with a timestamp column.
cursor.execute("DROP TABLE IF EXISTS login_logs")

cursor.execute("""
CREATE TABLE login_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    status TEXT NOT NULL,
    event_time TEXT NOT NULL
)
""")

now = datetime.now()

sample_records = [
    ("rahul", "192.168.1.5", "Success", now - timedelta(minutes=10)),
    ("admin", "192.168.1.10", "Failed", now - timedelta(minutes=5)),
    ("admin", "192.168.1.10", "Failed", now - timedelta(minutes=4)),
    ("admin", "192.168.1.10", "Failed", now - timedelta(minutes=3)),
    ("priya", "192.168.1.8", "Success", now - timedelta(minutes=2)),
    ("admin", "192.168.1.10", "Failed", now - timedelta(minutes=1)),
    ("admin", "192.168.1.10", "Failed", now),
]

cursor.executemany("""
INSERT INTO login_logs
(username, ip_address, status, event_time)
VALUES (?, ?, ?, ?)
""", [
    (username, ip, status, event_time.isoformat(timespec="seconds"))
    for username, ip, status, event_time in sample_records
])

connection.commit()
connection.close()

print("Practice database created with 7 sample login records.")