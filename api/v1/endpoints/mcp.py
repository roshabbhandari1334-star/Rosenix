from fastapi import APIRouter
from backend.services.mcp.mcp_client import mcp_manager

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol (MCP)"])

@router.get("/servers")
async def list_mcp_servers():
    return {"servers": mcp_manager.list_mcp_servers()}

@router.post("/connect")
async def connect_mcp_server(uri: str):
    return mcp_manager.discover_and_connect(uri)
