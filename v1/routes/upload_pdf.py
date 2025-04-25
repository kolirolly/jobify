from fastapi import UploadFile
from fastapi import APIRouter
from core import resume_parser
from fastapi.exceptions import HTTPException
import uuid
import os

router = APIRouter()


@router.post("/upload_resume/")
async def create_upload_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    id = uuid.uuid4()
    path = "uploads"
    os.makedirs(path, exist_ok=True)
    content = await file.read()
    with open(f"{path}/{id}","wb") as f:
        f.write(content)
    text = await resume_parser.extract_text(content)
    return {"filename": text}
