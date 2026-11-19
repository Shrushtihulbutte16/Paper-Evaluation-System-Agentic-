"""
Assignment 2 — Escalate after two failures.

If the same skill fails twice in one session for the same user,
the third attempt is escalated to a human instead of executing again.

The decision is derived from the existing audit log; no separate
failure-counter state is maintained.
"""
from datetime import datetime


class Memory:
    def __init__(self):
        self._store = {}

    def scope(self, user):
        return self._store.setdefault(user, {})


class Audit:
    def __init__(self):
        self.entries = []

    def log(self, task, skill_name, tool_calls, user, result=None, error=None):
        self.entries.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "user": user,
            "task": task,
            "skill": skill_name,
            "tool_calls": tool_calls,
            "result": result,
            "error": error,
        })


class DraftEmailSkill:
    CONTACTS = {"Dr. Meena": {"email": "meena@example.edu"}}

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        contact = self.CONTACTS.get(
            task.get("to"),
            {"error": f"no contact found for {task.get('to', '<missing>')}"},
        )
        self.tool_calls.append({
            "tool": "lookup_contact",
            "input": {"name": task.get("to")},
            "output": contact,
        })

        if "error" in contact:
            raise RuntimeError(contact["error"])

        return f"Draft email to {contact['email']}: '{task['subject']}'"


SKILL_REGISTRY = {"draft_email": DraftEmailSkill}


def select_skill(task):
    return task["skill"]


def count_prior_failures(user, skill_name, audit):
    return sum(
        1 for entry in audit.entries
        if entry["user"] == user
        and entry["skill"] == skill_name
        and entry.get("error") is not None
    )


def run_task(task, user, memory, audit):
    skill_name = select_skill(task)
    if skill_name not in SKILL_REGISTRY:
        raise ValueError(f"unknown skill: {skill_name}")

    skill = SKILL_REGISTRY[skill_name](memory.scope(user))
    try:
        result = skill.execute(task)
        audit.log(task, skill_name, skill.tool_calls, user, result=result)
        return result
    except Exception as error:
        audit.log(task, skill_name, skill.tool_calls, user, error=str(error))
        raise


def receive_task(task, user, memory, audit):
    skill_name = select_skill(task)
    failures = count_prior_failures(user, skill_name, audit)

    if failures >= 2:
        escalation = {
            "escalated": True,
            "to": "human_support",
            "reason": (
                f"skill '{skill_name}' has already failed twice "
                f"for user '{user}' in this session"
            ),
        }
        # Record the escalation as a result, not as another skill failure.
        audit.entries.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "user": user,
            "task": task,
            "skill": skill_name,
            "tool_calls": [],
            "result": escalation,
            "error": None,
            "escalation": True,
        })
        return escalation

    return run_task(task, user, memory, audit)


if __name__ == "__main__":
    memory, audit = Memory(), Audit()

    failing_task = {
        "skill": "draft_email",
        "to": "Unknown Person",
        "subject": "Lab update",
    }

    for attempt in range(1, 4):
        print(f"\n=== Attempt {attempt} ===")
        try:
            result = receive_task(
                failing_task, user="alice", memory=memory, audit=audit
            )
            print(result)
        except RuntimeError as error:
            print(f"Skill failed: {error}")

    failures = count_prior_failures("alice", "draft_email", audit)
    assert failures == 2
    assert audit.entries[-1].get("escalation") is True
    print("\nPASS: two failures recorded; third attempt escalated without execution.")

    print("\n=== Audit log ===")
    for entry in audit.entries:
        print(entry)
