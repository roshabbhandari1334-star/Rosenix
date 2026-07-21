from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from backend.services.ai_brain import ai_brain

router = APIRouter(prefix="/ai", tags=["J.A.R.V.I.S. AI Engine"])

class CommandRequest(BaseModel):
    prompt: str = Field(..., description="Voice or text command prompt for JARVIS")
    voice_input: Optional[bool] = Field(False, description="Flag indicating if command originated from voice")

class CommandResponse(BaseModel):
    status: str
    prompt: str
    response: str
    voice_response: str
    intent: str
    action_type: Optional[str] = None
    file_info: Optional[Dict[str, Any]] = None

@router.post("/command", response_model=CommandResponse)
async def process_ai_command(req: CommandRequest):
    if not req.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt cannot be empty."
        )

    res = await ai_brain.process_command(req.prompt)
    return CommandResponse(
        status="SUCCESS",
        prompt=req.prompt,
        response=res["response"],
        voice_response=res["voice_response"],
        intent=res["intent"],
        action_type=res.get("action_type"),
        file_info=res.get("file_info")
    )
