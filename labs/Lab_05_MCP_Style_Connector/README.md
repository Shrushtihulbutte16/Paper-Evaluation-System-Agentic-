# Lab 5 — MCP-Style Connector

## Objective
Build a mini integration layer through which a client discovers and invokes server capabilities using a structured manifest.

## Files
- `main.py` — reference server/client with a file resource, SQLite query tool, and mock API tool.
- `assignment_1.py` — adds a fourth discoverable resource, `list_files`, without hard-coding its name in the generic client.
- `assignment_2.py` — additional robustness exercise for manifest input validation and error handling.
- `test_output.txt` — captured output from all three scripts.

## Important note about the guide
The supplied Lab 5 pages list one formal assignment: add a fourth discoverable `list_files` resource. `assignment_2.py` is included as an additional practice extension, not as a second formally stated assignment in the guide.

## Requirements
- Python 3.10+
- SQLite support (included with standard Python installations)
- No third-party packages, API keys, or internet connection

## Run in VS Code terminal

```powershell
python main.py
python assignment_1.py
python assignment_2.py
```

## Concepts
1. **Capability manifest:** describes capability names, kinds, inputs, and outputs.
2. **Resource:** exposes data for reading, such as `read_file`.
3. **Tool:** performs an operation, such as a database query or API call.
4. **Discovery:** client asks the server for its manifest before invoking a capability.
5. **Authorization:** only approved callers may query the database.
6. **Input governance:** database access is restricted to SELECT statements.
7. **Structured response:** successful calls and failures return dictionaries.

## Architecture limitation
This is a local Python simulation of MCP-style discovery and invocation. It is not a standards-compliant MCP transport/server and does not communicate over a network. The database is in-memory and the API is mocked.
