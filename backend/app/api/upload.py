print("UPLOAD.PY START")
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import save_file, process_file
import traceback

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()

        file_path = save_file(content, file.filename)
        results = process_file(file_path)

        return {
            "filename": file.filename,
            "analysis": {
                "document_summary": results["document_summary"],
                "clauses": results["clauses"][:10]
            }
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )