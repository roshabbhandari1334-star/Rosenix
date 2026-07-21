import time
from typing import Dict, Any, List
from backend.services.tools.builtin_tools import builtin_tools

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {
            "python_runner": {
                "name": "python_runner",
                "category": "Coding",
                "description": "Executes Python code dynamically with output and error capture.",
                "permissions": "EXECUTE",
                "status": "HEALTHY",
                "calls_count": 0
            },
            "workspace_file_tool": {
                "name": "workspace_file_tool",
                "category": "File Manager",
                "description": "Reads, writes, lists, and manages project files in workspace.",
                "permissions": "READ_WRITE",
                "status": "HEALTHY",
                "calls_count": 0
            },
            "cyber_audit_tool": {
                "name": "cyber_audit_tool",
                "category": "Security",
                "description": "Performs defensive security audits and vulnerability sanity checks.",
                "permissions": "READ_ONLY",
                "status": "HEALTHY",
                "calls_count": 0
            }
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        return list(self.tools.values())

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tools:
            return {"success": False, "error": f"Tool '{tool_name}' not found in registry."}

        self.tools[tool_name]["calls_count"] += 1

        if tool_name == "python_runner":
            code = params.get("code", "print('J.A.R.V.I.S. Core Test')")
            return builtin_tools.execute_python_code(code)

        elif tool_name == "workspace_file_tool":
            action = params.get("action", "list")
            filepath = params.get("filepath", ".")
            content = params.get("content", "")
            return builtin_tools.manage_file_workspace(action, filepath, content)

        elif tool_name == "cyber_audit_tool":
            return builtin_tools.defensive_cyber_audit()

        return {"success": True, "message": f"Executed tool '{tool_name}' successfully."}

tool_registry = ToolRegistry()
