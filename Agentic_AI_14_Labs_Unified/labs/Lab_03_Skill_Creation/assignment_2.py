"""
Lab 3 — Assignment 2: Test Against a Low-Evidence Input

The article asserts a claim but provides no supporting evidence and no
limitation. The skill must explicitly return "not stated in source"
instead of inventing plausible details.
"""

from main import split_sentences


ARTICLE_D = {
    "title": "A New Study Method Transforms Student Performance",
    "text": (
        "A new study method dramatically improves student performance. "
        "Students using this method achieve better results."
    ),
}


def apply_low_evidence_skill(article):
    sentences = split_sentences(article["text"])

    claim = sentences[0] if sentences else "not stated in source"

    # These phrases indicate concrete supporting evidence in this simple
    # rule-based exercise. The source has none, so the field stays explicit.
    evidence_cues = (
        "%",
        "increased by",
        "decreased by",
        "compared to",
        "across ",
        "sample of",
        "measured",
        "benchmark",
        "data showed",
    )

    evidence_sentence = next(
        (
            sentence for sentence in sentences[1:]
            if any(cue in sentence.lower() for cue in evidence_cues)
        ),
        None,
    )

    limitation_markers = (
        "limited to",
        "small sample",
        "may not generalize",
        "does not include",
        "unclear",
        "limitation",
    )
    limitation = next(
        (
            sentence for sentence in sentences
            if any(marker in sentence.lower() for marker in limitation_markers)
        ),
        "not stated in source",
    )

    evidence = evidence_sentence or "not stated in source"

    return {
        "claim": claim,
        "evidence": evidence,
        "limitation": limitation,
        "takeaway": (
            "The source makes a claim, but its supporting evidence and "
            "limitations are not established in the provided text."
        ),
    }


if __name__ == "__main__":
    output = apply_low_evidence_skill(ARTICLE_D)

    print(f"--- {ARTICLE_D['title']} ---")
    for key, value in output.items():
        print(f"{key.title()}: {value}")

    print("\n=== No-fabrication check ===")
    no_evidence_fabricated = output["evidence"] == "not stated in source"
    no_limitation_fabricated = output["limitation"] == "not stated in source"

    print("Evidence correctly marked as not stated:", no_evidence_fabricated)
    print("Limitation correctly marked as not stated:", no_limitation_fabricated)
    print(
        "Conclusion:",
        "NO FABRICATION DETECTED"
        if no_evidence_fabricated and no_limitation_fabricated
        else "REVIEW REQUIRED",
    )
