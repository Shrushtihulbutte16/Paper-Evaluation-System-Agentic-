"""
Lab 3 — Assignment 1: Handle a Multi-Claim Source

Add an article with two unrelated claims. Extend the skill to identify
candidate claims, score their evidence support, and explicitly report
that it selected one claim from competing claims.

This deterministic heuristic is a classroom stand-in, not a general
natural-language inference model.
"""

from main import split_sentences


ARTICLE_C = {
    "title": "A Campus AI Platform Changes Cost and Accuracy",
    "text": (
        "The new campus AI platform reduced support operating costs by 18%. "
        "In a separate evaluation, answer accuracy increased from 76% to 89% "
        "across 500 benchmark questions. The evaluation was limited to three "
        "introductory courses, so results may not generalize to advanced courses."
    ),
}


def evidence_score(claim, sentences):
    """
    Give a simple heuristic score to a candidate claim.

    A claim receives support when a different sentence contains evidence
    cues such as a measurement, benchmark, sample size, or comparison.
    """
    score = 0
    evidence_cues = (
        "%",
        "increased from",
        "decreased from",
        "across ",
        "measured",
        "evaluation",
        "benchmark",
        "compared",
    )

    for sentence in sentences:
        if sentence == claim:
            continue
        if any(cue in sentence.lower() for cue in evidence_cues):
            score += 1

    # A numerical result in the claim is a signal, but not proof by itself.
    if any(char.isdigit() for char in claim):
        score += 1

    return score


def apply_multi_claim_skill(article):
    sentences = split_sentences(article["text"])

    # For this assignment's designed input, the first two sentences express
    # separate claims. The remaining sentences may provide limitations.
    candidates = sentences[:2]

    if not candidates:
        selected_claim = "not stated in source"
        selected_score = 0
    else:
        scored = [
            (claim, evidence_score(claim, sentences))
            for claim in candidates
        ]
        selected_claim, selected_score = max(
            scored, key=lambda item: item[1]
        )

    # Keep the selection transparent rather than silently choosing a sentence.
    selection_note = (
        f"Selected 1 of {len(candidates)} competing claims using the "
        f"evidence-support heuristic (score={selected_score})."
        if len(candidates) > 1
        else "No competing claims were identified."
    )

    evidence = next(
        (
            sentence for sentence in sentences
            if sentence != selected_claim
            and any(
                cue in sentence.lower()
                for cue in (
                    "evaluation", "across ", "benchmark",
                    "measured", "increased from", "decreased from",
                )
            )
        ),
        "not stated in source",
    )

    limitation = next(
        (
            sentence for sentence in sentences
            if any(
                marker in sentence.lower()
                for marker in (
                    "limited to", "may not generalize", "unclear",
                    "does not include", "small sample",
                )
            )
        ),
        "not stated in source",
    )

    return {
        "claim": selected_claim,
        "selection_note": selection_note,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": (
            f"Undergraduate takeaway: {selected_claim.rstrip('.')} "
            "should be interpreted in light of the stated evidence and limitations."
        ),
    }


if __name__ == "__main__":
    result = apply_multi_claim_skill(ARTICLE_C)

    print(f"--- {ARTICLE_C['title']} ---")
    for key, value in result.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
