"""
Lab 1: Agent vs Chatbot — Study Planner Agent

Implements the Goal -> Plan -> Act -> Observe -> Revise loop.
No external API key is required. Simulated inputs stand in for user responses.
"""

import json

# Simulated user responses for a reproducible demonstration.
SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"],
}

SIMULATED_FEEDBACK = "Move Tuesday's session to the evening."


class StudyPlannerAgent:
    def __init__(self, existing_schedule):
        # The goal is represented as structured data so it can be checked.
        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False,
        }
        self.existing_schedule = existing_schedule
        self.plan = None
        self.log = []

    def satisfied(self):
        """Return True when the agent has generated the requested plan."""
        return self.goal["schedule_generated"] is True

    def next_step(self):
        """Ask only for information that is still missing."""
        for field in ("subjects", "hours_per_day", "unavailable_days"):
            if self.goal[field] is None:
                return "ask", field
        return "generate_plan", None

    def read_existing_schedule(self):
        """Simulated tool that returns the student's existing busy days."""
        result = self.existing_schedule
        if "error" in result:
            raise RuntimeError(f"Schedule tool failed: {result['error']}")
        return result

    def run(self):
        """Run the Goal -> Plan -> Act -> Observe loop."""
        while not self.satisfied():
            step, argument = self.next_step()

            if step == "ask":
                answer = SIMULATED_ANSWERS[argument]
                self.goal[argument] = answer
                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": f"ask for {argument}",
                    "action": f"asked user for {argument}",
                    "observed": answer,
                    "stopped": False,
                })

            elif step == "generate_plan":
                busy = self.read_existing_schedule()
                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "read existing schedule before generating plan",
                    "action": "tool call: read_existing_schedule()",
                    "observed": busy,
                    "stopped": False,
                })

                self.plan = self._build_plan(busy)
                self.goal["schedule_generated"] = True
                self.log.append({
                    "iteration": len(self.log) + 1,
                    "planned": "generate schedule from gathered requirements",
                    "action": "built weekly plan",
                    "observed": self.plan.copy(),
                    "stopped": True,
                    "stop_reason": "goal.schedule_generated is now True",
                })

        return self.plan

    def _build_plan(self, busy_slots):
        """Build a plan while avoiding the busy-day time slot."""
        all_days = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]
        days = [
            day for day in all_days
            if day not in self.goal["unavailable_days"]
        ]

        subjects = self.goal["subjects"]
        if not subjects:
            raise ValueError("At least one subject is required.")

        plan = {}
        for index, day in enumerate(days):
            subject = subjects[index % len(subjects)]
            slot = "17:00-19:00"

            if day in busy_slots.get("busy_days", []):
                slot = "20:00-22:00"

            plan[day] = {
                "subject": subject,
                "time": slot,
                "duration_hours": self.goal["hours_per_day"],
            }

        return plan

    def revise(self, feedback):
        """
        Apply the reference assignment's Tuesday-evening feedback.
        The existing plan is mutated instead of being regenerated.
        """
        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "apply user feedback to existing plan",
            "action": f"feedback received: '{feedback}'",
            "observed": None,
            "stopped": False,
        })

        normalized = feedback.lower()
        if "tuesday" in normalized and "evening" in normalized:
            if self.plan and "Tuesday" in self.plan:
                self.plan["Tuesday"]["time"] = "20:00-22:00"

        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "confirm revised plan",
            "action": "mutated existing plan (not regenerated from scratch)",
            "observed": self.plan.copy() if self.plan else None,
            "stopped": True,
            "stop_reason": "revision applied without restarting the loop",
        })
        return self.plan


if __name__ == "__main__":
    existing_schedule = {"busy_days": ["Wednesday"]}
    agent = StudyPlannerAgent(existing_schedule)

    print("Stopping condition (declared before the loop runs):")
    print(" goal['schedule_generated'] is True\n")

    plan = agent.run()
    print("=== Initial plan ===")
    print(json.dumps(plan, indent=2))

    revised = agent.revise(SIMULATED_FEEDBACK)
    print("\n=== Revised plan (after feedback) ===")
    print(json.dumps(revised, indent=2))

    print("\n=== Full iteration log ===")
    for entry in agent.log:
        print(json.dumps(entry, indent=2))
