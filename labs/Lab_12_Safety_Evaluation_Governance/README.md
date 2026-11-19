# Lab 12 — Safety, Evaluation, and Governance

## Objective
Build a governance layer for an infrastructure agent proposing production configuration changes. The agent must assess permissions, pass evaluation, require human approval, maintain audit logs, require rollback evidence, and reject privacy-unscrubbed inputs.

## Project files
- `main.py` — reference production-change governance agent implementing the six controls in the lab guide.
- `assignment_1.py` — cost threshold, finance approval exception, and adversarial missing-cost rejection.
- `assignment_2.py` — forces re-evaluation after five proposals and blocks the sixth until evaluation is repeated.
- `test_output.txt` — captured output from all scripts.

## Run in VS Code (Windows PowerShell)
```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

No third-party packages, API keys, internet connection, or real cloud credentials are needed.

## Six controls in the reference program
1. **Permissions / least privilege:** the agent is restricted to staging write access and cannot directly write to production.
2. **Evaluation:** the diagnostic regression pass rate must meet the 80% threshold before proposals are allowed.
3. **Human approval:** every production change proposal is routed through an approval request.
4. **Audit logs:** evaluation, rejection, approval request, and human decision are recorded.
5. **Rollback:** a proposal without a rollback plan is rejected.
6. **Privacy:** diagnostic input must be privacy-scrubbed before a proposal is accepted.

Even after human approval, this agent does not execute the production change. It hands off to a separate privileged deployment process.

## Simulation note
The regression score (9/10), permissions, approval, and deployment handoff are local classroom fixtures. No real production system is contacted or changed.
