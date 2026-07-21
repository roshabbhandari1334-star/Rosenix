from fastapi import APIRouter, UploadFile, File, HTTPException, status
from backend.services.file_processor import file_processor
from backend.services.ai_brain import ai_brain

router = APIRouter(prefix="/upload", tags=["File Processing Engine"])

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a valid filename."
        )

    try:
        content = await file.read()
        processed_info = await file_processor.save_and_process(file.filename, content)
        ai_brain.register_uploaded_file(processed_info)
        
        return {
            "status": "SUCCESS",
            "message": f"File '{file.filename}' uploaded and analyzed successfully.",
            "file": processed_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file upload: {str(e)}"
        )
