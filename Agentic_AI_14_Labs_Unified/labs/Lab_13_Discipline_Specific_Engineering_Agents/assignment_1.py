"""Assignment 1 — Electrical Engineering: load forecasting and fault triage."""

POWER_LOG = [
    {"time": 0, "load_kw": 62, "voltage_v": 230},
    {"time": 1, "load_kw": 70, "voltage_v": 229},
    {"time": 2, "load_kw": 78, "voltage_v": 228},
    {"time": 3, "load_kw": 88, "voltage_v": 226},
    {"time": 4, "load_kw": 105, "voltage_v": 224},
]

LIMITS = {
    "load_warn_kw": 80,
    "load_alarm_kw": 100,
    "voltage_warn_low": 220,
}


def read_power_log():
    return POWER_LOG


def classify_load(reading):
    if reading["load_kw"] >= LIMITS["load_alarm_kw"]:
        return "ALARM"
    if (
        reading["load_kw"] >= LIMITS["load_warn_kw"]
        or reading["voltage_v"] < LIMITS["voltage_warn_low"]
    ):
        return "WARNING"
    return "NORMAL"


def estimate_next_load(log):
    """Simple last-step projection for demonstration, not a production forecast."""
    if len(log) < 2:
        return log[-1]["load_kw"]
    change = log[-1]["load_kw"] - log[-2]["load_kw"]
    return round(log[-1]["load_kw"] + change, 2)


def electrical_safety_gate(condition):
    if condition == "ALARM":
        return {
            "recommendation": "isolate_and_inspect_for_human_review",
            "auto_execute": False,
        }
    if condition == "WARNING":
        return {
            "recommendation": "alert_operator_and_review_load",
            "auto_execute": False,
        }
    return {"recommendation": "continue_monitoring", "auto_execute": True}


def electrical_load_agent():
    log = read_power_log()
    latest = log[-1]
    condition = classify_load(latest)
    safety = electrical_safety_gate(condition)
    return {
        "domain": "Electrical Engineering — Load Forecasting",
        "latest_reading": latest,
        "condition": condition,
        "estimated_next_load_kw": estimate_next_load(log),
        "recommended_action": safety["recommendation"],
        "auto_executed": safety["auto_execute"],
        "evaluation_method": (
            "Compare latest load and voltage against the illustrative limits; "
            "project the next load using the latest observed change."
        ),
    }


if __name__ == "__main__":
    result = electrical_load_agent()
    print("=== Electrical Load Agent Output ===")
    for key, value in result.items():
        print(f"{key}: {value}")
    assert result["condition"] != "ALARM" or result["auto_executed"] is False
    print("\nConfirmed: ALARM-level electrical recommendations require human review.")
