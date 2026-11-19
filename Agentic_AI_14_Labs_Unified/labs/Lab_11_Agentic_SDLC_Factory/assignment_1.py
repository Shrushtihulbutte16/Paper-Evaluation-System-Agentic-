"""Assignment 1 — Two concurrent stories: CSV and PDF export."""

import csv
import io


def requirement_agent():
    return [
        {
            "id": "US-1",
            "format": "csv",
            "text": "Export the filtered report as CSV.",
            "acceptance_criteria": [
                "CSV export produces comma-separated content",
                "CSV export preserves applied filters",
            ],
        },
        {
            "id": "US-2",
            "format": "pdf",
            "text": "Export the same filtered report as PDF in addition to CSV.",
            "acceptance_criteria": [
                "PDF export produces a PDF document",
                "PDF export preserves applied filters",
            ],
        },
    ]


def design_agent(story):
    if story["format"] == "csv":
        components = ["csv_export_endpoint", "csv_serializer"]
    else:
        components = ["pdf_export_endpoint", "pdf_document_builder"]
    return {"story_id": story["id"], "format": story["format"], "components": components}


def _make_minimal_pdf(lines):
    """Create a small valid one-page PDF using only Python's standard library."""
    escaped = [line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") for line in lines]
    stream = "BT /F1 11 Tf 50 760 Td " + " ".join(
        f"({line}) Tj 0 -16 Td" for line in escaped
    ) + " ET"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("latin-1")
    )
    return bytes(output)


def coding_agent(story, design):
    def export(rows, filters, columns):
        filtered = [row for row in rows if all(row.get(k) == v for k, v in filters.items())]
        if story["format"] == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer, lineterminator="\n")
            writer.writerow(columns)
            writer.writerows([[row.get(column, "") for column in columns] for row in filtered])
            return buffer.getvalue()
        lines = ["Filtered report"] + [
            " | ".join(str(row.get(column, "")) for column in columns) for row in filtered
        ]
        return _make_minimal_pdf(lines)

    return {"story_id": story["id"], "design_ref": design["components"], "export": export}


def testing_agent(story):
    """Tests depend only on this story's acceptance criteria, never on generated code."""
    criteria = story["acceptance_criteria"]

    def tests(export_fn):
        rows = [{"region": "North", "sales": 10}, {"region": "South", "sales": 20}]
        result = export_fn(rows, {"region": "North"}, ["region", "sales"])
        if story["format"] == "csv":
            passed = result.splitlines() == ["region,sales", "North,10"]
        else:
            passed = result.startswith(b"%PDF-") and b"North" in result and b"South" not in result
        return [(criteria[0], passed), (criteria[1], passed)]

    return tests


if __name__ == "__main__":
    stories = requirement_agent()
    print("=== Two concurrent stories ===")
    for story in stories:
        design = design_agent(story)
        code = coding_agent(story, design)
        test_factory = testing_agent(story)  # no code passed while tests are authored
        results = test_factory(code["export"])
        print(f"\n{story['id']} ({story['format'].upper()}): {story['text']}")
        print(f"Design: {design}")
        print(f"Tests: {results}")
        print(f"Lineage: design <- {story['id']}; code <- {story['id']}; tests <- {story['id']} [independent]")
        assert all(passed for _, passed in results)
