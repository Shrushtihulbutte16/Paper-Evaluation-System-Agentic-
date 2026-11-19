"""Lab 14 — Assignment 1: Add a second reusable skill.

Adds password-reset guidance with explicit instructions and constraints,
then routes matching issues to that skill from the graph's triage stage.
"""

from datetime import datetime

FAQ_DB = {
    "wifi": "Connect to 'Campus-Secure' and log in with your student ID."
}
TICKET_DB = []


def tool_search_faq(query):
    for keyword, answer in FAQ_DB.items():
        if keyword in query.lower():
            return {"found": True, "answer": answer}
    return {"found": False}


def tool_create_ticket(issue):
    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"
    TICKET_DB.append({"id": ticket_id, "issue": issue, "status": "open"})
    return {"ticket_id": ticket_id}


def password_reset_skill(issue_text):
    """Give safe password-reset steps.

    Constraint: never ask the user to share their current password or OTP.
    """
    return {
        "resolution": "password_guidance",
        "answer": (
            "Open the university account portal, choose 'Forgot Password', "
            "verify using your registered email or phone, and create a new "
            "unique password. Never share your password or OTP with anyone."
        ),
    }


def triage_skill(issue_text):
    """Default skill: FAQ first, then ticket escalation; never invent answers."""
    faq = tool_search_faq(issue_text)
    if faq["found"]:
        return {"resolution": "faq", "answer": faq["answer"]}
    ticket = tool_create_ticket(issue_text)
    return {"resolution": "escalated", "ticket_id": ticket["ticket_id"]}


class CapstoneMemory:
    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):
        self.history.append({
            "user": user, "issue": issue, "outcome": outcome,
            "date": datetime.now().isoformat(timespec="seconds"),
        })
        self.session["last_issue"] = issue


def node_graph_run(user, issue, memory, audit_log, prompt_log):
    prompt_log.append({"stage": "intake", "input": issue})
    if not isinstance(issue, str) or not issue.strip():
        audit_log.append({"stage": "intake", "result": "rejected: empty issue"})
        return {"rejected": True, "reason": "empty issue text"}

    # Routing decision: password-reset issues use the new skill.
    if "password" in issue.lower() or "reset" in issue.lower():
        outcome = password_reset_skill(issue)
        selected_skill = "password_reset_skill"
    else:
        outcome = triage_skill(issue)
        selected_skill = "triage_skill"

    prompt_log.append({
        "stage": "triage",
        "selected_skill": selected_skill,
        "output": outcome,
    })
    response = (
        outcome["answer"] if "answer" in outcome
        else f"Ticket {outcome['ticket_id']} created; support will follow up."
    )
    memory.record(user, issue, outcome)
    audit_log.append({
        "stage": "complete", "user": user, "skill": selected_skill,
        "issue": issue, "outcome": outcome,
    })
    return {
        "rejected": False, "selected_skill": selected_skill,
        "response": response, "outcome": outcome,
    }


def main():
    memory, audit_log, prompt_log = CapstoneMemory(), [], []
    print("=== Assignment 1: Two-skill routing ===")
    for user, issue in [
        ("alice", "I forgot my password and need a reset"),
        ("bob", "How do I connect to campus wifi?"),
        ("carol", "My laptop battery is damaged"),
    ]:
        result = node_graph_run(user, issue, memory, audit_log, prompt_log)
        print(f"\nIssue: {issue}")
        print(f"Selected skill: {result.get('selected_skill')}")
        print(f"Response: {result.get('response', result.get('reason'))}")

    print("\n=== Prompt / routing trace ===")
    for entry in prompt_log:
        print(entry)
    print("\n=== Audit trace ===")
    for entry in audit_log:
        print(entry)

    assert prompt_log[1]["selected_skill"] == "password_reset_skill"
    assert prompt_log[3]["selected_skill"] == "triage_skill"
    print("\nBoth reusable skills were routed and executed successfully.")


if __name__ == "__main__":
    main()
