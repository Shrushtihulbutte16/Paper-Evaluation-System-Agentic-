# Agentic AI Systems — Unified 14-Lab Codebase

This project combines **all 14 labs** into one VS Code project and one entry-point file: `main.py`.

The original implementation for every lab is retained in its own folder, including:
- `main.py` — the lab's reference program
- `assignment_1.py` — Assignment 1
- `assignment_2.py` — Assignment 2
- `README.md` — lab-specific notes

The unified runner lets you launch any of the 42 programs from one menu or from a command.

## 1. Requirements

- Python 3.10 or later
- VS Code (recommended)
- No third-party Python packages are required for the lab programs in this bundle.
- No external LLM API keys are required. Mock APIs, sample datasets, and simulated infrastructure are used where the individual labs specify them.

## 2. Open in VS Code

1. Download and extract the ZIP.
2. Open the extracted `Agentic_AI_14_Labs_Unified` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run:

```powershell
python main.py
```

If `python` is not recognized, use:

```powershell
py main.py
```

## 3. Interactive menu

The menu lets you:
1. Run any lab's reference program.
2. Run Assignment 1 for any lab.
3. Run Assignment 2 for any lab.
4. Run all 42 programs.
5. Exit.

Choose the lab number when prompted.

## 4. Run directly from the terminal

Run the reference program for Lab 7:

```powershell
python main.py --lab 7
```

Run Lab 7 Assignment 1:

```powershell
python main.py --lab 7 --part assignment1
```

Run Lab 7 Assignment 2:

```powershell
python main.py --lab 7 --part assignment2
```

The supported `--part` values are:
- `main`
- `assignment1`
- `assignment2`

List all labs:

```powershell
python main.py --list
```

Run every reference program and assignment:

```powershell
python main.py --all
```

## 5. Folder structure

```text
Agentic_AI_14_Labs_Unified/
│
├── main.py
├── README.md
├── requirements.txt
├── run_all_tests.py
│
└── labs/
    ├── Lab_01_Agent_vs_Chatbot/
    │   ├── main.py
    │   ├── assignment_1.py
    │   ├── assignment_2.py
    │   └── README.md
    ├── Lab_02_Tool_Using_Agent/
    ├── ...
    └── Lab_14_Capstone_Project_Studio/
```

## 6. How the unified runner works

`main.py` is the single entry point. It routes your selection to the original lab script and starts it in a separate Python process. This keeps each lab's variables, mock databases, and execution state isolated. It also preserves the original reference programs and assignment logic rather than merging unrelated global variables into one giant Python file.

## 7. Test all programs

Run:

```powershell
python run_all_tests.py
```

This executes all 14 reference programs and both assignments for every lab (42 programs total) and writes a combined report to `test_results.txt`.

## 8. Important notes

- Lab 4 and Lab 8 are included, even though the earlier learning sequence may have skipped them.
- Some labs intentionally use mock APIs, simulated sensor readings, sample research sources, or simulated cloud operations. They do not contact real external systems.
- Lab 13's engineering thresholds and readings are illustrative classroom data, not operational safety limits.
- Running `--all` may print a large amount of output because it runs all 42 programs.
- This bundle is a unified launcher and organized codebase, not a claim that all 14 labs form one autonomous agent or share one live database.
