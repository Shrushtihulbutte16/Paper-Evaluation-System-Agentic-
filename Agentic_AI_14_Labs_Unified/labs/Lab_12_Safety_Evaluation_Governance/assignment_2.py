"""Assignment 2 — Force a fresh evaluation after every five proposals."""

class ReEvaluationAgent:
    def __init__(self):
        self.evaluated = False
        self.proposals_since_evaluation = 0
        self.audit_log = []

    def log(self, step, data):
        self.audit_log.append({"step": step, "data": data})

    def evaluate(self):
        pass_rate = 9 / 10
        self.evaluated = pass_rate >= 0.8
        self.proposals_since_evaluation = 0
        self.log("evaluation", {
            "pass_rate": pass_rate,
            "passed": self.evaluated,
            "proposal_counter_reset": True,
        })
        return self.evaluated

    def propose(self, action):
        if not self.evaluated:
            result = {"blocked": True, "reason": "agent must pass evaluation first"}
        elif self.proposals_since_evaluation >= 5:
            self.evaluated = False
            result = {
                "blocked": True,
                "reason": "five proposals reached; call evaluate() before another proposal",
            }
        else:
            self.proposals_since_evaluation += 1
            result = {
                "blocked": False,
                "proposal": action,
                "proposal_number_since_evaluation": self.proposals_since_evaluation,
            }
        self.log("proposal_attempt", result)
        return result


if __name__ == "__main__":
    agent = ReEvaluationAgent()
    print("Initial evaluation:", agent.evaluate())

    print("\n=== First five proposals ===")
    for number in range(1, 6):
        result = agent.propose(f"configuration change {number}")
        print(result)
        assert result["blocked"] is False

    print("\n=== Sixth proposal: must be blocked ===")
    sixth = agent.propose("configuration change 6")
    print(sixth)
    assert sixth["blocked"] is True

    print("\n=== Re-evaluate and retry ===")
    print("Re-evaluation passed:", agent.evaluate())
    retry = agent.propose("configuration change 6")
    print(retry)
    assert retry["blocked"] is False
    print("\nConfirmed: proposal 6 was blocked until a fresh evaluation.")
