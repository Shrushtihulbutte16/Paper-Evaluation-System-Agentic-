# Lab 4 — Memory and Retrieval

## Objective
Build a multi-session project assistant that separates current session state from long-term stored memory, retrieves only relevant facts, tags every answer with its source, detects conflicting updates, and controls who can write memory.

## Folder contents
- `main.py` — complete reference implementation.
- `assignment_1.py` — topic-scoped retrieval for separate database and hosting decisions.
- `assignment_2.py` — retention policy and stale-memory warnings.
- `test_output.txt` — captured output from all three programs.

## Requirements
- Python 3.10+
- No third-party packages
- No API keys or internet connection

## Run in VS Code terminal
Open this folder in VS Code, then run:

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Core concepts
1. **Short-term memory:** `session_facts` holds facts for the active session.
2. **Long-term memory:** `MemoryRecord` stores `topic`, `fact`, `date`, and `source`.
3. **Scoped retrieval:** `retrieve(topic)` returns only records for that topic.
4. **Conflict detection:** a changed fact is flagged instead of silently replacing the old decision.
5. **Write permissions:** only `team_lead` can write to long-term memory in the reference implementation.
6. **Staleness:** Assignment 2 warns when a record exceeds the configured retention period.

## Important design note
The reference implementation stores records in an in-memory Python list. It does not persist data after the process exits. A database or file-backed store can be added in a later integration stage.

## Expected learning outcome
You should be able to explain why an agent must distinguish current session context from stored decisions, why retrieval should be scoped, and why stale or conflicting memory should be surfaced rather than treated as unquestionable truth.
