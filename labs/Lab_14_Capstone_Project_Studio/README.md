# Lab 14 — Capstone Project Studio

## Project
**Campus Help-Desk Agent** — an offline, deterministic reference worklet for the Agentic AI Systems Lab 14.

This project demonstrates the required capstone elements:
- A node graph: `intake -> safety_check -> triage -> respond -> log`
- Three tools: FAQ search, ticket creation, ticket-status lookup
- A reusable `triage_skill`
- Short-term session state and long-term interaction history
- Prompt log and audit log
- A small regression evaluation suite
- A safety control that rejects empty input
- Explicit limitations and a next-step roadmap

## Requirements
- Python 3.10+
- No third-party packages
- No API keys or internet connection

## Run in VS Code (Windows PowerShell)

Open this folder in VS Code, then open **Terminal → New Terminal**.

Run each program separately:

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

If `python` is not recognized, try `py` instead:

```powershell
py main.py
py assignment_1.py
py assignment_2.py
```

## What each file does

### `main.py`
Runs the complete reference worklet:
1. Answers a known Wi-Fi FAQ.
2. Creates a ticket for an unsupported issue.
3. Checks the created ticket status.
4. Rejects empty input.
5. Runs the evaluation suite and prints prompt/audit/memory traces.

### `assignment_1.py`
Adds a second reusable skill, `password_reset_skill`, with its own safety constraint. The node graph routes password-reset requests to this skill and other requests to `triage_skill`.

### `assignment_2.py`
Expands evaluation to at least five issue types and includes an adversarial prompt-injection-style case. The agent treats it as an unsupported help request and escalates it instead of following its embedded instructions.

## Architecture and execution flow

```text
User issue
   |
   v
[Intake]
   |
   v
[Safety check] -- empty input --> Reject + audit
   |
   v
[Triage skill]
   |                 |
 FAQ match        No FAQ match
   |                 |
   v                 v
FAQ response     Create support ticket
   |                 |
   +--------+--------+
            |
            v
      [Respond]
            |
            v
 [Memory + audit log]
```

## Important limitations
- FAQ lookup uses simple keyword matching, not semantic retrieval.
- Tickets and memory are stored in Python lists/dictionaries and disappear when the process exits.
- There is no real email, ticketing platform, authentication, or human approval integration.
- The adversarial test is a deterministic rule-based classroom demonstration, not a complete prompt-injection defense.

## Suggested next steps for a real team-owned capstone
- Replace keyword lookup with retrieval over an approved FAQ knowledge base.
- Persist tickets and memory in SQLite or a managed database.
- Add priority classification and a human approval gate for critical incidents.
- Add authentication, role-based access, privacy controls, and monitoring.
- Evaluate on a larger, independently reviewed test set.

## Safety note
This is a local educational simulation. It does not connect to or modify a real campus support system.
