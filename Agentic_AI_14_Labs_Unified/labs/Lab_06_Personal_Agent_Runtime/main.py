"""
Lab 6: OpenCLA/OpenClaw-Style Runtime — Mini Personal Agent Runtime

Six components:
1. Interface
2. Runtime loop
3. Skill registry
4. Tools
5. Scoped memory
6. Audit log

This is a deterministic offline teaching implementation.
"""
from datetime import datetime


# ----- Tools -----------------------------------------------------------
def tool_word_count(text):
    return {"count": len(text.split())}


def tool_lookup_contact(name, contacts_db):
    return contacts_db.get(name, {"error": f"no contact found for {name}"})


TOOLS = {
    "word_count": tool_word_count,
    "lookup_contact": tool_lookup_contact,
}


# ----- Memory scoped per user -----------------------------------------
class Memory:
    def __init__(self):
        self._store = {}

    def scope(self, user):
        return self._store.setdefault(user, {})


# ----- Audit log -------------------------------------------------------
class Audit:
    def __init__(self):
        self.entries = []

    def log(self, task, skill_name, tool_calls, result=None, error=None):
        self.entries.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "task": task,
            "skill": skill_name,
            "tool_calls": tool_calls,
            "result": result,
            "error": error,
        })


# ----- Skills ----------------------------------------------------------
class SummarizeNotesSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        note_text = task.get("text", "")
        word_count = TOOLS["word_count"](note_text)
        self.tool_calls.append({
            "tool": "word_count",
            "input": {"text": note_text},
            "output": word_count,
        })
        self.memory_scope["last_note_length"] = word_count["count"]
        return f"Summary stub: note has {word_count['count']} words."


class DraftEmailSkill:
    CONTACTS = {
        "Dr. Meena": {"email": "meena@example.edu"}
    }

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        contact = TOOLS["lookup_contact"](task["to"], self.CONTACTS)
        self.tool_calls.append({
            "tool": "lookup_contact",
            "input": {"name": task["to"]},
            "output": contact,
        })

        if "error" in contact:
            raise RuntimeError(contact["error"])

        return f"Draft email to {contact['email']}: '{task['subject']}'"


class TranslateTextSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        # Translation is simulated to keep the lab fully offline.
        return f"[translated to {task['target_lang']}] {task['text']}"


SKILL_REGISTRY = {
    "summarize_notes": SummarizeNotesSkill,
    "draft_email": DraftEmailSkill,
}


# ----- Runtime core loop: keep this generic when adding skills --------
def select_skill(task):
    return task["skill"]


def run_task(task, user, memory, audit):
    skill_name = select_skill(task)
    if skill_name not in SKILL_REGISTRY:
        raise ValueError(f"unknown skill: {skill_name}")

    skill_class = SKILL_REGISTRY[skill_name]
    skill = skill_class(memory.scope(user))

    try:
        result = skill.execute(task)
        audit.log(task, skill_name, skill.tool_calls, result=result)
        return result
    except Exception as error:
        audit.log(task, skill_name, skill.tool_calls, error=str(error))
        raise


# ----- Interface: only entry point ------------------------------------
def receive_task(task, user, memory, audit):
    return run_task(task, user, memory, audit)


if __name__ == "__main__":
    memory, audit = Memory(), Audit()

    print("=== Successful run: summarize_notes ===")
    result = receive_task(
        {
            "skill": "summarize_notes",
            "text": "Agentic AI systems combine goals tools skills memory",
        },
        user="uday", memory=memory, audit=audit
    )
    print(result)

    print("\n=== Successful run: draft_email ===")
    result = receive_task(
        {
            "skill": "draft_email",
            "to": "Dr. Meena",
            "subject": "Lab guide review",
        },
        user="uday", memory=memory, audit=audit
    )
    print(result)

    print("\n=== Failing run: unknown contact ===")
    try:
        receive_task(
            {
                "skill": "draft_email",
                "to": "Unknown Person",
                "subject": "Hello",
            },
            user="uday", memory=memory, audit=audit
        )
    except RuntimeError as error:
        print(f"Run failed as expected: {error}")

    print("\n=== Register a third skill without changing runtime ===")
    SKILL_REGISTRY["translate_text"] = TranslateTextSkill
    result = receive_task(
        {
            "skill": "translate_text",
            "text": "Hello, team",
            "target_lang": "Kannada",
        },
        user="uday", memory=memory, audit=audit
    )
    print(result)

    print("\n=== Full audit log ===")
    for entry in audit.entries:
        print(entry)

    print("\n=== Scoped memory for user 'uday' ===")
    print(memory.scope("uday"))
