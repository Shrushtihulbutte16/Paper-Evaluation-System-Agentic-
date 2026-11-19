"""
Assignment 2 — Memory retention and staleness.

Warn before using a memory record older than retention_days.
The demonstration uses a fixed reference date so the output is
repeatable on every machine.
"""
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str
    source: str = "memory"


class ProjectMemory:
    def __init__(self, retention_days=90):
        self.records = []
        self.retention_days = retention_days

    def write(self, record):
        self.records.append(record)

    def retrieve(self, topic):
        return [r for r in self.records if r.topic == topic]

    def is_stale(self, record, today=None):
        today = today or date.today()
        stored_on = datetime.strptime(record.date, "%Y-%m-%d").date()
        age_days = (today - stored_on).days
        return age_days > self.retention_days, age_days


def answer(memory, topic, today=None):
    hits = memory.retrieve(topic)
    if not hits:
        return "[no supported source] No stored decision found."

    record = hits[-1]
    stale, age_days = memory.is_stale(record, today)

    if stale:
        return (
            f"[stale memory warning] This decision is {age_days} days old "
            f"(retention limit: {memory.retention_days} days): '{record.fact}'. "
            "Verify with the team before relying on it."
        )

    return (
        f"[{record.source}, dated {record.date}] "
        f"{record.fact} (age: {age_days} days)"
    )


if __name__ == "__main__":
    reference_today = date(2026, 11, 13)
    memory = ProjectMemory(retention_days=90)

    memory.write(MemoryRecord(
        "database", "The project uses PostgreSQL.", "2026-11-01"
    ))
    memory.write(MemoryRecord(
        "hosting", "The old prototype used Heroku.", "2026-06-01"
    ))

    print("=== Fresh memory ===")
    fresh = answer(memory, "database", today=reference_today)
    print(fresh)
    assert "stale memory warning" not in fresh

    print("\n=== Old memory ===")
    old = answer(memory, "hosting", today=reference_today)
    print(old)
    assert "stale memory warning" in old
    assert "Verify with the team" in old

    print("\nPASS: fresh memory is usable; stale memory is flagged.")
