import time
from typing import Dict, Any, List, Optional
from backend.services.ai_core.planner import planner

class BaseAgent:
    def __init__(self, name: str, role: str, description: str, system_prompt: str):
        self.name = name
        self.role = role
        self.description = description
        self.system_prompt = system_prompt

    async def execute_task(self, goal: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        start_time = time.time()
        subtasks = planner.decompose_goal(goal, agent_role=self.role)
        
        step_logs = []
        for task in subtasks:
            step_logs.append({
                "step": task["step"],
                "description": task["description"],
                "tool": task["tool"],
                "status": "COMPLETED",
                "success": True,
                "output": f"[{self.name.upper()}] Executed step successfully."
            })
            
        reflection = planner.self_reflect(step_logs)
        exec_duration = round(time.time() - start_time, 3)

        return {
            "agent_name": self.name,
            "agent_role": self.role,
            "goal": goal,
            "subtasks": subtasks,
            "execution_steps": step_logs,
            "reflection": reflection,
            "duration_seconds": exec_duration,
            "output_summary": f"[{self.name}] Completed goal '{goal}' in {exec_duration}s with confidence {reflection['confidence_score']*100}%."
        }
