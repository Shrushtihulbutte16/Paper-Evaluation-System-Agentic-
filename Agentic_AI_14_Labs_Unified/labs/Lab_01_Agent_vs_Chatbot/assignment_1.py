"""
Lab 1 — Assignment 1: Two Rounds of Feedback

Both feedback rounds mutate the same plan object:
1. Move Tuesday's session to the evening.
2. Make Friday's session one hour long.
"""

import json
from main import StudyPlannerAgent


class ExtendedStudyPlannerAgent(StudyPlannerAgent):
    def revise(self, feedback):
        # Keep a reference to the original plan to demonstrate in-place updates.
        original_plan_id = id(self.plan)

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "apply a new feedback request",
            "action": f"feedback received: '{feedback}'",
            "observed": None,
            "stopped": False,
        })

        normalized = feedback.lower()

        if "tuesday" in normalized and "evening" in normalized:
            if "Tuesday" in self.plan:
                self.plan["Tuesday"]["time"] = "20:00-22:00"

        if "friday" in normalized and ("one hour" in normalized or "1 hour" in normalized):
            if "Friday" in self.plan:
                self.plan["Friday"]["duration_hours"] = 1
                self.plan["Friday"]["time"] = "17:00-18:00"

        # Verify that this revision changed the existing object, not a new plan.
        same_object = id(self.plan) == original_plan_id

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "verify and retain the revised plan",
            "action": "updated existing plan in place",
            "observed": {
                "plan": self.plan.copy(),
                "same_plan_object": same_object,
            },
            "stopped": True,
            "stop_reason": "feedback applied without regenerating the plan",
        })
        return self.plan


if __name__ == "__main__":
    agent = ExtendedStudyPlannerAgent(
        existing_schedule={"busy_days": ["Wednesday"]}
    )

    initial_plan = agent.run()
    original_plan_id = id(agent.plan)

    print("=== Initial plan ===")
    print(json.dumps(initial_plan, indent=2))

    print("\n=== Feedback round 1 ===")
    agent.revise("Move Tuesday's session to the evening.")
    print(json.dumps(agent.plan, indent=2))

    print("\n=== Feedback round 2 ===")
    agent.revise("Also make Friday's session shorter, only one hour.")
    print(json.dumps(agent.plan, indent=2))

    print("\nSame plan object throughout both revisions:",
          id(agent.plan) == original_plan_id)

    print("\n=== Full iteration log ===")
    for entry in agent.log:
        print(json.dumps(entry, indent=2))
