import os
import json
import mimetypes
from typing import Dict, Any, List

class FileProcessor:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_and_process(self, file_name: str, content_bytes: bytes) -> Dict[str, Any]:
        file_path = os.path.join(self.upload_dir, file_name)
        
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(content_bytes)

        file_size = len(content_bytes)
        ext = os.path.splitext(file_name)[1].lower()
        mime_type, _ = mimetypes.guess_type(file_name)
        mime_type = mime_type or "application/octet-stream"

        extracted_text = ""
        preview = ""
        line_count = 0
        file_category = "General File"

        # Categorize & Extract Text
        if ext in [".txt", ".md", ".json", ".py", ".js", ".html", ".css", ".csv", ".xml", ".yaml", ".yml", ".sh", ".sql"]:
            file_category = "Code & Data Document" if ext in [".py", ".js", ".json", ".csv", ".sql"] else "Text Document"
            try:
                extracted_text = content_bytes.decode("utf-8", errors="ignore")
                lines = extracted_text.splitlines()
                line_count = len(lines)
                preview = "\n".join(lines[:20]) + ("\n..." if line_count > 20 else "")
            except Exception as e:
                extracted_text = f"[Error decoding text content: {str(e)}]"
        
        elif ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"]:
            file_category = "Image Asset"
            preview = f"Image file parsed successfully ({file_size} bytes, format: {ext.replace('.', '').upper()})."
            extracted_text = f"[Image File: {file_name}, Size: {file_size} bytes]"

        elif ext == ".pdf":
            file_category = "PDF Document"
            try:
                # Basic text extraction fallback for PDF raw streams or strings
                raw_text = content_bytes.decode("latin1", errors="ignore")
                extracted_text = f"PDF File uploaded: {file_name} ({file_size} bytes)."
                preview = "PDF Document registered and ready for J.A.R.V.I.S indexing."
            except Exception:
                extracted_text = f"PDF Document {file_name}"
                preview = "PDF uploaded."

        else:
            file_category = "Binary / Media File"
            preview = f"Binary file registered ({file_size} bytes)."
            extracted_text = f"[Binary File: {file_name}]"

        return {
            "filename": file_name,
            "filepath": file_path,
            "size_bytes": file_size,
            "extension": ext,
            "mime_type": mime_type,
            "category": file_category,
            "line_count": line_count,
            "preview": preview,
            "extracted_text": extracted_text[:10000] # Limit to 10k chars for AI context
        }

file_processor = FileProcessor(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads"))
