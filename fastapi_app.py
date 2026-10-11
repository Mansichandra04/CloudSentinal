
import ipaddress
import os
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, Query,Form
from fastapi.templating import Jinja2Templates

from cloudsentinel_data import get_login_records, add_login_record,verify_user


app = FastAPI(
    title="CloudSentinel",
    description="Cloud security monitoring and access audit system",
    version="1.0.0"
)


templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent / "templates")
)


def detect_security_alerts(records):
    """Detect repeated failed logins and suspicious multiple-IP activity."""
    failed_by_user = {}
    ips_by_user = {}

    for record in records:
        username = record["username"]
        ip_address = record["ip_address"]
        status = record["status"].lower()

        # Track IP addresses used by each username.
        ips_by_user.setdefault(username, set()).add(ip_address)

        # Group failed login events by username.
        if status == "failed":
            failed_by_user.setdefault(username, []).append(record)

    alerts = []

    # Rule 1: Five or more failed logins within five minutes.
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

    # Rule 2: One username seen from three or more IP addresses.
    for username, ip_addresses in ips_by_user.items():
        if len(ip_addresses) >= 3:
            alerts.append({
                "username": username,
                "severity": "MEDIUM",
                "ip_count": len(ip_addresses),
                "message": (
                    f"User '{username}' had login activity "
                    f"from {len(ip_addresses)} different IP addresses"
                )
            })

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


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


@app.post("/login")
def process_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    username = username.strip()

    if verify_user(username, password):
        add_login_record(
            username=username,
            ip_address=request.client.host if request.client else "unknown",
            status="success"
        )

        return {
            "message": "Login successful",
            "username": username
        }

    add_login_record(
        username=username,
        ip_address=request.client.host if request.client else "unknown",
        status="failed"
    )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Invalid username or password."},
        status_code=401
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
def create_test_login(
    username: str = Query(
        default="testuser",
        min_length=1,
        max_length=50
    ),
    status: str = Query(
        default="failed",
        pattern="^(success|failed)$"
    ),
    ip_address: str = Query(
        default="192.168.1.100",
        min_length=2,
        max_length=45
    )
):
    """Create a validated test login event."""
    if os.getenv("RENDER"):
        raise HTTPException(
            status_code=404,
            detail="Test login is disabled on the public website."
        )
    username = username.strip()
    status = status.lower()
    ip_address = ip_address.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty."
        )

    try:
        ip_address = str(ipaddress.ip_address(ip_address))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid IP address. Enter a valid IPv4 or IPv6 address."
        )

    add_login_record(
        username=username,
        ip_address=ip_address,
        status=status
    )

    return {
        "message": "Test login event added successfully",
        "username": username,
        "status": status,
        "ip_address": ip_address
    }
