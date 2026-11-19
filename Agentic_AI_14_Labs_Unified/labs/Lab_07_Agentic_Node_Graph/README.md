# Lab 7 — Agentic Node Graph: Campus App Builder

## Objective
Represent a campus event app workflow as a sequence of agentic nodes. Each node has a clear input, output, owner, success condition, and failure behavior.

## Project files
- `main.py` — reference graph, node contracts, success simulation, and builder-failure simulation.
- `assignment_1.py` — inserts `security_scan` between `builder` and `tester`; demonstrates a successful scan and a failing scan.
- `assignment_2.py` — limits the builder to exactly one retry; demonstrates one-failure-then-success and two-failures-then-escalation.

## Requirements
- Python 3.10+
- No third-party packages
- No API key or internet connection required

## Run in VS Code terminal (PowerShell)
Open this folder in VS Code, then run:

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Expected behavior
### Reference
- Success: requirement -> planner -> builder -> tester -> reviewer -> human_gate.
- Failure: if builder fails, the graph stops and reports `retry_build_or_escalate`.

### Assignment 1
- New order: requirement -> planner -> builder -> security_scan -> tester -> reviewer -> human_gate.
- If security scan fails, execution stops at `security_scan`; testing does not run.

### Assignment 2
- Scenario A: builder attempt 1 fails; attempt 2 succeeds; graph continues.
- Scenario B: builder attempt 1 and attempt 2 fail; execution escalates to a human. No third build attempt is made.

## Important note
These are deterministic, offline educational simulations of agent/node orchestration. They demonstrate graph execution and control flow; they do not call real LLMs or build a production campus application.
