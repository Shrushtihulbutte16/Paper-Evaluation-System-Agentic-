"""
Assignment 1 — Per-user rate limiting.

Each user may run at most three tasks in one session.
The limit is enforced in receive_task, without changing run_task.
The audit log is used to count completed/failed attempts per user.
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


class WordCountSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        count = len(task.get("text", "").split())
        output = {"count": count}
        self.tool_calls.append({"tool": "word_count", "output": output})
        self.memory_scope["last_note_length"] = count
        return f"Word count: {count}"


SKILL_REGISTRY = {"word_count": WordCountSkill}


def select_skill(task):
    return task["skill"]


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
    # Count only this user's task records; other users have separate quotas.
    user_task_count = sum(
        1 for entry in audit.entries
        if entry["user"] == user and entry.get("kind") != "rate_limit_rejection"
    )

    if user_task_count >= 3:
        return {
            "rejected": True,
            "reason": "session task limit reached (maximum 3 tasks per user)",
        }

    return run_task(task, user, memory, audit)


if __name__ == "__main__":
    memory, audit = Memory(), Audit()

    for number in range(1, 5):
        print(f"\n=== Task {number} for user alice ===")
        result = receive_task(
            {"skill": "word_count", "text": f"Task number {number}"},
            user="alice", memory=memory, audit=audit
        )
        print(result)

    print("\n=== Another user has an independent quota ===")
    print(receive_task(
        {"skill": "word_count", "text": "Bob can still run a task"},
        user="bob", memory=memory, audit=audit
    ))

    assert len([e for e in audit.entries if e["user"] == "alice"]) == 3
    assert "rejected" in result and result["rejected"]
    print("\nPASS: fourth task rejected; other user's quota unaffected.")
