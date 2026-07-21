from fastapi import APIRouter
from api.v1.endpoints import health, tasks, system, upload, ai, agentic, mcp, tools

api_v1_router = APIRouter(prefix="/api/v1")

# Register All API V1 Endpoints
api_v1_router.include_router(health.router)
api_v1_router.include_router(tasks.router)
api_v1_router.include_router(system.router)
api_v1_router.include_router(upload.router)
api_v1_router.include_router(ai.router)
api_v1_router.include_router(agentic.router)
api_v1_router.include_router(mcp.router)
api_v1_router.include_router(tools.router)