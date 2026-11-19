"""
Lab 7: Agentic Node Graph -- Campus App Builder

A deterministic, offline simulation of a workflow represented as a graph.
Each node has an owner, input/output contract, success condition,
success action, failure behavior, retry policy, and approval requirement.
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


def requirement_node(state: State) -> State:
    state["requirements"] = [
        "user login",
        "event listing",
        "RSVP button",
    ]
    return state


def planner_node(state: State) -> State:
    requirements = state.get("requirements", [])
    state["tasks"] = {
        requirement: f"task_for({requirement})"
        for requirement in requirements
    }
    return state


def builder_node(state: State) -> State:
    if state.get("force_build_fail"):
        state["build_ok"] = False
        return state

    state["build_ok"] = True
    state["code"] = "app.py generated"
    return state


def tester_node(state: State) -> State:
    state["tests_passed"] = state.get("build_ok", False)
    return state


def reviewer_node(state: State) -> State:
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state: State) -> State:
    # In this simulation, approval is supplied through the input state.
    state["human_signoff"] = state.get("human_approved", True)
    return state


GRAPH: List[Node] = [
    Node(
        name="requirement",
        owner="requirement_agent",
        input_description="Campus event app goal",
        output_description="At least three clear app requirements",
        success_fn=lambda s: len(s.get("requirements", [])) >= 3,
        action=requirement_node,
        on_fail="escalate_to_human: goal is too vague",
        retry_behavior="Ask the user to clarify the goal, then retry once",
    ),
    Node(
        name="planner",
        owner="planner_agent",
        input_description="Extracted app requirements",
        output_description="A task mapped to every requirement",
        success_fn=lambda s: all(
            requirement in s.get("tasks", {})
            for requirement in s.get("requirements", [])
        ),
        action=planner_node,
        on_fail="return_to_requirement",
        retry_behavior="Regenerate the task breakdown once",
    ),
    Node(
        name="builder",
        owner="builder_agent",
        input_description="Task breakdown",
        output_description="Generated application code and build status",
        success_fn=lambda s: s.get("build_ok", False),
        action=builder_node,
        on_fail="retry_build_or_escalate",
        retry_behavior="Retry build once, then escalate to a human",
    ),
    Node(
        name="tester",
        owner="tester_agent",
        input_description="Generated application code",
        output_description="Automated test result",
        success_fn=lambda s: s.get("tests_passed", False),
        action=tester_node,
        on_fail="route_back_to_builder",
        retry_behavior="Send test failures to builder for correction",
    ),
    Node(
        name="reviewer",
        owner="reviewer_agent",
        input_description="Code and passing test result",
        output_description="Code-review status",
        success_fn=lambda s: s.get("review_clean", False),
        action=reviewer_node,
        on_fail="route_back_to_builder",
        retry_behavior="Request fixes and run review again",
    ),
    Node(
        name="human_gate",
        owner="human",
        input_description="Reviewed application",
        output_description="Human sign-off",
        success_fn=lambda s: s.get("human_signoff", False),
        action=human_gate_node,
        on_fail="return_to_planner_with_human_feedback",
        retry_behavior="Revise according to human feedback",
        human_approval="Required before final acceptance",
    ),
]


def print_graph(graph: List[Node]) -> None:
    print("\n=== NODE GRAPH ===")
    for index, node in enumerate(graph):
        suffix = " -> " if index < len(graph) - 1 else ""
        print(f"{node.name} [{node.owner}]{suffix}")
    print("\n=== NODE CONTRACTS ===")
    for node in graph:
        print(f"\nNode: {node.name}")
        print(f"  Input: {node.input_description}")
        print(f"  Output: {node.output_description}")
        print(f"  Owner: {node.owner}")
        print(f"  Success criteria: {node.success_fn.__doc__ or 'See success predicate in code'}")
        print(f"  Retry behavior: {node.retry_behavior}")
        print(f"  Failure behavior: {node.on_fail}")
        print(f"  Human approval: {node.human_approval}")


def simulate(force_build_fail: bool = False) -> State:
    state: State = {"force_build_fail": force_build_fail}

    print("\n=== FAILURE PATH ===" if force_build_fail else "\n=== SUCCESS PATH ===")

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
    print_graph(GRAPH)
    simulate()
    simulate(force_build_fail=True)
