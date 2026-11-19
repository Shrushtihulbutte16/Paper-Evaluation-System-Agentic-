# Lab 6 — OpenCLA/OpenClaw-Style Runtime: Mini Personal Agent Runtime

## Objective
Build a small personal-agent runtime with six components:
1. Interface
2. Runtime loop
3. Skill registry
4. Tools
5. Scoped memory
6. Audit log

## Files
- `main.py` — reference implementation with note summarization, email drafting, translation stub, user-scoped memory, and audit logging.
- `assignment_1.py` — per-user maximum of three tasks per session.
- `assignment_2.py` — escalate to a human after two failures of the same skill for the same user.
- `test_output.txt` — captured output from all three programs.

## Requirements
- Python 3.10+
- No third-party packages
- No API keys or internet connection

## Run in VS Code terminal

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Important design concepts
- **Skill registry:** maps a skill name to a skill class. New skills can be registered without editing the runtime dispatch loop.
- **Tools:** small functions called by skills to perform specific operations.
- **Scoped memory:** `memory.scope(user)` gives each user a separate memory dictionary.
- **Audit log:** records task, skill, tool calls, result, error, and timestamp.
- **Interface:** `receive_task` is the entry point that delegates to the runtime.
- **Runtime:** `run_task` selects and executes the requested skill, then records success or failure.

## Assignment 1
The formal guide asks for a maximum of three tasks per user per session. The check is placed in `receive_task`, leaving `run_task`'s signature and skill dispatch unchanged. Task counts are derived from the audit entries.

## Assignment 2
The formal guide asks for escalation after two failures of the same skill for the same user. The implementation counts prior error entries in the audit log. On the third attempt, it returns a human-support escalation without running the skill again.

## Limitations
- Translation is a deterministic placeholder, not a real translation service.
- Contact lookup uses a small in-code sample directory.
- Memory and audit entries are in-memory and reset when the process exits.
- The runtime is a teaching simulation, not a production agent framework.
