"""
Lab 4: Memory and Retrieval — Multi-Session Project Assistant

Demonstrates:
- Short-term current session state
- Long-term, source-tagged project memory
- Topic-scoped retrieval
- Conflict detection before updating stored decisions
- Permission-gated memory writes

This is a deterministic offline reference implementation.
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str
    source: str = "memory"


class ProjectMemory:
    def __init__(self):
        self.records = []
        self.allowed_writers = {"team_lead"}

    def retrieve(self, topic):
        """Return only records belonging to the requested topic."""
        return [record for record in self.records if record.topic == topic]

    def write(self, record, user_role):
        """Only authorized roles can add long-term memories."""
        if user_role not in self.allowed_writers:
            raise PermissionError(
                f"role '{user_role}' is not permitted to write memory"
            )
        self.records.append(record)


class ProjectAssistant:
    def __init__(self, memory):
        self.memory = memory
        self.session_facts = {}

    def set_session_fact(self, topic, fact):
        """Store information that is valid only in the current session."""
        self.session_facts[topic] = fact

    def answer(self, topic, question):
        # Current session state takes precedence, but its source is explicit.
        if topic in self.session_facts:
            return f"[current session] {self.session_facts[topic]}"

        hits = self.memory.retrieve(topic)
        if not hits:
            return (
                f"[no supported source] No stored decision on '{topic}'. "
                f"Question: {question}"
            )

        latest = hits[-1]
        return (
            f"[{latest.source}, dated {latest.date}] "
            f"Per the stored decision: {latest.fact}"
        )

    def receive_statement(self, topic, new_fact, user_role):
        """Flag conflicting statements; do not silently overwrite memory."""
        hits = self.memory.retrieve(topic)

        if hits and hits[-1].fact.strip().casefold() != new_fact.strip().casefold():
            return {
                "conflict": True,
                "stored": hits[-1].fact,
                "stored_date": hits[-1].date,
                "new": new_fact,
                "message": (
                    f"Conflict: stored decision from {hits[-1].date} is "
                    f"'{hits[-1].fact}', but the new statement is '{new_fact}'. "
                    "Confirm the change with an authorized team lead."
                ),
                "written": False,
            }

        record = MemoryRecord(
            topic=topic,
            fact=new_fact,
            date=str(date.today()),
        )
        self.memory.write(record, user_role)
        return {
            "conflict": False,
            "message": f"Recorded: {new_fact}",
            "written": True,
        }


if __name__ == "__main__":
    memory = ProjectMemory()
    memory.write(
        MemoryRecord(
            topic="database",
            fact="We chose PostgreSQL",
            date="2026-07-03",
        ),
        user_role="team_lead",
    )

    assistant = ProjectAssistant(memory)

    print("=== Initial retrieval ===")
    print(assistant.answer("database", "What database did we choose?"))

    print("\n=== Current session state is tagged separately ===")
    assistant.set_session_fact("deadline", "The demo is scheduled for Friday.")
    print(assistant.answer("deadline", "When is the demo?"))

    print("\n=== Topic with no stored decision ===")
    print(assistant.answer("hosting", "Which hosting provider did we choose?"))

    print("\n=== A team member proposes a conflicting change ===")
    proposal = assistant.receive_statement(
        "database", "We are switching to SQLite", user_role="member"
    )
    print(proposal["message"])

    print("\n=== Team lead confirms the change ===")
    memory.write(
        MemoryRecord(
            topic="database",
            fact="We are switching to SQLite",
            date=str(date.today()),
        ),
        user_role="team_lead",
    )
    print("Write permitted: memory updated by team_lead.")

    print("\n=== Unauthorized write attempt ===")
    try:
        memory.write(
            MemoryRecord("database", "Switch to MongoDB", str(date.today())),
            user_role="member",
        )
    except PermissionError as error:
        print(f"Blocked as expected: {error}")

    print("\n=== Final answer after confirmed update ===")
    print(assistant.answer("database", "What database did we choose?"))
