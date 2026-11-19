"""
Assignment 1 — Add a fourth, discoverable capability: list_files.

Important requirement:
MCPClient must not contain the literal capability name "list_files".
The new capability is added to the manifest and implemented on the server;
the existing generic client dispatch discovers it automatically.
"""
import sqlite3


MOCK_FILES = {
    "README.md": "Mini MCP server demonstration.",
    "notes.txt": "Project notes for the campus planning agent.",
    "events.csv": "event,count\nAI Club Talk,12\nRobotics Demo,15",
}

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
    {
        "name": "list_files",
        "kind": "resource",
        "input": {},
        "output": {"files": "list"},
    },
]

ALLOWED_CALLERS = {"planning_agent"}


class MCPServer:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE signups (event TEXT, count INTEGER)")
        self.conn.executemany(
            "INSERT INTO signups VALUES (?, ?)",
            [("AI Club Talk", 12), ("Robotics Demo", 15)],
        )
        self.conn.commit()

    def list_capabilities(self):
        return CAPABILITIES

    def read_file(self, path):
        if path not in MOCK_FILES:
            return {"error": f"file not found: {path}"}
        return {"content": MOCK_FILES[path]}

    def query_db(self, sql, caller):
        if caller not in ALLOWED_CALLERS:
            return {"error": f"caller '{caller}' is not permitted"}
        if not isinstance(sql, str) or not sql.strip().upper().startswith("SELECT"):
            return {"error": "only SELECT statements are permitted"}
        try:
            return {"rows": self.conn.execute(sql).fetchall()}
        except sqlite3.Error as error:
            return {"error": str(error)}

    def call_api(self, endpoint):
        if endpoint == "events_today":
            return {"data": ["AI Club Talk", "Robotics Demo"]}
        return {"error": f"unknown endpoint: {endpoint}"}

    def list_files(self):
        return {"files": sorted(MOCK_FILES.keys())}


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
            raise ValueError(f"unknown capability: {capability_name}")

        method = getattr(self.server, capability_name)
        if capability_name == "query_db":
            return method(caller=self.caller_name, **kwargs)
        return method(**kwargs)


if __name__ == "__main__":
    server = MCPServer()
    client = MCPClient(server, "planning_agent")

    print("=== Dynamically discovered capabilities ===")
    for capability in client.discover():
        print(f"{capability['name']} ({capability['kind']})")

    print("\n=== Invoke newly added capability ===")
    result = client.call("list_files")
    print("Input: {}")
    print("Output:", result)

    assert result["files"] == sorted(MOCK_FILES.keys())
    print("PASS: new resource was discovered and invoked through generic dispatch.")
