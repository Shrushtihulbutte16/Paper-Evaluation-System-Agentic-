"""
Lab 9 -- Assignment 1: Add a Directly Contradicting Source

S4 directly contradicts S1 by reporting no measurable hallucination
reduction in a different domain/evaluation. The comparison labels this
as a genuine conflict and explains a plausible methodological reason.
The separate S3 latency observation remains a coverage gap, not a conflict.
"""

from main import SOURCES, build_evidence_table, synthesize

S4 = {
    "id": "S4",
    "type": "independent evaluation report",
    "author_org": "Illustrative independent evaluation team",
    "date": "2026-06",
    "claim": "RAG showed no measurable reduction in hallucination rate compared with a non-retrieval baseline.",
    "evidence": "Evaluation on a separate legal-domain QA dataset using a different retrieval setup.",
    "limitation": "Different domain, dataset, and evaluation methodology; results may not transfer to medical QA.",
    "relevance": "Directly tests whether the hallucination reduction reported by S1 generalizes.",
}


def compare_with_contradiction(sources):
    result = {
        "agreements": [],
        "direct_conflicts": [],
        "coverage_gaps": [],
    }

    s1 = next(source for source in sources if source["id"] == "S1")
    s4 = next(source for source in sources if source["id"] == "S4")

    result["direct_conflicts"].append({
        "source_ids": ["S1", "S4"],
        "claims": [s1["claim"], s4["claim"]],
        "conflict": (
            "S1 reports a 41% reduction in hallucination, while S4 reports "
            "no measurable reduction."
        ),
        "plausible_reason": (
            "The studies use different domains, datasets, retrieval setups, "
            "and evaluation methodologies; S1 uses a medical QA set while "
            "S4 uses a legal QA set."
        ),
    })

    s3 = next(source for source in sources if source["id"] == "S3")
    result["coverage_gaps"].append({
        "source_ids": ["S1", "S2", "S3"],
        "gap": (
            f"{s3['id']} reports latency overhead, while the accuracy-focused "
            "sources do not measure latency. This is missing coverage, not "
            "a contradictory result."
        ),
    })
    result["agreements"].append(
        "S1 and S2 report accuracy-related benefits in their respective settings."
    )
    return result


def synthesize_with_conflict(sources, comparison):
    lines = [
        f"[{source['id']}] {source['claim']}"
        for source in sources
    ]
    for agreement in comparison["agreements"]:
        lines.append(f"[S1,S2] {agreement}")
    for conflict in comparison["direct_conflicts"]:
        ids = ",".join(conflict["source_ids"])
        lines.append(f"[{ids}] DIRECT CONFLICT: {conflict['conflict']}")
        lines.append(f"[{ids}] Possible explanation: {conflict['plausible_reason']}")
    for gap in comparison["coverage_gaps"]:
        lines.append(f"[{','.join(gap['source_ids'])}] GAP: {gap['gap']}")
    return lines


def main():
    sources = build_evidence_table(SOURCES + [S4])
    comparison = compare_with_contradiction(sources)

    print("=== Fourth source: S4 ===")
    print(S4)
    print("\n=== Updated comparison ===")
    print(comparison)
    print("\n=== Updated synthesis ===")
    for line in synthesize_with_conflict(sources, comparison):
        print(line)

    assert comparison["direct_conflicts"]
    assert "different domains" in comparison["direct_conflicts"][0]["plausible_reason"]
    print("\nCheck passed: S1 vs S4 is classified as a direct conflict, not a gap.")


if __name__ == "__main__":
    main()
