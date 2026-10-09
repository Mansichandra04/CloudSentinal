
# CloudSentinel - Login Activity Monitor

login_records = [
    {"username": "rahul", "ip": "192.168.1.5", "status": "Success"},
    {"username": "admin", "ip": "192.168.1.10", "status": "Failed"},
    {"username": "admin", "ip": "192.168.1.10", "status": "Failed"},
    {"username": "admin", "ip": "192.168.1.10", "status": "Failed"},
    {"username": "priya", "ip": "192.168.1.8", "status": "Success"},
    {"username": "admin", "ip": "192.168.1.10", "status": "Failed"},
    {"username": "admin", "ip": "192.168.1.10", "status": "Failed"},
]

failed_attempts = {}

# Count failed login attempts for each user
for record in login_records:
    if record["status"] == "Failed":
        username = record["username"]

        if username not in failed_attempts:
            failed_attempts[username] = 0

        failed_attempts[username] += 1

# Display the results
print("=== CloudSentinel Login Report ===")

for username, count in failed_attempts.items():
    print(f"{username}: {count} failed login attempts")

    if count >= 5:
        print("ALERT: Suspicious login activity detected!")