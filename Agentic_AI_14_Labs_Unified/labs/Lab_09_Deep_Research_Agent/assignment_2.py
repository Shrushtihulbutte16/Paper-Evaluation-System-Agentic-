"""
Lab 9 -- Assignment 2: Weight Sources by Quality

Each source receives a quality tier. When sources conflict, synthesis
leans toward the higher-tier source while explicitly disclosing that
the lower-tier claim was down-weighted, not discarded.
"""

from assignment_1 import S4, compare_with_contradiction

SOURCES_WITH_QUALITY = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "quality_tier": "Tier 1 - peer-reviewed",
        "quality_rank": 3,
        "claim": "RAG reduces hallucination rate by 41% on domain QA vs a non-retrieval baseline.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set; may not generalize.",
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "quality_tier": "Tier 3 - vendor blog",
        "quality_rank": 1,
        "claim": "RAG improves answer accuracy by 35% in an internal support-ticket QA system.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "Funded/internal evaluation; no independent replication reported.",
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "quality_tier": "Tier 2 - independent benchmark",
        "quality_rank": 2,
        "claim": "RAG introduces a measurable latency overhead of 200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Latency depends heavily on retrieval index size; not tested at scale.",
    },
    {
        **S4,
        "quality_tier": "Tier 2 - independent evaluation",
        "quality_rank": 2,
    },
]


def synthesize_weighted(sources):
    by_id = {source["id"]: source for source in sources}
    s1 = by_id["S1"]
    s4 = by_id["S4"]

    lines = [
        f"[{source['id']} | {source['quality_tier']}] {source['claim']}"
        for source in sources
    ]

    if s1["quality_rank"] > s4["quality_rank"]:
        preferred = s1
        down_weighted = s4
    elif s4["quality_rank"] > s1["quality_rank"]:
        preferred = s4
        down_weighted = s1
    else:
        preferred = None
        down_weighted = None

    if preferred:
        lines.append(
            f"[S1,S4] The synthesis leans toward {preferred['id']} "
            f"({preferred['quality_tier']}) because it has the higher source-quality tier."
        )
        lines.append(
            f"[S1,S4] {down_weighted['id']} ({down_weighted['quality_tier']}) "
            "is down-weighted, not discarded; its contrary finding remains disclosed."
        )
    else:
        lines.append(
            "[S1,S4] The sources have equal quality tiers; no quality-based winner "
            "is selected, so the conflict remains unresolved."
        )

    lines.append(
        "[S1,S4] Quality tiers are a transparent prioritization aid, not proof "
        "that the higher-tier result is universally correct."
    )
    return lines


def main():
    comparison = compare_with_contradiction(SOURCES_WITH_QUALITY)
    print("=== Source quality tiers ===")
    for source in SOURCES_WITH_QUALITY:
        print(
            source["id"],
            source["quality_tier"],
            "| rank:", source["quality_rank"],
            "| claim:", source["claim"],
        )

    print("\n=== Conflict to be weighted ===")
    for conflict in comparison["direct_conflicts"]:
        print(conflict)

    print("\n=== Weighted synthesis ===")
    for line in synthesize_weighted(SOURCES_WITH_QUALITY):
        print(line)

    assert any("down-weighted, not discarded" in line
               for line in synthesize_weighted(SOURCES_WITH_QUALITY))
    print("\nCheck passed: lower-tier claim remains explicitly disclosed.")


if __name__ == "__main__":
    main()
