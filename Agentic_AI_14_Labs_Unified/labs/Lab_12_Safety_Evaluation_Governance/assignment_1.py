"""Assignment 1 — Cost-category control and adversarial missing-cost test."""

class CostGovernedAgent:
    permissions = {"can_write": "staging_only"}

    def __init__(self, budget_threshold):
        self.budget_threshold = budget_threshold
        self.evaluated = False
        self.audit_log = []

    def log(self, step, data):
        self.audit_log.append({"step": step, "data": data})

    def evaluate(self):
        # Classroom evaluation fixture: 9 of 10 regression tests pass.
        pass_rate = 9 / 10
        self.evaluated = pass_rate >= 0.8
        self.log("evaluation", {"pass_rate": pass_rate, "passed": self.evaluated})
        return self.evaluated

    def propose_change(self, action, estimated_cost=None, finance_approved=False):
        if not self.evaluated:
            result = {"rejected": True, "reason": "evaluation gate not passed"}
        elif self.permissions.get("can_write") != "staging_only":
            raise PermissionError("No direct production write permission.")
        elif estimated_cost is None:
            result = {"rejected": True, "reason": "cost estimate is required"}
        elif not isinstance(estimated_cost, (int, float)) or estimated_cost < 0:
            result = {"rejected": True, "reason": "cost estimate must be a non-negative number"}
        elif estimated_cost > self.budget_threshold and not finance_approved:
            result = {
                "rejected": True,
                "reason": "estimated cost exceeds budget; finance approval is required",
                "estimated_cost": estimated_cost,
                "budget_threshold": self.budget_threshold,
            }
        else:
            result = {
                "rejected": False,
                "proposed_action": action,
                "estimated_cost": estimated_cost,
                "finance_approved": finance_approved,
                "requires_human_approval": True,
            }
        self.log("cost_control", result)
        return result


if __name__ == "__main__":
    agent = CostGovernedAgent(budget_threshold=5000)
    agent.evaluate()

    print("=== Within budget ===")
    print(agent.propose_change("resize staging service", estimated_cost=2500))

    print("\n=== Above budget without finance approval ===")
    print(agent.propose_change("upgrade production database", estimated_cost=9000))

    print("\n=== Above budget with explicit finance approval ===")
    print(agent.propose_change(
        "upgrade production database",
        estimated_cost=9000,
        finance_approved=True,
    ))

    print("\n=== Adversarial attempt: omit cost estimate ===")
    missing_cost = agent.propose_change("unknown-cost production change")
    print(missing_cost)
    assert missing_cost["rejected"] is True
    assert "cost estimate is required" in missing_cost["reason"]
    print("Confirmed: missing cost cannot silently default to approval.")
