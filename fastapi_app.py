
from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from cloudsentinel_data import get_login_records, add_login_record
from pathlib import Path


app = FastAPI(
    title="CloudSentinel",
    description="Cloud security monitoring and access audit system",
    version="1.0.0"
)



templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent / "templates")
)


def detect_security_alerts(records):
    """Detect five or more failed logins within five minutes."""
    failed_by_user = {}

    for record in records:
        if record["status"].lower() == "failed":
            username = record["username"]
            failed_by_user.setdefault(username, []).append(record)

    alerts = []

    for username, failures in failed_by_user.items():
        failures.sort(key=lambda record: record["event_time"])

        for start in range(len(failures)):
            window_start = datetime.fromisoformat(
                failures[start]["event_time"]
            )
            window_end = window_start + timedelta(minutes=5)

            matching = [
                event for event in failures[start:]
                if window_start <= datetime.fromisoformat(
                    event["event_time"]
                ) <= window_end
            ]

            if len(matching) >= 5:
                alerts.append({
                    "username": username,
                    "severity": "HIGH",
                    "failed_attempts": len(matching),
                    "window_minutes": 5,
                    "message": (
                        f"{len(matching)} failed login attempts "
                        f"for user '{username}' within five minutes"
                    )
                })
                break

    return alerts


@app.get("/")
def dashboard(request: Request):
    records = get_login_records()
    alerts = detect_security_alerts(records)

    successful_logins = sum(
        1 for record in records
        if record["status"].lower() == "success"
    )

    failed_logins = sum(
        1 for record in records
        if record["status"].lower() == "failed"
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_logins": len(records),
            "successful_logins": successful_logins,
            "failed_logins": failed_logins,
            "alert_count": len(alerts),
            "alerts": alerts,
            "records": records
        }
    )


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/logins")
def read_login_records():
    records = get_login_records()
    return {
        "count": len(records),
        "records": records
    }


@app.get("/api/alerts")
def read_security_alerts():
    alerts = detect_security_alerts(get_login_records())
    return {
        "alert_count": len(alerts),
        "alerts": alerts
    }


@app.post("/api/test-login")
def create_test_login(username: str = "testuser",
                      status: str = "failed"):
    """Create a test login event for dashboard demonstrations."""

    if status.lower() not in ("success", "failed"):
        return {
            "error": "Status must be 'success' or 'failed'."
        }

    add_login_record(
        username=username,
        ip_address="192.168.1.100",
        status=status.lower()
    )

    return {
        "message": "Test login event added successfully",
        "username": username,
        "status": status.lower()
    }
