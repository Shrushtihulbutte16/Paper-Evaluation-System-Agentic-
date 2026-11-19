"""
Lab 9: Deep Research Agent -- AI Topic Briefing

Question -> Search -> Extract -> Compare -> Synthesize.
This offline teaching example uses three illustrative source records.
Every synthesized claim is tagged with its source IDs.
"""

QUESTION = (
    "What are the demonstrated benefits and limitations of retrieval-augmented "
    "generation (RAG) for domain-specific question answering, as of the last year?"
)
SUCCESS_CRITERIA = (
    "At least 3 independent sources; at least 1 limitation identified; "
    "1 executive summary."
)

SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "author_org": "Illustrative academic research team",
        "date": "2026-02",
        "claim": "RAG reduces hallucination rate by 41% on domain QA vs a non-retrieval baseline.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set; may not generalize.",
        "relevance": "Evidence about factual reliability in a domain-specific QA setting.",
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "author_org": "Illustrative vendor engineering team",
        "date": "2026-04",
        "claim": "RAG improves answer accuracy by 35% in an internal support-ticket QA system.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "Funded/internal evaluation; no independent replication reported.",
        "relevance": "Evidence about accuracy in a practical support-ticket setting.",
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "author_org": "Illustrative independent benchmark group",
        "date": "2026-05",
        "claim": "RAG introduces a measurable latency overhead of 200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Latency depends heavily on retrieval index size; not tested at scale.",
        "relevance": "Evidence about the performance cost of retrieval.",
    },
]


def build_evidence_table(sources):
    """Return source records in the evidence-table structure."""
    return sources


def compare(sources):
    agreements, conflicts, gaps = [], [], []

    accuracy_claims = [
        source for source in sources
        if "reduces" in source["claim"] or "improves" in source["claim"]
    ]
    if len(accuracy_claims) >= 2:
        ids = ", ".join(source["id"] for source in accuracy_claims)
        agreements.append(
            f"{ids} agree that RAG improves factual/answer accuracy over "
            "a non-retrieval baseline, in different domains."
        )

    latency_sources = [
        source for source in sources if "latency" in source["claim"].lower()
    ]
    if latency_sources:
        latency_ids = ", ".join(source["id"] for source in latency_sources)
        conflicts.append(
            f"{latency_ids} raises a latency cost that the accuracy-focused "
            "sources do not discuss. This is a coverage gap, not a direct "
            "contradiction, because the sources measure different outcomes."
        )

    gaps.append(
        "No source in this set reports on RAG performance for non-English languages."
    )
    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps,
    }


def synthesize(evidence_table, comparison):
    """Build a source-traceable executive summary."""
    lines = [
        f"[{source['id']}] {source['claim']}"
        for source in evidence_table
    ]

    agreement_ids = [
        source["id"] for source in evidence_table
        if "reduces" in source["claim"] or "improves" in source["claim"]
    ]
    for agreement in comparison["agreements"]:
        lines.append(f"[{','.join(agreement_ids)}] {agreement}")

    latency_ids = [
        source["id"] for source in evidence_table
        if "latency" in source["claim"].lower()
    ]
    accuracy_ids = [
        source["id"] for source in evidence_table
        if source not in [
            item for item in evidence_table
            if "latency" in item["claim"].lower()
        ]
    ]
    for item in comparison["conflicts"]:
        ids = accuracy_ids + latency_ids
        lines.append(f"[{','.join(ids)}] {item}")

    for gap in comparison["gaps"]:
        lines.append(f"[gap] {gap}")

    return lines


def main():
    print("=== Research question ===")
    print(QUESTION)
    print("Success criteria:", SUCCESS_CRITERIA)

    table = build_evidence_table(SOURCES)
    print("\n=== Evidence table ===")
    for row in table:
        print(row)

    comparison = compare(table)
    print("\n=== Comparison ===")
    print(comparison)

    synthesis = synthesize(table, comparison)
    print("\n=== Executive summary (source-traceable) ===")
    for line in synthesis:
        print(line)

    print("\n=== Recommended next questions ===")
    print("- How does RAG latency scale with retrieval index size beyond the tested range?")
    print("- Do RAG accuracy gains hold for non-English domain QA?")


if __name__ == "__main__":
    main()
