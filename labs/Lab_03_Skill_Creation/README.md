# Lab 3 — Skill Creation: Research Summary Skill

## Requirements
- Python 3.10 or later
- No third-party packages
- No API keys

## Files
- `main.py` — Reusable research-summary skill, tested on two different articles.
- `assignment_1.py` — Multi-claim input; selects a claim using a transparent evidence-support heuristic and records that a selection was made.
- `assignment_2.py` — Low-evidence input; explicitly returns `not stated in source` where the source provides no evidence or limitation.
- `README.md` — Run instructions and expected checks.
- `test_output.txt` — Captured execution transcripts.

## Run in VS Code terminal

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

If needed on Windows, use `py` instead of `python`.

## Reference program checks
- Outputs claim, evidence, limitation, and undergraduate takeaway.
- Does not leave the limitation field blank.
- Uses the same output keys for both sample articles.
- Prints a reusability check.

## Assignment 1 checks
- Adds an article with two separate claims.
- Scores candidate claims with an explicit, inspectable heuristic.
- Reports that one of multiple claims was selected.
- Returns evidence, limitation, and takeaway fields.

## Assignment 2 checks
- Uses an article with assertions but no concrete evidence or limitation.
- Returns `not stated in source` for evidence and limitation.
- Prints a no-fabrication check.

## Important limitation
The guide's reference skill and these assignment extensions are deterministic classroom stand-ins. Sentence splitting and evidence cues are intentionally simple; they do not provide robust semantic claim detection. A production skill would need stronger NLP/LLM reasoning and source-grounded verification.
