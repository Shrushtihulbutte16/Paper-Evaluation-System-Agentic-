"""
Lab 10: Cloud Operations Agent -- Failed Deployment Diagnosis

Observe -> Reason -> Act.
The agent inspects logs and metrics, correlates an incident with a recent
deployment, classifies severity, and drafts an approval request for rollback.
No real infrastructure is contacted or changed.
"""

LOGS = [
    {"ts": "14:00:00", "level": "INFO", "msg": "deploy started: payments-service v2.4.1"},
    {"ts": "14:00:45", "level": "INFO", "msg": "deploy completed: payments-service v2.4.1"},
    {"ts": "14:03:10", "level": "WARN", "msg": "refund endpoint latency elevated"},
    {"ts": "14:03:40", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
    {"ts": "14:04:05", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
    {"ts": "14:04:30", "level": "ERROR", "msg": "refund endpoint: NullPointerException in RefundHandler"},
]

DEPLOY_HISTORY = [
    {
        "ts": "14:00:00",
        "service": "payments-service",
        "version": "v2.4.1",
        "prev_version": "v2.4.0",
    },
]

METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 1.6,
}  # percentages


def classify_severity(metrics):
    """Classify incident using current error rate and baseline ratio."""
    baseline = metrics["baseline_error_rate"]
    current = metrics["current_error_rate"]

    if baseline <= 0:
        raise ValueError("baseline_error_rate must be greater than zero")

    ratio = current / baseline
    if current > 50:
        return "down"
    if ratio >= 2:
        return "degraded"
    return "early_warning"


def find_incident_start(logs):
    """Return timestamp of the first ERROR entry."""
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]
    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    """Build a root-cause hypothesis from error messages and deploy timing."""
    error_msgs = [
        entry["msg"] for entry in logs
        if entry["level"] == "ERROR"
    ]
    joined = " ".join(error_msgs).lower()

    if "refund" in joined:
        affected_path = "refund"
    elif "connection pool" in joined or "connection-pool" in joined:
        affected_path = "database connection pool"
    else:
        affected_path = "unknown"

    for deploy in deploys:
        if (
            incident_start is not None
            and deploy["ts"] < incident_start
        ):
            return {
                "hypothesis": (
                    f"Errors began at {incident_start}, after the "
                    f"{deploy['ts']} deployment of {deploy['service']} "
                    f"{deploy['version']}. Errors are concentrated in the "
                    f"{affected_path} path, consistent with a regression "
                    "introduced in that release."
                ),
                "suspect_deploy": deploy,
                "affected_path": affected_path,
            }

    return {
        "hypothesis": "No recent deployment correlates with the incident window.",
        "suspect_deploy": None,
        "affected_path": affected_path,
    }


def risk_level(action):
    high_risk = {"rollback", "scale", "config_change", "delete"}
    low_risk = {"open_ticket", "notify", "restart_single_pod"}

    if action in high_risk:
        return "high"
    if action in low_risk:
        return "low"
    return "unknown"


def draft_approval_request(hypothesis, action, rollback_plan):
    return {
        "diagnosis": hypothesis["hypothesis"],
        "proposed_action": action,
        "risk_if_wrong": (
            "Brief service interruption (~30 seconds) during rollback "
            "if the root-cause hypothesis is incorrect."
        ),
        "rollback_plan": rollback_plan,
        "status": "AWAITING HUMAN APPROVAL -- NOT EXECUTED",
    }


def diagnose_and_propose(logs, deploys, metrics, urgency_prompt=False):
    severity = classify_severity(metrics)
    incident_start = find_incident_start(logs)
    hypothesis = correlate_with_recent_changes(logs, deploys, incident_start)

    proposed_action = "rollback"
    risk = risk_level(proposed_action)

    if risk == "high":
        suspect = hypothesis["suspect_deploy"]
        if suspect is None:
            rollback_plan = "Identify and verify the last known-good version before rollback."
        else:
            rollback_plan = (
                f"Revert to {suspect['prev_version']}; if that also errors, "
                f"re-deploy {suspect['version']}."
            )

        request = draft_approval_request(
            hypothesis,
            proposed_action,
            rollback_plan,
        )

        if urgency_prompt:
            request["note"] = (
                "Urgency noted, but high-risk action still requires human "
                "approval; the approval gate is not bypassed."
            )

        return {
            "severity": severity,
            "incident_start": incident_start,
            "affected_service": (
                hypothesis["suspect_deploy"]["service"]
                if hypothesis["suspect_deploy"] else "unknown"
            ),
            "immediate_mitigation": "Monitor error rate and prepare incident communication.",
            "long_term_fix": "Inspect the implicated code path and add regression coverage.",
            **request,
        }

    # This branch is not used by the reference rollback scenario.
    return {
        "severity": severity,
        "incident_start": incident_start,
        "action_executed": proposed_action,
    }


def main():
    result = diagnose_and_propose(
        LOGS,
        DEPLOY_HISTORY,
        METRICS,
        urgency_prompt=True,
    )

    print("=== Diagnostic + Approval Request ===")
    for key, value in result.items():
        print(f"{key}: {value}")

    assert "action_executed" not in result, (
        "High-risk rollback must never auto-execute."
    )
    assert result["status"].startswith("AWAITING HUMAN APPROVAL")
    print("\nConfirmed: no destructive action was executed automatically.")


if __name__ == "__main__":
    main()
