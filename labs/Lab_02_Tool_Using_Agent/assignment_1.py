"""
Lab 2 — Assignment 1: Add a Notification Tool with Justified Use

The notification tool drafts a message only; it never sends anything.
If the average event sign-ups fall below the configured threshold,
the assistant calls the tool and records why it was needed.
"""

from main import (
    CampusDataAssistant,
    SIGNUPS_CSV,
    read_csv,
    calculator,
    mock_events_api,
)
import json


def send_notification(message):
    """Draft a notification without sending it."""
    return {
        "status": "drafted",
        "message": message,
        "sent": False,
    }


class NotificationCampusAssistant(CampusDataAssistant):
    def __init__(self, threshold=13):
        super().__init__()
        self.threshold = threshold
        self.tools = {
            "calculator": calculator,
            "read_csv": read_csv,
            "events_api": mock_events_api,
            "send_notification": send_notification,
        }

    def _call(self, tool_name, reason, **kwargs):
        if tool_name not in self.tools:
            raise ValueError(f"unknown tool: {tool_name}")

        result = self.tools[tool_name](**kwargs)
        self.trace.append({
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result,
        })

        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"{tool_name} failed: {result['error']}")

        return result

    def answer_signup_question(self):
        csv_result = self._call(
            "read_csv",
            "signup totals and averages must be read from the CSV export",
        )
        values = [int(row["signups"]) for row in csv_result["rows"]]

        total = self._call(
            "calculator",
            "calculate total sign-ups from the extracted CSV values",
            operation="sum",
            values=values,
        )
        average = self._call(
            "calculator",
            "calculate average sign-ups to compare against the alert threshold",
            operation="average",
            values=values,
        )

        avg_value = average["result"]
        notification_text = "No notification required."

        if avg_value < self.threshold:
            notification = self._call(
                "send_notification",
                (
                    f"average sign-ups ({avg_value:.2f}) are below "
                    f"the configured threshold ({self.threshold})"
                ),
                message=(
                    f"Low turnout notice: average event sign-ups are "
                    f"{avg_value:.2f}, below the threshold of {self.threshold}."
                ),
            )
            notification_text = (
                f"Notification {notification['status']}; "
                f"sent={notification['sent']}."
            )

        return (
            f"Total sign-ups: {total['result']}. "
            f"Average per event: {avg_value:.2f}. "
            f"{notification_text}"
        )


if __name__ == "__main__":
    # The guide's sample data averages 12.33. A threshold of 13
    # makes the low-turnout branch observable without changing the data.
    assistant = NotificationCampusAssistant(threshold=13)

    question = "How many students signed up for events, and what's the average?"
    print("Q:", question)
    print("A:", assistant.answer_signup_question())

    print("\n=== Tool trace, including notification justification ===")
    for index, entry in enumerate(assistant.trace, 1):
        print(f"{index}. tool={entry['tool']}")
        print(f"   reason={entry['reason']}")
        print(f"   input={entry['input']}")
        print(f"   output={entry['output']}")

    print("\nNotification is a draft only; no message was sent.")
