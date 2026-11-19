"""
Lab 1 — Assignment 2: Detect a Scheduling Conflict

The schedule tool reports Wednesday and Friday as busy.
The agent checks whether those days are included in the student's
unavailable days. It reports conflicts before generating a final plan.

For this deterministic demonstration, the simulated user resolves the
conflict by marking the busy days unavailable.
"""

import json
from main import StudyPlannerAgent, SIMULATED_ANSWERS


class ConflictAwareStudyPlannerAgent(StudyPlannerAgent):
    def __init__(self, existing_schedule):
        super().__init__(existing_schedule)
        self.conflicts = []

    def detect_conflicts(self, busy_slots):
        unavailable = set(self.goal["unavailable_days"] or [])
        busy_days = set(busy_slots.get("busy_days", []))

        # A busy day is a conflict unless the student marked it unavailable.
        self.conflicts = sorted(busy_days - unavailable)
        return self.conflicts

    def run(self):
        # Gather the same missing requirements as the reference agent.
        while self.goal["subjects"] is None:
            self.goal["subjects"] = SIMULATED_ANSWERS["subjects"]
            self.log.append({
                "iteration": len(self.log) + 1,
                "planned": "ask for subjects",
                "action": "asked user for subjects",
                "observed": self.goal["subjects"],
                "stopped": False,
            })

        while self.goal["hours_per_day"] is None:
            self.goal["hours_per_day"] = SIMULATED_ANSWERS["hours_per_day"]
            self.log.append({
                "iteration": len(self.log) + 1,
                "planned": "ask for hours_per_day",
                "action": "asked user for hours_per_day",
                "observed": self.goal["hours_per_day"],
                "stopped": False,
            })

        while self.goal["unavailable_days"] is None:
            self.goal["unavailable_days"] = SIMULATED_ANSWERS["unavailable_days"]
            self.log.append({
                "iteration": len(self.log) + 1,
                "planned": "ask for unavailable_days",
                "action": "asked user for unavailable_days",
                "observed": self.goal["unavailable_days"],
                "stopped": False,
            })

        busy = self.read_existing_schedule()
        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "read existing schedule",
            "action": "tool call: read_existing_schedule()",
            "observed": busy,
            "stopped": False,
        })

        conflicts = self.detect_conflicts(busy)

        if conflicts:
            print("SCHEDULING CONFLICT DETECTED!")
            print("Busy days not marked unavailable:", ", ".join(conflicts))
            print("The plan will not be finalized until these conflicts are resolved.")

            # Simulated user resolution for this runnable example.
            print("\nSimulated resolution: marking conflicting days unavailable.")
            self.goal["unavailable_days"].extend(conflicts)
            self.goal["unavailable_days"] = sorted(
                set(self.goal["unavailable_days"]),
                key=[
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"
                ].index
            )
            print("Updated unavailable days:", self.goal["unavailable_days"])

            self.log.append({
                "iteration": len(self.log) + 1,
                "planned": "resolve reported scheduling conflicts",
                "action": "marked conflicting busy days unavailable",
                "observed": self.goal["unavailable_days"].copy(),
                "stopped": False,
            })
        else:
            print("No scheduling conflicts detected.")

        # Finalize only after conflict detection and resolution.
        self.plan = self._build_plan(busy)
        self.goal["schedule_generated"] = True
        self.log.append({
            "iteration": len(self.log) + 1,
            "planned": "generate conflict-free weekly plan",
            "action": "built weekly plan after conflict check",
            "observed": self.plan.copy(),
            "stopped": True,
            "stop_reason": "all reported conflicts were resolved",
        })
        return self.plan


if __name__ == "__main__":
    agent = ConflictAwareStudyPlannerAgent(
        existing_schedule={"busy_days": ["Wednesday", "Friday"]}
    )

    final_plan = agent.run()

    print("\n=== Final conflict-checked plan ===")
    print(json.dumps(final_plan, indent=2))

    print("\n=== Full iteration log ===")
    for entry in agent.log:
        print(json.dumps(entry, indent=2))
