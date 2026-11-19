"""Assignment 2 — Deliberately break filter logic; independent tests must catch it."""


def requirement_agent():
    return [{
        "id": "US-1",
        "acceptance_criteria": [
            "CSV export produces a .csv file",
            "only rows matching applied filters are included",
            "CSV header matches visible columns",
        ],
    }]


def coding_agent(stories):
    # DELIBERATE BUG: inverted comparison includes rows that do NOT match.
    def export_endpoint(rows, applied_filters, columns):
        filtered = [
            row for row in rows
            if not all(row.get(key) == value for key, value in applied_filters.items())
        ]
        lines = [",".join(columns)]
        lines.extend(",".join(str(row.get(column, "")) for column in columns) for row in filtered)
        return "\n".join(lines)
    return {"export_endpoint": export_endpoint}


def testing_agent(stories):
    """Unchanged test logic: generated only from the user story's criteria."""
    criteria = stories[0]["acceptance_criteria"]

    def test_suite(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150},
        ]
        output = export_fn(rows, {"region": "North"}, ["region", "sales"])
        lines = output.splitlines()
        return [
            (criteria[0], len(output) > 0),
            (criteria[2], bool(lines) and lines[0] == "region,sales"),
            (criteria[1], len(lines) == 3 and all("South" not in line for line in lines[1:])),
        ]
    return test_suite


if __name__ == "__main__":
    stories = requirement_agent()
    code = coding_agent(stories)
    test_suite = testing_agent(stories)  # generated without access to code
    results = test_suite(code["export_endpoint"])

    print("=== Deliberate regression: inverted filter comparison ===")
    for name, passed in results:
        print(f" [{'PASS' if passed else 'FAIL'}] {name}")
    print("\nExpected evidence: the filtered-rows test fails because South is included.")
    assert any(not passed for _, passed in results), "The independent tests should catch the deliberate bug."
    print("Confirmed: independently-generated tests caught the regression.")
