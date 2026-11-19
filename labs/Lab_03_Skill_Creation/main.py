"""
Lab 3: Skill Creation — Research Summary Skill

A reusable skill package defines instructions, constraints, and a stable
output contract. This deterministic classroom implementation applies the
same extraction workflow to two different articles without an API key.
"""

import json

ARTICLE_A = {
    "title": "Retrieval-Augmented Generation Reduces Hallucination in Domain QA",
    "text": (
        "A recent benchmark study found that retrieval-augmented generation (RAG) "
        "reduced factual hallucination rates by 41% compared to a non-retrieval "
        "baseline on a domain-specific question-answering task. The evaluation used "
        "200 held-out questions from a medical knowledge base. The authors note the "
        "evaluation set was small and drawn from a single domain, so results may not "
        "generalize to other domains without further testing."
    ),
}

ARTICLE_B = {
    "title": "Campus Wi-Fi Upgrade Improves Peak-Hour Throughput",
    "text": (
        "Following a campus-wide Wi-Fi access point upgrade, average peak-hour "
        "throughput in the library increased by 60%. The measurement was taken "
        "over two weeks post-upgrade using the network monitoring dashboard. "
        "The report does not include measurements from other buildings on campus, "
        "so it is unclear whether the improvement is uniform across campus."
    ),
}

SKILL_SPEC = {
    "name": "research_summary",
    "instructions": [
        "identify the single main claim",
        "list supporting evidence for that claim",
        "note at least one limitation (or 'not stated in source' if genuinely absent)",
        "write a 1-sentence undergraduate-level takeaway",
    ],
    "constraints": [
        "never present a hedged claim as unhedged fact",
        "never omit the limitation row, even if the source states none",
    ],
}


def split_sentences(article_text):
    """Split the guide's simple sample prose into non-empty sentences."""
    return [sentence.strip() for sentence in article_text.split(".") if sentence.strip()]


def apply_research_summary_skill(article):
    """
    Apply the reusable research-summary output contract.

    This intentionally simple, rule-based stand-in demonstrates the skill
    workflow and required output fields rather than LLM-level extraction.
    """
    sentences = split_sentences(article["text"])

    claim = sentences[0] if sentences else "not stated in source"
    evidence = sentences[1] if len(sentences) > 1 else "not stated in source"

    limitation_markers = (
        "small",
        "does not include",
        "unclear",
        "may not generalize",
        "not generalize",
    )
    limitation = next(
        (
            sentence for sentence in sentences
            if any(marker in sentence.lower() for marker in limitation_markers)
        ),
        "not stated in source",
    )

    takeaway = (
        f"Undergraduate takeaway: {claim.rstrip('.')} "
        "-- but verify before generalizing."
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": takeaway,
    }


def print_skill_output(article, output):
    print(f"\n--- {article['title']} ---")
    print(f"Claim:      {output['claim']}")
    print(f"Evidence:   {output['evidence']}")
    print(f"Limitation: {output['limitation']}")
    print(f"Takeaway:   {output['takeaway']}")


def reusability_check(output_a, output_b):
    """Check whether two different inputs produce the same output contract."""
    keys_a = set(output_a.keys())
    keys_b = set(output_b.keys())

    same_structure = keys_a == keys_b
    both_have_limitation = all(
        output["limitation"] != "" for output in (output_a, output_b)
    )

    print("\n=== Reusability check ===")
    print(f"Same output structure across both inputs: {same_structure}")
    print(f"Limitation field populated in both outputs: {both_have_limitation}")
    print(
        "Conclusion:",
        "SKILL IS REUSABLE"
        if same_structure and both_have_limitation
        else "SKILL NEEDS TIGHTER INSTRUCTIONS",
    )


if __name__ == "__main__":
    output_a = apply_research_summary_skill(ARTICLE_A)
    output_b = apply_research_summary_skill(ARTICLE_B)

    print_skill_output(ARTICLE_A, output_a)
    print_skill_output(ARTICLE_B, output_b)
    reusability_check(output_a, output_b)
