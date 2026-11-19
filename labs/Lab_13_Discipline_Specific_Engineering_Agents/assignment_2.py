"""Assignment 2 — Escalate after three consecutive WARNING readings."""

from main import THRESHOLDS, classify_condition

# All vibration values remain below the ALARM threshold (4.5 mm/s).
# Three consecutive readings are WARNING-level and steadily increasing.
MODIFIED_SENSOR_LOG = [
    {"t": 0, "vibration_mm_s": 1.8, "temp_c": 61},
    {"t": 1, "vibration_mm_s": 2.0, "temp_c": 63},
    {"t": 2, "vibration_mm_s": 2.9, "temp_c": 65},
    {"t": 3, "vibration_mm_s": 3.2, "temp_c": 66},
    {"t": 4, "vibration_mm_s": 3.7, "temp_c": 68},
]


def recommend_from_trend(sensor_log):
    conditions = [classify_condition(reading) for reading in sensor_log]
    consecutive_warnings = 0

    for condition in reversed(conditions):
        if condition == "WARNING":
            consecutive_warnings += 1
        else:
            break

    latest = sensor_log[-1]
    if conditions[-1] == "ALARM":
        action = "recommend_shutdown_for_human_review"
        auto_execute = False
    elif consecutive_warnings >= 3:
        action = "schedule_inspection"
        auto_execute = False
    else:
        action = "continue_monitoring"
        auto_execute = False

    return {
        "conditions": conditions,
        "latest_vibration_mm_s": latest["vibration_mm_s"],
        "consecutive_warning_readings": consecutive_warnings,
        "recommended_action": action,
        "auto_executed": auto_execute,
        "all_readings_below_alarm": all(
            item["vibration_mm_s"] < THRESHOLDS["vibration_alarm"]
            and item["temp_c"] < THRESHOLDS["temp_alarm"]
            for item in sensor_log
        ),
    }


if __name__ == "__main__":
    result = recommend_from_trend(MODIFIED_SENSOR_LOG)
    print("=== Trend-Based Mechanical Maintenance Escalation ===")
    for key, value in result.items():
        print(f"{key}: {value}")

    assert result["consecutive_warning_readings"] == 3
    assert result["all_readings_below_alarm"] is True
    assert result["recommended_action"] == "schedule_inspection"
    print("\nConfirmed: three consecutive WARNING readings trigger inspection.")
