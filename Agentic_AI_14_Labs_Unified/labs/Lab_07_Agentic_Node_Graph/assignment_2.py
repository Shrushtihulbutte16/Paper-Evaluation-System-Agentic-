"""
Lab 7 -- Assignment 2: Add a Retry Limit to the Builder Node

The builder is allowed exactly one retry:
- First failure: retry the builder once.
- Second failure: escalate to a human; never attempt a third build.

Two scenarios are simulated as required by the lab guide.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any, List

State = Dict[str, Any]


@dataclass
class Node:
    name: str
    owner: str
    success_fn: Callable[[State], bool]
    action: Callable[[State], State]
    on_fail: str


def requirement_node(state):
    state["requirements"] = ["user login", "event listing", "RSVP button"]
    return state


def planner_node(state):
    state["tasks"] = {
        req: f"task_for({req})" for req in state.get("requirements", [])
    }
    return state


def builder_node(state):
    # build_failures_before_success controls the deterministic test scenario.
    attempt = state.get("build_attempts", 0) + 1
    state["build_attempts"] = attempt

    failures_to_simulate = state.get("build_failures_before_success", 0)
    if attempt <= failures_to_simulate:
        state["build_ok"] = False
        state["build_error"] = f"simulated build failure on attempt {attempt}"
    else:
        state["build_ok"] = True
        state["code"] = f"app.py generated on attempt {attempt}"
        state.pop("build_error", None)

    return state


def tester_node(state):
    state["tests_passed"] = state.get("build_ok", False)
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("review_clean", False)
    return state


GRAPH: List[Node] = [
    Node(
        "requirement", "requirement_agent",
        lambda s: len(s.get("requirements", [])) >= 3,
        requirement_node, "escalate_to_human",
    ),
    Node(
        "planner", "planner_agent",
        lambda s: all(r in s.get("tasks", {}) for r in s.get("requirements", [])),
        planner_node, "return_to_requirement",
    ),
    Node(
        "builder", "builder_agent",
        lambda s: s.get("build_ok", False),
        builder_node, "retry_once_then_escalate",
    ),
    Node(
        "tester", "tester_agent",
        lambda s: s.get("tests_passed", False),
        tester_node, "route_back_to_builder",
    ),
    Node(
        "reviewer", "reviewer_agent",
        lambda s: s.get("review_clean", False),
        reviewer_node, "route_back_to_builder",
    ),
    Node(
        "human_gate", "human",
        lambda s: s.get("human_signoff", False),
        human_gate_node, "return_for_revision",
    ),
]


def simulate(build_failures_before_success: int, scenario_name: str):
    state = {
        "build_failures_before_success": build_failures_before_success,
        "build_attempts": 0,
    }

    print(f"\n=== {scenario_name} ===")
    for node in GRAPH:
        if node.name == "builder":
            # First attempt plus at most one retry.
            while True:
                state = node.action(state)
                success = node.success_fn(state)
                print({
                    "node": node.name,
                    "owner": node.owner,
                    "attempt": state["build_attempts"],
                    "success": success,
                    "state_after": dict(state),
                })

                if success:
                    break

                if state["build_attempts"] == 1:
                    print("Builder failed once: using its one permitted retry.")
                    continue

                print({
                    "node": node.name,
                    "failure_behavior_triggered": "escalate_to_human",
                    "reason": "Builder failed twice; no third attempt is allowed.",
                })
                state["escalated_to_human"] = True
                return state
        else:
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
                })
                break

    return state


if __name__ == "__main__":
    # (a) One failure, then success on the single retry.
    first = simulate(
        build_failures_before_success=1,
        scenario_name="SCENARIO A: FAIL ONCE, RETRY, THEN SUCCEED",
    )
    assert first.get("build_attempts") == 2
    assert first.get("build_ok") is True
    assert first.get("human_signoff") is True

    # (b) Two failures; escalate immediately after the second failure.
    second = simulate(
        build_failures_before_success=2,
        scenario_name="SCENARIO B: FAIL TWICE, THEN ESCALATE",
    )
    assert second.get("build_attempts") == 2
    assert second.get("escalated_to_human") is True
    assert second.get("human_signoff") is not True

    print("\nRetry-limit checks passed: no scenario attempted a third build.")
