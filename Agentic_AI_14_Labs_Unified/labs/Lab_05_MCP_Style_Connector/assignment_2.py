"""
Assignment 2 — Connector contract validation and failure handling.

This is an additional robustness exercise: the supplied Lab 5 guide
lists one formal assignment. This extension checks required inputs
against the manifest and returns clear errors for invalid requests.
"""
import sqlite3


CAPABILITIES = [
    {
        "name": "read_file",
        "kind": "resource",
        "input": {"path": "str"},
        "output": {"content": "str"},
    },
    {
        "name": "query_db",
        "kind": "tool",
        "input": {"sql": "str"},
        "output": {"rows": "list"},
    },
    {
        "name": "call_api",
        "kind": "tool",
        "input": {"endpoint": "str"},
        "output": {"data": "any"},
    },
]

MOCK_FILES = {"README.md": "Connector contract validation demo."}
MOCK_API = {"events_today": ["AI Club Talk"]}
ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")
        self.conn.execute("INSERT INTO signups VALUES ('AI Club Talk', 12)")
        self.conn.commit()

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": f"file not found: {path}"}
        return {"content": MOCK_FILES[path]}

    def query_db(self, sql, caller):
        if caller not in ALLOWED_CALLERS:
            return {"error": "caller is not authorized"}
        if not isinstance(sql, str) or not sql.strip().upper().startswith("SELECT"):
            return {"error": "only SELECT statements are permitted"}
        try:
            return {"rows": self.conn.execute(sql).fetchall()}
        except sqlite3.Error as error:
            return {"error": f"database query failed: {error}"}

    def call_api(self, endpoint):
        if endpoint not in MOCK_API:
            return {"error": f"unknown endpoint: {endpoint}"}
        return {"data": MOCK_API[endpoint]}


class MCPClient:
    def __init__(self, server, caller_name):
        self.server = server
        self.caller_name = caller_name

    def discover(self):
        return self.server.list_capabilities()

    def call(self, capability_name, **kwargs):
        manifest = {
            capability["name"]: capability
            for capability in self.discover()
        }

        if capability_name not in manifest:
            return {"error": f"unknown capability: {capability_name}"}

        schema = manifest[capability_name]["input"]
        missing = [key for key in schema if key not in kwargs]
        unexpected = [key for key in kwargs if key not in schema]

        if missing:
            return {"error": f"missing required input(s): {', '.join(missing)}"}
        if unexpected:
            return {"error": f"unexpected input(s): {', '.join(unexpected)}"}

        method = getattr(self.server, capability_name)
        if capability_name == "query_db":
            return method(caller=self.caller_name, **kwargs)
        return method(**kwargs)


if __name__ == "__main__":
    server = MCPServer()
    client = MCPClient(server, "planning_agent")

    print("=== Valid request ===")
    valid = client.call("read_file", path="README.md")
    print(valid)
    assert "content" in valid

    print("\n=== Missing required input ===")
    missing = client.call("read_file")
    print(missing)
    assert "missing required input" in missing["error"]

    print("\n=== Unexpected input ===")
    unexpected = client.call("read_file", path="README.md", mode="write")
    print(unexpected)
    assert "unexpected input" in unexpected["error"]

    print("\n=== Unknown capability ===")
    unknown = client.call("delete_everything")
    print(unknown)
    assert "unknown capability" in unknown["error"]

    print("\n=== Invalid SQL operation ===")
    invalid_sql = client.call("query_db", sql="DROP TABLE signups")
    print(invalid_sql)
    assert "only SELECT" in invalid_sql["error"]

    print("\nPASS: connector validates requests and reports failures clearly.")
