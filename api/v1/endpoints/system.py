from fastapi import APIRouter
from backend.services.system_monitor import system_monitor

router = APIRouter(prefix="/system", tags=["System Telemetry"])

@router.get("/stats")
async def get_system_stats():
    return system_monitor.get_system_stats()
