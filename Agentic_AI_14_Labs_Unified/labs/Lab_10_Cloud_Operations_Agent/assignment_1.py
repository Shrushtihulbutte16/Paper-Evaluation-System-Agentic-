"""
Lab 10 -- Assignment 1: A Second Incident Type

Adds a database connection-pool exhaustion incident with its own logs,
deployment history, and metrics. The shared severity and correlation
functions must produce a different diagnosis and severity.
"""

from main import (
    classify_severity,
    find_incident_start,
    correlate_with_recent_changes,
)

DB_LOGS = [
    {"ts": "15:00:00", "level": "INFO", "msg": "deploy started: database-service v3.2.0"},
    {"ts": "15:00:30", "level": "INFO", "msg": "deploy completed: database-service v3.2.0"},
    {"ts": "15:02:10", "level": "WARN", "msg": "database connection pool usage at 82 percent"},
    {"ts": "15:02:45", "level": "ERROR", "msg": "connection pool exhausted: acquire timeout"},
    {"ts": "15:03:05", "level": "ERROR", "msg": "connection pool exhausted: acquire timeout"},
]

DB_DEPLOY_HISTORY = [
    {
        "ts": "15:00:00",
        "service": "database-service",
        "version": "v3.2.0",
        "prev_version": "v3.1.4",
    },
]

DB_METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 0.8,
}


def main():
    incident_start = find_incident_start(DB_LOGS)
    severity = classify_severity(DB_METRICS)
    diagnosis = correlate_with_recent_changes(
        DB_LOGS,
        DB_DEPLOY_HISTORY,
        incident_start,
    )

    print("=== Database Connection-Pool Incident ===")
    print("incident_start:", incident_start)
    print("severity:", severity)
    print("diagnosis:", diagnosis["hypothesis"])
    print("affected_path:", diagnosis["affected_path"])
    print("suspect_deploy:", diagnosis["suspect_deploy"])

    assert severity == "early_warning"
    assert diagnosis["affected_path"] == "database connection pool"
    assert diagnosis["suspect_deploy"]["service"] == "database-service"
    print("\nCheck passed: database incident has a distinct diagnosis and severity.")


if __name__ == "__main__":
    main()
