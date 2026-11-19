# Lab 1 — Agent vs Chatbot: Study Planner

## Requirements
- Python 3.10 or later
- No external packages or API keys required

## Files
- `main.py`: Complete reference Study Planner Agent.
- `assignment_1.py`: Adds two independent feedback rounds and verifies that both mutate the same plan object.
- `assignment_2.py`: Detects busy-day conflicts, reports them, simulates a resolution, and only then finalizes the plan.

## Run in VS Code terminal

Open this folder in VS Code, then run:

```bash
python main.py
python assignment_1.py
python assignment_2.py
```

On Windows, if `python` is not recognized, try:

```powershell
py main.py
py assignment_1.py
py assignment_2.py
```

## Expected checks

### Reference program
- Collects only missing goal fields.
- Reads the existing schedule through a tool-like method.
- Generates a weekly plan.
- Revises Tuesday's time after feedback.
- Prints an iteration log.

### Assignment 1
- Applies Tuesday evening feedback.
- Applies Friday one-hour feedback.
- Prints `Same plan object throughout both revisions: True`.

### Assignment 2
- Detects Wednesday and Friday as busy days not marked unavailable.
- Reports the conflict before finalizing.
- Simulates marking those days unavailable.
- Produces a plan that excludes the conflicting days.

## Important implementation note
The lab guide's reference program uses deterministic simulated inputs instead of a live LLM. This implementation preserves that offline, inspectable approach. Assignment 2 uses a simulated user resolution so the program can be executed end-to-end without interactive input.
