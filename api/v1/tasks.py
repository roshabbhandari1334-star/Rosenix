from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

router = APIRouter(prefix="/tasks", tags=["Agent Execution Engine"])

# Request Model: What the user sends
class TaskCreate(BaseModel):
    goal: str = Field(..., description="The high-level prompt or goal for Roshab AI", example="Scrape top news and write a summary report")
    agent_type: Optional[str] = Field("manager", description="Specialized agent to assign (manager, coding, research, devops)", example="manager")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context or tool configuration")

# Response Model: What Roshab AI returns
class TaskResponse(BaseModel):
    task_id: str
    status: str
    goal: str
    assigned_agent: str
    message: str

@router.post(
    "/execute",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a task/goal to Roshab AI"
)
async def submit_task(task_in: TaskCreate):
    if not task_in.goal.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal description cannot be empty."
        )

    task_id = str(uuid.uuid4())
    
    # In a full setup, this task is queued and processed by the AI Brain Engine
    return TaskResponse(
        task_id=task_id,
        status="PROCESSING",
        goal=task_in.goal,
        assigned_agent=task_in.agent_type,
        message=f"Goal received. Assigned to {task_in.agent_type.upper()} agent."
    )