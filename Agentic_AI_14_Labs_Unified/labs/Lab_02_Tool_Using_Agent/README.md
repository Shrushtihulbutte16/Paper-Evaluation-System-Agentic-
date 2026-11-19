# Lab 2 — Tool-Using Agent: Campus Data Assistant

## Requirements
- Python 3.10 or later
- No third-party packages
- No external API keys

## Files
- `main.py` — Complete reference implementation with calculator, CSV reader, and mock events API.
- `assignment_1.py` — Adds a notification drafting tool with a justified threshold check.
- `assignment_2.py` — Adds event categories and a three-tool chain: read CSV → filter category → calculate average.

## Run in VS Code terminal

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

If `python` is not recognized on Windows, use `py` instead.

## Expected results

### Reference program
- Total sign-ups: 74
- Average per event: 12.33
- Hackathon Kickoff: Innovation Lab, 2026-07-05
- Capstone Expo: gracefully reports missing metadata
- Trace records tool name, reason, input, and output

### Assignment 1
- Threshold: 13
- Average: 12.33, which is below the threshold
- `send_notification` drafts a low-turnout notice
- Output explicitly confirms `sent=False`; no notification is actually sent

The threshold is set to 13 for the demonstration because the guide's six sample events average 12.33. This makes the required notification branch observable without altering the guide's data.

### Assignment 2
- CSV has a category field (`technical` or `social`)
- The assistant reads the CSV, filters technical rows, validates the filtered subset, and calculates its average
- Technical events: 12, 9, 15, 7
- Expected technical-event average: 10.75
- An empty category is handled without calling the calculator

## Concepts demonstrated
- Function/tool calling
- Structured tool inputs and outputs
- Tool selection based on the question
- Tool chaining
- Error handling and graceful failure
- Traceable reasoning and execution logs
