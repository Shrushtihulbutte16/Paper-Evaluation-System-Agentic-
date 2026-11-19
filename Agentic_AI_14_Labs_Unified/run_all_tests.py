"""Run and verify all 42 lab programs in isolated Python processes."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LABS_DIR = ROOT / "labs"
parts = ["main.py", "assignment_1.py", "assignment_2.py"]
lab_dirs = sorted(p for p in LABS_DIR.iterdir() if p.is_dir())

results = []
for lab_dir in lab_dirs:
    for script_name in parts:
        script = lab_dir / script_name
        if not script.exists():
            results.append((lab_dir.name, script_name, False, "MISSING"))
            continue
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=lab_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        ok = proc.returncode == 0
        detail = proc.stdout
        if proc.stderr:
            detail += "\nSTDERR:\n" + proc.stderr
        results.append((lab_dir.name, script_name, ok, detail))

report_lines = []
for lab_name, script_name, ok, detail in results:
    status = "PASS" if ok else "FAIL"
    report_lines.append(f"===== {status}: {lab_name}/{script_name} =====\n")
    report_lines.append(detail)
    report_lines.append("\n")

report_path = ROOT / "test_results.txt"
report_path.write_text("\n".join(report_lines), encoding="utf-8")

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
for lab_name, script_name, ok, _ in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {lab_name}/{script_name}")
print(f"\nSUMMARY: {passed}/{total} programs passed.")
print(f"Full output saved to: {report_path}")

if passed != total:
    raise SystemExit(1)
