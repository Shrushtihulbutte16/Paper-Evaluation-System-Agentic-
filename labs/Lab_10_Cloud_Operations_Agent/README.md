# Lab 10 — Cloud Operations Agent: Failed Deployment

## Objective
Inspect deployment logs and metrics, identify a likely root cause, classify severity, propose remediation, and request human approval before high-risk action.

## Files
- `main.py` — diagnoses the payments-service incident and drafts an approval request for rollback.
- `assignment_1.py` — adds a database connection-pool exhaustion incident with separate logs, deployment history, and metrics.
- `assignment_2.py` — demonstrates a low-risk `restart_single_pod` path and verifies rollback remains approval-gated.
- `test_output.txt` — captured output from all three programs.

## Requirements
- Python 3.10+
- No third-party packages
- No API keys, cloud credentials, or internet connection

## Run in VS Code terminal (PowerShell)
```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Key concepts
1. Observe — inspect logs and metrics.
2. Reason — find incident start and correlate errors with recent deployments.
3. Classify — compare current error rate with baseline.
4. Assess risk — distinguish high-risk from low-risk actions.
5. Act safely — request human approval for high-risk rollback; only low-risk actions can use the simulated auto-remediation path.

## Safety note
This is a local classroom simulation. It does not connect to Kubernetes, AWS, Azure, GCP, or any real cloud service. `action_executed` in Assignment 2 is only a simulated policy outcome; it does not restart an actual pod.
