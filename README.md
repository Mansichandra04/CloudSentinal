# CloudSentinel

## Python-Based Security Monitoring and Access Audit System

### Project Overview

CloudSentinel is a beginner-friendly security monitoring project that identifies potentially suspicious login activity.

It uses Python, Flask, and SQLite to store login records and display security alerts on a web dashboard.

### Features

- Stores login records in an SQLite database.
- Records usernames, IP addresses, login status, and timestamps.
- Displays login activity on a web dashboard.
- Counts failed login attempts.
- Detects five or more failed login attempts by the same user within five minutes.
- Displays an alert when this rule is triggered.

### Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS

### How It Works

1. Sample login events are saved in the database.
2. Python retrieves the login records.
3. The system groups failed login attempts by username.
4. It checks whether five or more failures occurred within five minutes.
5. The dashboard displays suspicious activity.

### How to Run

1. Install Python.
2. Install Flask using `python -m pip install flask`.
3. Run `python database.py` to create the sample database.
4. Run `python app.py` to start the dashboard.
5. Open `http://127.0.0.1:5000` in your browser.

**Note:** Running `database.py` resets the sample login records.

### Current Limitations

This version uses sample login data. It does not yet connect to real cloud audit logs.

### Future Improvements

- Add login-record filters.
- Integrate real cloud audit logs.
- Deploy the application to Microsoft Azure.
- Improve security alerts.

### Learning Outcomes

This project demonstrates Python programming, SQL database operations, web development, and basic security-event monitoring.