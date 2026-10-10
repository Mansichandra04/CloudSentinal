# CloudSentinel – Cloud Security Monitoring and Access Audit System

## Project Overview

CloudSentinel is a Python-based security monitoring and access audit system designed to analyze login activity and identify potentially suspicious authentication behavior.

The project uses FastAPI to provide a web application and REST API, SQLite to store login records, and an HTML dashboard to display login statistics and security alerts.

It detects repeated failed login attempts and flags suspicious activity for further investigation.

## Features

- **Login Activity Monitoring:** Displays recorded login events, including usernames, IP addresses, login statuses, and event timestamps.
- **Security Alert Detection:** Generates a HIGH-severity alert when a user has five or more failed login attempts within a five-minute window.
- **Interactive Dashboard:** Displays total login events, successful logins, failed logins, and security alerts.
- **Automatic Dashboard Updates:** Refreshes dashboard data automatically every 10 seconds without reloading the entire page.
- **REST API:** Provides endpoints to retrieve login records, security alerts, and application health status.
- **SQLite Database:** Stores login activity for monitoring and auditing.
- **Test Login Generator:** Generate successful and failed login events directly from the dashboard for demonstration and testing.
- **Interactive Dashboard Refresh:** View updated login statistics, recent activity, and security alerts after generating test events.

## Technologies Used

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Templating Engine:** Jinja2
- **Development Tools:** Visual Studio Code, Git, GitHub

## Project Structure

```text
CloudSentinel/
├── main.py
├── database.py
├── monitor.py
├── app.py
├── fastapi_app.py
├── cloudsentinel_data.py
├── cloudsentinel.db
├── templates/
│   └── dashboard.html
├── README.md
└── .gitignore
```

**Important files:**

- `fastapi_app.py` – Main FastAPI application, dashboard route, API endpoints, and security alert detection.
- `cloudsentinel_data.py` – Retrieves login records from the SQLite database.
- `templates/dashboard.html` – Dashboard interface and automatic data updates.
- `database.py` – Initializes the login log table and inserts sample records.
- `monitor.py` – Earlier login monitoring implementation.
- `app.py` – Earlier Flask dashboard implementation.

The SQLite database file is created locally and is not intended to be committed to GitHub.

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

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install fastapi uvicorn jinja2
```

### 5. Initialize the database

If you are setting up the project for the first time and the local database does not exist, initialize it using:

```bash
python database.py
```

**Warning:** Running `database.py` again may recreate the practice table and replace its existing sample records. Do not rerun it if you want to preserve existing data.

## Running the Application

Start the FastAPI server from the project directory:

```bash
python -m uvicorn fastapi_app:app --reload
```

Open the following URLs in your browser:

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000` | Security dashboard |
| `http://127.0.0.1:8000/docs` | Interactive API documentation |
| `http://127.0.0.1:8000/health` | Application health check |
| `http://127.0.0.1:8000/api/logins` | Retrieve login records |
| `http://127.0.0.1:8000/api/alerts` | Retrieve security alerts |

To stop the server, press `Ctrl + C` in the terminal.

## How Security Alert Detection Works

1. The application retrieves login records from the SQLite database.
2. It identifies records with a failed login status.
3. It groups failed attempts by username.
4. It checks whether five or more failed attempts occurred within a five-minute window.
5. If the threshold is reached, it generates a HIGH-severity security alert.
6. The dashboard displays the alert and updates its statistics automatically.
- **Multiple-IP Detection:** Generates a medium-severity alert when the same username has login activity from three or more distinct IP addresses.

This rule-based approach demonstrates a basic security monitoring technique for identifying repeated authentication failures.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays the security dashboard |
| GET | `/health` | Returns application health status |
| GET | `/api/logins` | Returns login records in JSON format |
| GET | `/api/alerts` | Returns detected security alerts in JSON format |
- `POST /api/test-login` — Adds a test login event. Optional query parameters: `username` and `status` (`success` or `failed`).

## Current Scope and Limitations

- The current version analyzes login records already stored in the local SQLite database.
- The dashboard does not independently generate real login events.
- The alert detection uses a fixed threshold of five failed attempts within five minutes.
- This is an educational project and is not a replacement for a production cloud security monitoring platform.

## Future Enhancements

- Add a controlled test feature to generate sample login events.
- Display new security alerts as login activity changes.
- Add filters for usernames, login statuses, and timestamps.
- Introduce alert history and additional detection rules.
- Explore integration with cloud audit logs.

## Learning Outcomes

Through this project, I am developing practical experience with:

- Python backend development
- REST API development using FastAPI
- SQLite database operations
- Authentication log analysis
- Rule-based security alert detection
- HTML, CSS, and JavaScript
- Git and GitHub version control

## Author

Developed as a cybersecurity-focused academic project to demonstrate basic security monitoring, login auditing, and suspicious authentication detection.

## License

This project is intended for educational and learning purposes.
```