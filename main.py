from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from v1.routes import upload_pdf

app = FastAPI()

app.include_router(upload_pdf.router)
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/upload_resume")
def resume_upload_template(resquest:Request):
    return templates.TemplateResponse("upload-resume.html",{"request":resquest})


    
