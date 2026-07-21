from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from backend.services.agentic_engine import agentic_engine
from backend.services.ai_core.memory import memory_engine
from backend.services.agents.specialized import AGENT_REGISTRY

router = APIRouter(prefix="/agentic", tags=["Agentic AI Bot Engine"])

class AgentGoalRequest(BaseModel):
    goal: str = Field(..., description="High level goal for the autonomous agent to solve")
    agent_role: Optional[str] = Field("manager", description="Specialized agent to assign (manager, coding, research, devops, security, browser)")

@router.post("/execute")
async def execute_goal(req: AgentGoalRequest):
    if not req.goal.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Goal cannot be empty.")
    
    result = await agentic_engine.execute_autonomous_goal(req.goal, agent_role=req.agent_role)
    return result

@router.get("/agents")
async def list_agents():
    agents = []
    for k, a in AGENT_REGISTRY.items():
        agents.append({
            "name": a.name,
            "role": a.role,
            "description": a.description
        })
    return {"agents": agents}

@router.get("/memory/stats")
async def get_memory_stats():
    return memory_engine.get_memory_stats()
