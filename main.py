from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/upload_resume")
def resume_upload_template(resquest:Request):
    return templates.TemplateResponse("upload-resume.html",{"request":resquest})

@app.get("/feedback")
def feedback_form(resquest:Request):
    return templates.TemplateResponse("feedback.html",{"request":resquest})

    
