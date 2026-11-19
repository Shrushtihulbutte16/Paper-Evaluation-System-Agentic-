# Lab 8 — Parallel Swarm: Hackathon Planner

## Objective
Run independent role agents concurrently, merge their structured outputs, identify conflicts, and resolve them explicitly.

## Files
- `main.py`: four-role parallel swarm, merge, central critique, budget-priority resolution, and conflict log.
- `assignment_1.py`: adds `marketing_agent` and checks marketing cost against the same overall budget cap.
- `assignment_2.py`: replaces central critique with independent role-specific critiques and records which role raised each objection.

## Requirements
Python 3.10+. No third-party packages, API keys, or internet connection required.

## Run in VS Code PowerShell terminal
```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Expected demonstrations
- Reference: venue costs ₹45,000 while the overall budget cap is ₹30,000.
- Assignment 1: marketing cost is also checked against the overall budget cap; conflicts use `budget_over_preference`.
- Assignment 2: each role critiques independently; at least two distinct roles raise objections.

## Concepts
1. Parallel execution — `ThreadPoolExecutor` runs independent agents concurrently.
2. Merge — combines their structured outputs into one draft.
3. Critique — checks the draft against constraints.
4. Conflict resolution — applies an explicit priority rule.
5. Conflict log — records the objection and role responsible.

These are deterministic offline educational simulations, not real LLM-powered agents or real vendor integrations.
