# CloudSentinel – Login Activity Monitoring System

## Project Overview

CloudSentinel is a Python-based login activity monitoring and access auditing project that demonstrates how suspicious authentication patterns can be identified using rule-based security monitoring.

The application uses FastAPI for its web application and REST APIs, SQLite for storing login records, and an HTML dashboard for displaying login statistics and security alerts.

It also includes a demonstration login page that records successful and failed login attempts.

## Features

- **Login Activity Monitoring:** Records usernames, IP addresses, login statuses, and timestamps.
- **Password Hashing:** Stores password hashes instead of plain-text passwords for registered demo users.
- **Failed Login Detection:** Generates a HIGH-severity alert when a username has five or more failed login attempts within a five-minute window.
- **Multiple-IP Detection:** Generates a MEDIUM-severity alert when a username has login activity from three or more distinct IP addresses.
- **Interactive Dashboard:** Displays login statistics, recent activity, and security alerts.
- **Automatic Dashboard Updates:** Refreshes dashboard data periodically without reloading the entire page.
- **REST API:** Provides endpoints for login records, security alerts, and application health.
- **Test Event Generation:** Supports generating sample login events for demonstration and testing.

## Technologies Used

- **Language:** Python
- **Backend:** FastAPI
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Templating:** Jinja2
- **Password Hashing:** Werkzeug
- **Development Tools:** Visual Studio Code, Git, GitHub

## Project Structure

```text
CloudSentinal/
├── main.py
├── database.py
├── monitor.py
├── app.py
├── fastapi_app.py
├── cloudsentinel_data.py
├── requirements.txt
├── .gitignore
├── README.md
├── start_project.bat
├── start_dashboard.bat
└── templates/
    ├── dashboard.html
    └── login.html
```

The SQLite database is created locally and is excluded from version control.

### Important files

- `fastapi_app.py` — Main FastAPI application, dashboard, login routes, and API endpoints.
- `cloudsentinel_data.py` — Database operations, login records, and user password verification.
- `templates/dashboard.html` — Dashboard interface and automatic data refresh.
- `templates/login.html` — Demonstration login form.
- `database.py` — Database initialization and sample data setup.
- `monitor.py` — Earlier login monitoring implementation.
- `app.py` — Earlier Flask dashboard implementation.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Excludes local files and environment-specific data from Git.

## Installation and Setup

### 1. Install Python

Install Python 3.10 or a compatible newer version.

Verify the installation:

```bash
python --version
```

### 2. Clone the repository

```bash
git clone https://github.com/Mansichandra04/CloudSentinal.git
cd CloudSentinal
```

### 3. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Initialize the database if needed

If this is a fresh setup and the required database tables have not been created, follow the database initialization process in `database.py` and the application's database module.

**Warning:** Check `database.py` before running it. It may recreate tables or replace existing sample records. Do not rerun it if you want to preserve existing practice data.

## Running the Application

From the project directory, start the FastAPI server:

```bash
python -m uvicorn fastapi_app:app --reload
```

Open these URLs in your browser:

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000` | Security dashboard |
| `http://127.0.0.1:8000/login` | Demonstration login page |
| `http://127.0.0.1:8000/docs` | Interactive API documentation |
| `http://127.0.0.1:8000/health` | Application health check |
| `http://127.0.0.1:8000/api/logins` | Login records |
| `http://127.0.0.1:8000/api/alerts` | Security alerts |

To stop the server, press `Ctrl + C` in the terminal.

## Testing the Login Page

1. Start the application.
2. Open `http://127.0.0.1:8000/login`.
3. Enter the credentials for a user registered in your local demo database.
4. A successful login records a successful event.
5. An unsuccessful login records a failed event.
6. Open the dashboard to inspect the recorded activity and any triggered alerts.

The login feature demonstrates password verification and event logging. It is not production-ready authentication.

## Security Alert Detection

### 1. Repeated failed login attempts

- **Severity:** HIGH
- **Condition:** Five or more failed login attempts for the same username within a five-minute window.
- **Purpose:** Demonstrates detection of repeated authentication failures.

### 2. Login activity from multiple IP addresses

- **Severity:** MEDIUM
- **Condition:** The same username has activity from three or more distinct IP addresses.
- **Purpose:** Highlights activity that may warrant investigation.

These are demonstration rules, not proof of an attack. Multiple IP addresses can be legitimate, and repeated failures can have benign causes.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays the dashboard |
| GET | `/login` | Displays the login form |
| POST | `/login` | Processes a login attempt |
| GET | `/health` | Returns application health status |
| GET | `/api/logins` | Returns login records |
| GET | `/api/alerts` | Returns security alerts |
| POST | `/api/test-login` | Generates a test login event when enabled |

Use `/docs` to inspect the available API operations and parameters.

The test-login endpoint is intended for development and demonstration. Its availability may be disabled in hosted environments.

## Security and Limitations

- This is an educational project, not a production security monitoring platform.
- The current application uses a local SQLite database.
- Login events are generated by the demonstration application or its test functionality; they are not automatically collected from external cloud services.
- The alert rules use fixed thresholds and may produce false positives.
- Production deployment would require additional protections, including secure session management, CSRF protection where applicable, rate limiting, secure configuration, and appropriate access controls.
- Do not commit `.env` files, credentials, or local database files to the repository.

## Future Enhancements

- Detect successful logins following repeated failed attempts.
- Add unusual login-time detection.
- Identify repeated attempts across multiple usernames.
- Add filters for usernames, statuses, and timestamps.
- Improve alert history and severity reporting.
- Explore integration with cloud audit logs.

## Learning Outcomes

This project provides practical experience with:

- Python application development
- FastAPI and REST APIs
- SQLite database operations
- Password hashing and verification
- Login auditing and event logging
- Rule-based security monitoring
- HTML, CSS, and JavaScript
- Git and GitHub version control

## Author

Developed as a cybersecurity-focused academic project demonstrating login monitoring, access auditing, and suspicious authentication detection.

## License

This project is intended for educational and learning purposes.
