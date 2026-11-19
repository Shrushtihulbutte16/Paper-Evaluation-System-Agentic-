# Lab 9 — Deep Research Agent: AI Topic Briefing

## Objective
Create an evidence table from multiple sources, compare agreements and conflicts, identify gaps, and write a source-traceable executive summary.

## Files
- `main.py` — reference workflow: research question, three source records, evidence table, comparison, synthesis, and next questions.
- `assignment_1.py` — adds S4, a directly contradicting source, and distinguishes a genuine conflict from a coverage gap.
- `assignment_2.py` — adds source-quality tiers and makes the synthesis state which claim it leans toward while disclosing the down-weighted claim.
- `test_output.txt` — captured outputs from all three scripts.

## Requirements
- Python 3.10+
- No third-party packages
- No API key or internet connection required

## Run in VS Code terminal (PowerShell)
```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Workflow
Question -> Search/source records -> Extract -> Compare -> Synthesize

## Important interpretation
The source records and study figures in this lab are illustrative classroom data copied from the lab-guide scenario, not independently verified real-world research findings. The scripts demonstrate evidence organization and synthesis logic; they do not perform live web research or call an LLM.

## Success criteria
- At least three source records.
- At least one limitation is captured.
- Executive summary statements are traceable to source IDs.
- Assignment 1 reports S1/S4 as a genuine contradiction, with a plausible explanation.
- Assignment 2 explicitly discloses that a lower-tier claim is down-weighted, not discarded.
