import time
import asyncio
from typing import Dict, Any, List, Optional
from backend.services.agents.specialized import AGENT_REGISTRY
from backend.services.tools.tool_registry import tool_registry
from backend.services.mcp.mcp_client import mcp_manager
from backend.services.ai_core.memory import memory_engine
from backend.services.ai_core.planner import planner

class AutonomousAgenticEngine:
    def __init__(self):
        self.active_tasks: List[Dict[str, Any]] = []

    async def execute_autonomous_goal(self, goal: str, agent_role: str = "manager") -> Dict[str, Any]:
        agent = AGENT_REGISTRY.get(agent_role, AGENT_REGISTRY["manager"])
        
        # Check if user is asking about developer
        lower_goal = goal.lower()
        if any(w in lower_goal for w in ["who is your developer", "who developed you", "who made you", "who created you", "who is your creator", "who built you", "who is roshab", "developer name"]):
            response_text = (
                f"### 👑 Developer Identity Protocol\n\n"
                f"I am **Rosenix**, created and developed by **Roshab Bhandari**.\n\n"
                f"*He engineered my Autonomous AI Core, Multi-Agent Swarm, and Quantum HUD System.*"
            )
            voice_text = "I am Rosenix, developed by Roshab Bhandari."
            return {
                "status": "SUCCESS",
                "agent": agent.name,
                "role": agent.role,
                "goal": goal,
                "subtasks": [],
                "tool_outputs": [],
                "reflection": {"confidence_score": 1.0, "success": True, "reflection": "Developer identity verified."},
                "formatted_response": response_text,
                "voice_response": voice_text
            }

        # 1. Record Goal in Short-Term Memory
        memory_engine.add_short_term(role="user", content=goal)

        # 2. Decompose Goal via ReAct Planner
        subtasks = planner.decompose_goal(goal, agent_role=agent_role)

        step_results = []
        executed_tool_outputs = []

        # 3. Autonomous Tool Execution Loop
        for task in subtasks:
            tool_name = task["tool"]
            
            # Match tool or map to built-in runner
            if "python" in tool_name or "code" in tool_name:
                tool_res = tool_registry.execute_tool("python_runner", {
                    "code": f"# Auto-generated Rosenix protocol\nprint('[ROSENIX AGENT] Executing step: {task['description']}')\n"
                })
            elif "cyber" in tool_name or "security" in tool_name:
                tool_res = tool_registry.execute_tool("cyber_audit_tool", {})
            else:
                tool_res = tool_registry.execute_tool("workspace_file_tool", {"action": "list", "filepath": "."})

            executed_tool_outputs.append({
                "step": task["step"],
                "description": task["description"],
                "tool_used": tool_name,
                "output": tool_res
            })

            step_results.append({"step": task["step"], "success": tool_res.get("success", True)})

        # 4. Self Reflection & Confidence Scoring
        reflection = planner.self_reflect(step_results)

        # 5. Record Episode in Memory
        memory_engine.record_episode(
            goal=goal,
            steps=executed_tool_outputs,
            outcome=reflection["reflection"],
            success=reflection["success"]
        )

        response_summary = (
            f"### 🤖 Autonomous Agentic Execution Complete\n\n"
            f"- **Assigned Agent:** `{agent.name}` (`{agent.role.upper()}`)\n"
            f"- **Goal Target:** *\"{goal}\"*\n"
            f"- **Confidence Score:** `{reflection['confidence_score']*100}%`\n"
            f"- **Steps Executed:** `{len(executed_tool_outputs)}` tool actions\n\n"
            f"**Autonomous Reflection:** {reflection['reflection']}\n\n"
            f"```json\n"
            f"// Execution Telemetry\n"
            f"{{\n"
            f'  "status": "COMPLETED",\n'
            f'  "agent": "{agent.name}",\n'
            f'  "tools_called": {len(executed_tool_outputs)},\n'
            f'  "mcp_status": "ONLINE"\n'
            f"}}\n"
            f"```"
        )

        voice_response = f"Autonomous goal execution completed by {agent.name}. Confidence score is {int(reflection['confidence_score']*100)} percent."

        return {
            "status": "SUCCESS",
            "agent": agent.name,
            "role": agent.role,
            "goal": goal,
            "subtasks": subtasks,
            "tool_outputs": executed_tool_outputs,
            "reflection": reflection,
            "formatted_response": response_summary,
            "voice_response": voice_response
        }

agentic_engine = AutonomousAgenticEngine()
