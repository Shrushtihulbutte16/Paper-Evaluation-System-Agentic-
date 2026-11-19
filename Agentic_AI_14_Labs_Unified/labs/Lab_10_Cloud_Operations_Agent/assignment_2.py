"""
Lab 10 -- Assignment 2: Safe Auto-Remediation Path

A warning-level incident proposes restart_single_pod, a low-risk action,
which this offline simulation marks as executed. Rollback remains high-risk
and always produces an approval request, never an execution result.
No real pod or infrastructure is touched.
"""

from main import (
    LOGS,
    DEPLOY_HISTORY,
    METRICS,
    classify_severity,
    find_incident_start,
    correlate_with_recent_changes,
    risk_level,
    draft_approval_request,
)


WARNING_LOGS = [
    {"ts": "16:00:00", "level": "INFO", "msg": "deployment healthy: catalog-service v1.8.2"},
    {"ts": "16:04:00", "level": "WARN", "msg": "one catalog pod is intermittently unhealthy"},
]

WARNING_DEPLOYS = [
    {
        "ts": "15:55:00",
        "service": "catalog-service",
        "version": "v1.8.2",
        "prev_version": "v1.8.1",
    },
]

WARNING_METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 0.7,
}


def handle_action(action, hypothesis, urgency_prompt=False):
    """Execute only low-risk simulated actions; gate high-risk actions."""
    risk = risk_level(action)

    if risk == "low":
        return {
            "risk": risk,
            "action_executed": action,
            "note": "Low-risk action allowed by policy in this local simulation.",
        }

    if risk == "high":
        suspect = hypothesis["suspect_deploy"]
        if suspect is None:
            rollback_plan = "Verify a known-good version before any rollback."
        else:
            rollback_plan = (
                f"Revert to {suspect['prev_version']}; verify service health "
                f"before considering {suspect['version']} again."
            )

        request = draft_approval_request(
            hypothesis,
            action,
            rollback_plan,
        )
        if urgency_prompt:
            request["note"] = (
                "Urgency does not bypass human approval for high-risk actions."
            )
        return {
            "risk": risk,
            **request,
        }

    return {
        "risk": "unknown",
        "status": "BLOCKED -- unknown action risk; human review required",
    }


def main():
    warning_severity = classify_severity(WARNING_METRICS)
    warning_start = find_incident_start(WARNING_LOGS)
    warning_hypothesis = correlate_with_recent_changes(
        WARNING_LOGS,
        WARNING_DEPLOYS,
        warning_start,
    )

    print("=== Warning-level low-risk scenario ===")
    print("severity:", warning_severity)
    print("action result:", handle_action(
        "restart_single_pod",
        warning_hypothesis,
    ))

    low_result = handle_action("restart_single_pod", warning_hypothesis)
    assert warning_severity == "early_warning"
    assert low_result["action_executed"] == "restart_single_pod"

    print("\n=== Rollback safety check ===")
    rollback_hypothesis = correlate_with_recent_changes(
        LOGS,
        DEPLOY_HISTORY,
        find_incident_start(LOGS),
    )
    rollback_result = handle_action(
        "rollback",
        rollback_hypothesis,
        urgency_prompt=True,
    )
    print(rollback_result)

    assert rollback_result["risk"] == "high"
    assert "action_executed" not in rollback_result
    assert rollback_result["status"].startswith("AWAITING HUMAN APPROVAL")
    print("\nChecks passed: low-risk action is simulated as executed; rollback remains approval-gated.")


if __name__ == "__main__":
    main()
