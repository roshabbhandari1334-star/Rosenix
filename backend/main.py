import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add project root directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api.v1.router import api_v1_router
from backend.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Advanced Rosenix AI OS Backend Engine"
)

# Enable CORS for desktop app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API V1 Router
app.include_router(api_v1_router)

# Mount Frontend Static Files
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
os.makedirs(FRONTEND_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "J.A.R.V.I.S AI OS Backend Live. Frontend build pending."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=True)
