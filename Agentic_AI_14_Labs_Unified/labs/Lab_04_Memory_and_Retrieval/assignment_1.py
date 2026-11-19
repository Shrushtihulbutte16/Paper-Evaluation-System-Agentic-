"""
Assignment 1 — Topic-scoped retrieval.

Add a second topic (hosting) and prove that asking about the database
does not accidentally return the hosting decision, and vice versa.
"""
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str
    source: str = "memory"


class ProjectMemory:
    def __init__(self):
        self.records = []

    def write(self, record):
        self.records.append(record)

    def retrieve(self, topic):
        return [r for r in self.records if r.topic == topic]


def answer(memory, topic):
    hits = memory.retrieve(topic)
    if not hits:
        return f"[no supported source] No memory found for '{topic}'."
    latest = hits[-1]
    return f"[{latest.source}, dated {latest.date}] {latest.fact}"


if __name__ == "__main__":
    memory = ProjectMemory()
    memory.write(MemoryRecord(
        "database", "The project uses PostgreSQL.", "2026-07-03"
    ))
    memory.write(MemoryRecord(
        "hosting", "The demo is hosted on Render.", "2026-07-04"
    ))

    print("=== Database question ===")
    database_answer = answer(memory, "database")
    print(database_answer)

    print("\n=== Hosting question ===")
    hosting_answer = answer(memory, "hosting")
    print(hosting_answer)

    print("\n=== Scope validation ===")
    assert "PostgreSQL" in database_answer
    assert "Render" not in database_answer
    assert "Render" in hosting_answer
    assert "PostgreSQL" not in hosting_answer
    print("PASS: database and hosting facts remain isolated.")

    print("\n=== Unknown topic ===")
    unknown_answer = answer(memory, "deployment")
    print(unknown_answer)
    assert "No memory found" in unknown_answer
