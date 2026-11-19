# Lab 13 — Discipline-Specific Engineering Agents

## Objective
Apply agentic patterns (tools, goal, observation, domain reasoning, safety checks, and evaluation) to an engineering workflow outside computer science.

The reference implementation uses the Mechanical Engineering example: predictive maintenance from motor vibration and temperature logs.

## Project files
- `main.py` — mechanical predictive-maintenance agent.
- `assignment_1.py` — parallel Electrical Engineering agent for load forecasting / fault triage.
- `assignment_2.py` — trend-based escalation after three consecutive WARNING readings.
- `test_output.txt` — captured output from all three programs.

## Run in VS Code (Windows PowerShell)
```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

No third-party packages, API keys, or internet connection are required.

## Main workflow
1. Read sensor records using a data tool.
2. Classify the latest reading as NORMAL, WARNING, or ALARM.
3. Inspect the trend across multiple readings.
4. Apply the domain safety gate.
5. Produce an engineering recommendation and state the evaluation method.

## Safety
An ALARM-level condition never automatically triggers a shutdown or electrical isolation. The agent only recommends the action for qualified human review.

## Important engineering limitation
All sensor readings and thresholds are simulated classroom examples. The vibration bands are simplified ISO-10816-style teaching thresholds, not a claim of standards compliance or a substitute for equipment-specific limits, calibrated sensors, qualified engineering judgement, or site safety procedures. The electrical load limits are also illustrative. Do not use these scripts to operate real machinery or electrical infrastructure.
