from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {"status": "ONLINE", "service": "J.A.R.V.I.S. Core"}
