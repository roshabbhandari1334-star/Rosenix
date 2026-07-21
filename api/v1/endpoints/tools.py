from fastapi import APIRouter
from backend.services.tools.tool_registry import tool_registry

router = APIRouter(prefix="/tools", tags=["Tool Registry & Execution"])

@router.get("/list")
async def list_tools():
    return {"tools": tool_registry.list_tools()}

@router.post("/execute/{tool_name}")
async def execute_tool(tool_name: str, params: dict):
    return tool_registry.execute_tool(tool_name, params)
