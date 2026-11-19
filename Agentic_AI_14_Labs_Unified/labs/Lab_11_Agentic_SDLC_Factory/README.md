# Lab 11 — Agentic SDLC Factory

## Objective
Automate a small feature through a software-development lifecycle (SDLC) pipeline:
Requirement → Design → Code → Test → Review → Documentation → Release.

The central requirement is **test independence**. `testing_agent(stories)` creates a test suite from the user story's acceptance criteria only. It does not receive or inspect the implementation. The returned test function is later given the endpoint by the pipeline.

## Files
- `main.py` — reference CSV export pipeline with two human checkpoints.
- `assignment_1.py` — two concurrent stories (CSV and PDF export), with separate design/code/test lineage.
- `assignment_2.py` — deliberately inverted filter condition; unchanged independent tests catch the regression.
- `test_output.txt` — captured output from all three scripts.

## Run in VS Code (Windows PowerShell)
Open this folder in VS Code, open Terminal → New Terminal, then run:

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

No third-party packages, API keys, or internet connection are required. The PDF assignment creates a minimal local PDF using Python's standard library; it does not call an external PDF service.

## Key concepts
1. Requirement agent converts a feature request into a user story and acceptance criteria.
2. Design and coding agents produce artifacts tied to the story ID.
3. Testing agent is independent of implementation: tests are written from acceptance criteria first.
4. Review checks design completeness, lineage, and test outcomes.
5. Human checkpoints confirm requirements and make the final accept/reject decision.
6. Documentation and release agents prepare usage notes, release notes, and a rollback plan.

## Assignment 2 note
The inverted filter is intentionally incorrect. A failing test is the expected successful demonstration: it proves the test suite can detect a bug rather than merely approving the implementation.
