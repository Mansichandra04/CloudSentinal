
import sqlite3

DATABASE_NAME = "cloudsentinel.db"
FAILED_LOGIN_THRESHOLD = 5

# Connect to the existing database.
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

# Read all login records from the database.
cursor.execute("""
SELECT username, ip_address, status
FROM login_logs
""")

records = cursor.fetchall()
connection.close()

# Count failed attempts for each user.
failed_attempts = {}

for username, ip_address, status in records:
    if status == "Failed":
        if username not in failed_attempts:
            failed_attempts[username] = 0

        failed_attempts[username] += 1

# Display the monitoring report.
print("=== CloudSentinel Security Report ===")
print("Total login records:", len(records))

alerts_found = False

for username, count in failed_attempts.items():
    print(f"{username}: {count} failed login attempts")

    if count >= FAILED_LOGIN_THRESHOLD:
        print(f"ALERT: Suspicious activity for user '{username}'")
        alerts_found = True

if not alerts_found:
    print("No suspicious login patterns detected.")