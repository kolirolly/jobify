from fastapi import UploadFile
from fastapi import APIRouter
from core import resume_parser

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    text = await resume_parser.extract_text(file)
    return {"filename": text}