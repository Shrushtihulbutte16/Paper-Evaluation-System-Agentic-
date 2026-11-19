"""
Agentic AI Systems — Unified 14-Lab Runner

Run one lab or assignment from a single entry point:
    python main.py
    python main.py --lab 7
    python main.py --lab 7 --part assignment1
    python main.py --all

Each original lab program is preserved under labs/ and is launched in an
isolated Python process so its globals, mock databases, and demo state do not
leak into another lab.
"""

from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LABS_DIR = ROOT / "labs"

LABS = [
    (1, "Agent vs Chatbot — Study Planner", "Lab_01_Agent_vs_Chatbot"),
    (2, "Tool-Using Agent — Campus Data Assistant", "Lab_02_Tool_Using_Agent"),
    (3, "Skill Creation — Research Summary Skill", "Lab_03_Skill_Creation"),
    (4, "Memory and Retrieval — Project Memory", "Lab_04_Memory_and_Retrieval"),
    (5, "MCP-Style Connector — Mini Integration Layer", "Lab_05_MCP_Style_Connector"),
    (6, "Personal Agent Runtime — Skills, Tools, Memory, Audit", "Lab_06_Personal_Agent_Runtime"),
    (7, "Agentic Node Graph — Campus App Builder", "Lab_07_Agentic_Node_Graph"),
    (8, "Parallel Swarm — Hackathon Planner", "Lab_08_Parallel_Swarm"),
    (9, "Deep Research Agent — AI Topic Briefing", "Lab_09_Deep_Research_Agent"),
    (10, "Cloud Operations Agent — Failed Deployment", "Lab_10_Cloud_Operations_Agent"),
    (11, "Agentic SDLC Factory — Mini Software Team", "Lab_11_Agentic_SDLC_Factory"),
    (12, "Safety, Evaluation and Governance — Risky Agent Action", "Lab_12_Safety_Evaluation_Governance"),
    (13, "Discipline-Specific Engineering Agents — Mechanical / Electrical", "Lab_13_Discipline_Specific_Engineering_Agents"),
    (14, "Capstone Project Studio — Campus Help-Desk Agent", "Lab_14_Capstone_Project_Studio"),
]

PART_FILES = {
    "main": "main.py",
    "assignment1": "assignment_1.py",
    "assignment2": "assignment_2.py",
}
PART_LABELS = {
    "main": "Reference Program",
    "assignment1": "Assignment 1",
    "assignment2": "Assignment 2",
}


def show_labs():
    print("\n========== AGENTIC AI — 14 LABS ==========")
    for number, title, folder in LABS:
        print(f"{number:02d}. {title}")
    print("\nEach lab includes: reference program, Assignment 1, Assignment 2.")


def run_program(lab_number, part):
    lab = next((item for item in LABS if item[0] == lab_number), None)
    if lab is None:
        raise ValueError(f"Invalid lab number: {lab_number}")

    _, title, folder = lab
    script = LABS_DIR / folder / PART_FILES[part]
    if not script.is_file():
        raise FileNotFoundError(f"Program file not found: {script}")

    print("\n" + "=" * 78)
    print(f"LAB {lab_number:02d}: {title}")
    print(f"PART: {PART_LABELS[part]}")
    print("=" * 78 + "\n", flush=True)

    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(script.parent),
        check=False,
    )
    if completed.returncode != 0:
        print(f"\n[FAILED] Lab {lab_number:02d} / {PART_LABELS[part]} "
              f"(exit code {completed.returncode})")
        return False

    print(f"\n[COMPLETED] Lab {lab_number:02d} / {PART_LABELS[part]}")
    return True


def run_all():
    total = 0
    passed = 0
    for lab_number, _, _ in LABS:
        for part in PART_FILES:
            total += 1
            if run_program(lab_number, part):
                passed += 1
    print("\n" + "=" * 78)
    print(f"UNIFIED RUN SUMMARY: {passed}/{total} programs completed successfully")
    print("=" * 78)
    return passed == total


def interactive_menu():
    show_labs()
    while True:
        print("\nChoose an action:")
        print("  [1] Run a lab reference program")
        print("  [2] Run Assignment 1")
        print("  [3] Run Assignment 2")
        print("  [4] Run all 42 programs (14 labs × 3 parts)")
        print("  [5] Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "5":
            print("Exiting unified lab runner.")
            return
        if choice == "4":
            run_all()
            continue
        if choice not in {"1", "2", "3"}:
            print("Invalid choice. Choose 1, 2, 3, 4, or 5.")
            continue

        try:
            lab_number = int(input("Enter lab number (1-14): ").strip())
        except ValueError:
            print("Please enter a valid number.")
            continue

        part = {"1": "main", "2": "assignment1", "3": "assignment2"}[choice]
        run_program(lab_number, part)


def main():
    parser = argparse.ArgumentParser(
        description="Run all 14 Agentic AI labs and their assignments."
    )
    parser.add_argument("--lab", type=int, choices=range(1, 15),
                        help="Lab number to run (1-14).")
    parser.add_argument("--part", choices=PART_FILES,
                        default="main",
                        help="Part to run: main, assignment1, assignment2.")
    parser.add_argument("--all", action="store_true",
                        help="Run all 42 reference/assignment programs.")
    parser.add_argument("--list", action="store_true",
                        help="List all 14 labs.")
    args = parser.parse_args()

    if args.list:
        show_labs()
    elif args.all:
        raise SystemExit(0 if run_all() else 1)
    elif args.lab is not None:
        raise SystemExit(0 if run_program(args.lab, args.part) else 1)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
