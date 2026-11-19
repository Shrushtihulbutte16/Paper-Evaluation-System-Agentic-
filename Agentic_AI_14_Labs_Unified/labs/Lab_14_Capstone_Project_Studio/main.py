"""Lab 14: Capstone Project Studio — Campus Help-Desk Agent.

Offline, deterministic classroom implementation of the guide's capstone example.
"""

from datetime import datetime

FAQ_DB = {
    "wifi": "Connect to 'Campus-Secure' and log in with your student ID.",
    "library": "The central library is open from 8:00 AM to 8:00 PM on weekdays.",
}
TICKET_DB = []


# ----------------------------- Tools ---------------------------------

def tool_search_faq(query):
    """Search the local FAQ. Returns found=False rather than inventing an answer."""
    query = query.lower()
    for keyword, answer in FAQ_DB.items():
        if keyword in query:
            return {"found": True, "answer": answer, "matched_keyword": keyword}
    return {"found": False}


def tool_create_ticket(issue):
    """Create an in-memory support ticket."""
    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"
    ticket = {"id": ticket_id, "issue": issue, "status": "open"}
    TICKET_DB.append(ticket)
    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    """Look up a ticket by its ID."""
    for ticket in TICKET_DB:
        if ticket["id"] == ticket_id:
            return ticket.copy()
    return {"error": "not found"}


# ----------------------------- Reusable skill -------------------------

def triage_skill(issue_text):
    """Search FAQ first; escalate only if no match exists.

    Constraint: never fabricate an FAQ answer.
    """
    faq_result = tool_search_faq(issue_text)
    if faq_result["found"]:
        return {"resolution": "faq", "answer": faq_result["answer"]}
    ticket = tool_create_ticket(issue_text)
    return {"resolution": "escalated", "ticket_id": ticket["ticket_id"]}


# ----------------------------- Memory --------------------------------

class CapstoneMemory:
    """Short-term session state plus a simple long-term interaction history."""

    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):
        entry = {
            "user": user,
            "issue": issue,
            "outcome": outcome,
            "date": datetime.now().isoformat(timespec="seconds"),
        }
        self.history.append(entry)
        self.session["last_issue"] = issue
        self.session["last_outcome"] = outcome


# ----------------------------- Node graph ----------------------------

def node_graph_run(user, issue, memory, audit_log, prompt_log):
    """intake -> safety check -> triage -> respond -> log."""
    prompt_log.append({"stage": "intake", "input": issue})

    # Safety control: reject empty input before calling any skill or tool.
    if not isinstance(issue, str) or not issue.strip():
        audit_log.append({"stage": "intake", "result": "rejected: empty issue"})
        return {"rejected": True, "reason": "empty issue text"}

    outcome = triage_skill(issue)
    prompt_log.append({"stage": "triage", "output": outcome})

    if outcome["resolution"] == "faq":
        response = outcome["answer"]
    else:
        response = (
            f"Ticket {outcome['ticket_id']} created; support will follow up."
        )

    memory.record(user, issue, outcome)
    audit_log.append({
        "stage": "complete",
        "user": user,
        "issue": issue,
        "outcome": outcome,
    })
    return {"rejected": False, "response": response, "outcome": outcome}


# ----------------------------- Evaluation ----------------------------

def run_evaluation():
    cases = [
        ("How do I connect to wifi?", "faq"),
        ("Where is the library?", "faq"),
        ("My laptop charger is broken", "escalated"),
        ("I cannot access the printer", "escalated"),
        ("", "rejected"),
    ]
    memory, audit_log, prompt_log = CapstoneMemory(), [], []
    results = []
    for issue, expected in cases:
        result = node_graph_run(
            "eval_user", issue, memory, audit_log, prompt_log
        )
        if result["rejected"]:
            actual = "rejected"
        else:
            actual = result["outcome"]["resolution"]
        results.append({
            "issue": issue,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
        })
    return results


def main():
    memory, audit_log, prompt_log = CapstoneMemory(), [], []

    print("=== Run 1: FAQ match ===")
    r1 = node_graph_run(
        "alice", "How do I connect to wifi on campus?",
        memory, audit_log, prompt_log
    )
    print(r1)

    print("\n=== Run 2: Escalation (no FAQ match) ===")
    r2 = node_graph_run(
        "bob", "My laptop charger is broken",
        memory, audit_log, prompt_log
    )
    print(r2)

    print("\n=== Run 3: Ticket status tool ===")
    ticket_id = r2["outcome"]["ticket_id"]
    print(tool_check_ticket_status(ticket_id))

    print("\n=== Run 4: Safety control rejects empty input ===")
    print(node_graph_run("carol", " ", memory, audit_log, prompt_log))

    print("\n=== Evaluation ===")
    results = run_evaluation()
    for item in results:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['issue']!r} -> {item['actual']} "
              f"(expected {item['expected']})")

    print("\n=== Prompt log ===")
    for item in prompt_log:
        print(item)

    print("\n=== Audit log ===")
    for item in audit_log:
        print(item)

    print("\n=== Long-term memory / history ===")
    for item in memory.history:
        print(item)

    print("\n=== Architecture / node graph ===")
    print("intake -> safety_check -> triage_skill -> respond -> memory/audit_log")
    print("Tools: tool_search_faq, tool_create_ticket, tool_check_ticket_status")
    print("Reusable skill: triage_skill")

    print("\n=== Limitations & next-step roadmap ===")
    print("- FAQ matching is keyword-based, not semantic.")
    print("- Tickets and memory are in-memory and reset when the process exits.")
    print("- No human approval workflow for high-priority incidents.")
    print("- Next: add retrieval-based FAQ search, priority classification, "
          "persistent storage, and human approval for critical tickets.")


if __name__ == "__main__":
    main()
