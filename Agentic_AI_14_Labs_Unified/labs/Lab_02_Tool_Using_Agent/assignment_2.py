"""
Lab 2 — Assignment 2: A Three-Tool Chain

Adds an event category to the CSV and answers:
"What's the average sign-up for technical events only?"

The three steps are:
1. Read the CSV.
2. Filter rows to category == "technical".
3. Validate the filtered result, then calculate its average.
"""

import csv
import io


CATEGORY_SIGNUPS_CSV = """event,signups,category
AI Club Talk,12,technical
Hackathon Kickoff,9,technical
Robotics Demo,15,technical
GenAI Workshop,7,technical
Capstone Expo,20,social
Career Panel,11,social
"""


def read_csv_with_category(source_text=CATEGORY_SIGNUPS_CSV):
    reader = csv.DictReader(io.StringIO(source_text))
    rows = list(reader)

    if not rows:
        return {"error": "empty file", "rows": [], "row_count": 0}

    required = {"event", "signups", "category"}
    if not required.issubset(reader.fieldnames or []):
        return {"error": "CSV is missing required columns"}

    return {"rows": rows, "row_count": len(rows)}


def filter_by_category(rows, category):
    filtered = [
        row for row in rows
        if row["category"].strip().lower() == category.strip().lower()
    ]
    return {"rows": filtered, "row_count": len(filtered)}


def calculator(operation, values):
    if operation == "average":
        if not values:
            return {"error": "no values supplied"}
        return {"result": sum(values) / len(values)}

    if operation == "sum":
        return {"result": sum(values)}

    return {"error": f"unsupported operation: {operation}"}


class CategoryCampusAssistant:
    def __init__(self):
        self.trace = []
        self.tools = {
            "read_csv": read_csv_with_category,
            "filter_by_category": filter_by_category,
            "calculator": calculator,
        }

    def call_tool(self, tool_name, reason, **kwargs):
        if tool_name not in self.tools:
            raise ValueError(f"unknown tool: {tool_name}")

        result = self.tools[tool_name](**kwargs)
        self.trace.append({
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result,
        })

        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"{tool_name} failed: {result['error']}")

        return result

    def average_for_category(self, category):
        # Step 1: Read the source CSV.
        csv_result = self.call_tool(
            "read_csv",
            "event sign-ups and categories are stored in the CSV",
        )

        # Step 2: Filter rows by the requested category.
        filtered_result = self.call_tool(
            "filter_by_category",
            f"select only events categorized as '{category}'",
            rows=csv_result["rows"],
            category=category,
        )

        # Validate before passing values to the calculator.
        if filtered_result["row_count"] == 0:
            return f"No events found in category '{category}'."

        values = [int(row["signups"]) for row in filtered_result["rows"]]

        # Step 3: Calculate the average for the filtered subset.
        average_result = self.call_tool(
            "calculator",
            "compute average only over the validated filtered subset",
            operation="average",
            values=values,
        )

        return (
            f"Average sign-ups for {category} events: "
            f"{average_result['result']:.2f} "
            f"(across {filtered_result['row_count']} events)."
        )


if __name__ == "__main__":
    assistant = CategoryCampusAssistant()

    question = "What's the average sign-up for technical events only?"
    print("Q:", question)
    print("A:", assistant.average_for_category("technical"))

    print("\n=== Three-step tool trace ===")
    for index, entry in enumerate(assistant.trace, 1):
        print(f"{index}. tool={entry['tool']}")
        print(f"   reason={entry['reason']}")
        print(f"   input={entry['input']}")
        print(f"   output={entry['output']}")

    print("\n=== Empty-category validation test ===")
    empty_assistant = CategoryCampusAssistant()
    print(empty_assistant.average_for_category("arts"))
    print("Calculator called after empty filter:",
          any(item["tool"] == "calculator" for item in empty_assistant.trace))
