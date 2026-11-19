"""
Lab 7 -- Assignment 1: Add a Security-Scan Node

The security_scan node is inserted between builder and tester.
Two runs are demonstrated:
1. The security scan passes and the graph completes.
2. The builder succeeds, but the security scan fails and stops the graph.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any, List

State = Dict[str, Any]


@dataclass
class Node:
    name: str
    owner: str
    input_description: str
    output_description: str
    success_fn: Callable[[State], bool]
    action: Callable[[State], State]
    on_fail: str
    retry_behavior: str
    human_approval: str = "Not required"


def requirement_node(state):
    state["requirements"] = ["user login", "event listing", "RSVP button"]
    return state


def planner_node(state):
    state["tasks"] = {
        req: f"task_for({req})" for req in state.get("requirements", [])
    }
    return state


def builder_node(state):
    state["build_ok"] = not state.get("force_build_fail", False)
    if state["build_ok"]:
        state["code"] = "app.py generated"
    return state


def security_scan_node(state):
    # A flag lets us deliberately simulate a vulnerability being detected.
    state["security_passed"] = not state.get("force_security_fail", False)
    state["security_report"] = (
        "No critical issues found"
        if state["security_passed"]
        else "Critical issue: unsafe input handling"
    )
    return state


def tester_node(state):
    state["tests_passed"] = (
        state.get("build_ok", False)
        and state.get("security_passed", False)
    )
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("human_approved", True)
    return state


GRAPH: List[Node] = [
    Node(
        "requirement", "requirement_agent",
        "Campus app goal", "At least three app requirements",
        lambda s: len(s.get("requirements", [])) >= 3,
        requirement_node, "escalate_to_human",
        "Clarify requirements and retry once",
    ),
    Node(
        "planner", "planner_agent",
        "App requirements", "Task mapped to each requirement",
        lambda s: all(r in s.get("tasks", {}) for r in s.get("requirements", [])),
        planner_node, "return_to_requirement",
        "Regenerate task breakdown once",
    ),
    Node(
        "builder", "builder_agent",
        "Task breakdown", "Generated application code",
        lambda s: s.get("build_ok", False),
        builder_node, "retry_build_or_escalate",
        "Retry build once, then escalate",
    ),
    Node(
        "security_scan", "security_agent",
        "Generated application code", "Security report and pass/fail result",
        lambda s: s.get("security_passed", False),
        security_scan_node, "block_release_and_escalate_to_security_reviewer",
        "Fix the vulnerability and rerun the scan; do not continue to testing",
        "Security reviewer approval required if a critical issue is found",
    ),
    Node(
        "tester", "tester_agent",
        "Security-approved application code", "Automated test result",
        lambda s: s.get("tests_passed", False),
        tester_node, "route_back_to_builder",
        "Send failing tests to builder for correction",
    ),
    Node(
        "reviewer", "reviewer_agent",
        "Code and passing tests", "Code-review status",
        lambda s: s.get("review_clean", False),
        reviewer_node, "route_back_to_builder",
        "Request fixes and review again",
    ),
    Node(
        "human_gate", "human",
        "Reviewed application", "Human sign-off",
        lambda s: s.get("human_signoff", False),
        human_gate_node, "return_for_revision",
        "Revise according to human feedback",
        "Required before final acceptance",
    ),
]


def simulate(force_security_fail=False):
    state = {
        "force_build_fail": False,
        "force_security_fail": force_security_fail,
    }
    print("\n=== SECURITY SCAN FAILURE ===" if force_security_fail
          else "\n=== SUCCESS PATH WITH SECURITY SCAN ===")

    for node in GRAPH:
        state = node.action(state)
        success = node.success_fn(state)
        print({
            "node": node.name,
            "owner": node.owner,
            "success": success,
            "state_after": dict(state),
        })
        if not success:
            print({
                "node": node.name,
                "failure_behavior_triggered": node.on_fail,
                "retry_behavior": node.retry_behavior,
            })
            break

    return state


if __name__ == "__main__":
    print("GRAPH:")
    print("requirement -> planner -> builder -> security_scan -> tester -> reviewer -> human_gate")
    for node in GRAPH:
        print(
            f"\n{node.name}: input={node.input_description}; "
            f"output={node.output_description}; owner={node.owner}; "
            f"failure={node.on_fail}; approval={node.human_approval}"
        )
    simulate()
    simulate(force_security_fail=True)
