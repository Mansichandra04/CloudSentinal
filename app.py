
from flask import Flask, render_template_string
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE = "cloudsentinel.db"


def get_database_connection():
    """Create a connection to the CloudSentinel database."""
    connection = sqlite3.connect(DATABASE)
    return connection


@app.route("/")
def dashboard():
    """Display login activity and suspicious login alerts."""

    connection = get_database_connection()
    cursor = connection.cursor()

    # Get all login records, with the newest events first.
    cursor.execute("""
        SELECT username, ip_address, status, event_time
        FROM login_logs
        ORDER BY event_time DESC
    """)
    records = cursor.fetchall()

    # Count all failed login attempts.
    cursor.execute("""
        SELECT COUNT(*)
        FROM login_logs
        WHERE status = 'Failed'
    """)
    failed_total = cursor.fetchone()[0]

    # Get failed login events and their timestamps.
    cursor.execute("""
        SELECT username, event_time
        FROM login_logs
        WHERE status = 'Failed'
        ORDER BY event_time
    """)
    failed_events = cursor.fetchall()

    connection.close()

    # Group failed login timestamps by username.
    failed_by_user = {}

    for username, event_time in failed_events:
        timestamp = datetime.fromisoformat(event_time)

        if username not in failed_by_user:
            failed_by_user[username] = []

        failed_by_user[username].append(timestamp)

    # Detect 5 or more failures within a 5-minute window.
    alerts = []
    threshold = 5
    window = timedelta(minutes=5)

    for username, timestamps in failed_by_user.items():
        timestamps.sort()

        for start in range(len(timestamps)):
            count = 1

            for end in range(start + 1, len(timestamps)):
                if timestamps[end] - timestamps[start] <= window:
                    count += 1
                else:
                    break

            if count >= threshold:
                alerts.append((username, count))
                break

    # Dashboard HTML.
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>CloudSentinel Dashboard</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f7fb;
                margin: 0;
                padding: 30px;
                color: #1f2937;
            }

            .container {
                max-width: 1100px;
                margin: auto;
            }

            h1 {
                color: #163a70;
                margin-bottom: 5px;
            }

            .subtitle {
                color: #64748b;
                margin-bottom: 25px;
            }

            .cards {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                margin-bottom: 25px;
            }

            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
                flex: 1;
                min-width: 180px;
            }

            .card h3 {
                margin-top: 0;
                color: #64748b;
                font-size: 15px;
            }

            .number {
                font-size: 30px;
                font-weight: bold;
                color: #163a70;
            }

            .section {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 25px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }

            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
                white-space: nowrap;
            }

            th {
                background-color: #f8fafc;
            }

            .failed {
                color: #b91c1c;
                font-weight: bold;
            }

            .success {
                color: #15803d;
                font-weight: bold;
            }

            .alert {
                background: #fff1f2;
                border-left: 5px solid #dc2626;
                padding: 14px;
                margin-top: 12px;
                border-radius: 5px;
            }

            .safe {
                background: #ecfdf5;
                border-left: 5px solid #16a34a;
                padding: 14px;
                margin-top: 12px;
                border-radius: 5px;
            }

            .footer {
                color: #64748b;
                font-size: 13px;
                text-align: center;
                margin-top: 25px;
            }

            @media (max-width: 600px) {
                body {
                    padding: 15px;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>CloudSentinel</h1>
            <p class="subtitle">
                Cloud Security Monitoring and Access Audit Dashboard
            </p>

            <div class="cards">
                <div class="card">
                    <h3>Total Login Records</h3>
                    <div class="number">{{ records|length }}</div>
                </div>

                <div class="card">
                    <h3>Failed Login Attempts</h3>
                    <div class="number">{{ failed_total }}</div>
                </div>

                <div class="card">
                    <h3>Suspicious Users</h3>
                    <div class="number">{{ alerts|length }}</div>
                </div>
            </div>

            <div class="section">
                <h2>Security Alerts</h2>

                {% if alerts %}
                    {% for username, count in alerts %}
                        <div class="alert">
                            <strong>Suspicious activity detected!</strong><br>
                            User <strong>{{ username }}</strong> had
                            {{ count }} failed login attempts within a
                            five-minute window.
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="safe">
                        No suspicious login patterns detected.
                    </div>
                {% endif %}
            </div>

            <div class="section">
                <h2>Recent Login Activity</h2>

                {% if records %}
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Username</th>
                                <th>IP Address</th>
                                <th>Status</th>
                            </tr>
                        </thead>

                        <tbody>
                            {% for record in records %}
                                <tr>
                                    <td>{{ record[3] }}</td>
                                    <td>{{ record[0] }}</td>
                                    <td>{{ record[1] }}</td>
                                    <td class="{% if record[2] == 'Failed' %}failed{% else %}success{% endif %}">
                                        {{ record[2] }}
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p>No login records found in the database.</p>
                {% endif %}
            </div>

            <p class="footer">
                CloudSentinel | Python · Flask · SQLite
            </p>

        </div>
    </body>
    </html>
    """

    return render_template_string(
        html,
        records=records,
        failed_total=failed_total,
        alerts=alerts
    )


if __name__ == "__main__":
    app.run(debug=True)
