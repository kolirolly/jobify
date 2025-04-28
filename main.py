from fastapi import FastAPI, Request, UploadFile, Form,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from services.resume_feedback import get_resume_feedback,apply_feedback
from services.convert_to_markdown import markdown_to_pdf
from v1.routes import upload_pdf
import os
from pydantic import BaseModel


app = FastAPI()

app.include_router(upload_pdf.router)
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/js", StaticFiles(directory="/etc/secrets/"),name="js")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/landing", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/upload_resume")
def resume_upload_template(resquest:Request):
    return templates.TemplateResponse("upload-resume.html",{"request":resquest})


@app.get("/feedback")
def feedback(request:Request,path):
    with open(f"uploads/{path}.md") as f:
        feedback_array = get_resume_feedback(f.read())
    return templates.TemplateResponse("feedback.html",{"request":request,"feedback":feedback_array})


class FeedbackRequest(BaseModel):
    path: str
    preferences: list[str]


@app.post("/apply_feedback")
def apply_feedback_(payload: FeedbackRequest):
    path = payload.path
    selected_preferences = payload.preferences
    print("fddfs",path)
    with open(f"uploads/{path}.md") as f:
        updated_resume = apply_feedback(f.read(), selected_preferences)
        os.makedirs("pdfs", exist_ok=True)
        # print("hehe",updated_resume)
        if markdown_to_pdf(updated_resume,f"pdfs/{path}.pdf"):
            return {"filename": f"pdfs/{path}.pdf"}
        else:
            return HTMLResponse({"error","error Occurred"})


@app.get("/download")
def download_resume(path:str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path, media_type="application/pdf", filename=os.path.basename(path)
    )
