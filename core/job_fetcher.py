import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import io
from PyPDF2 import PdfReader
import docx

load_dotenv()

# Adzuna API credentials
APP_ID = os.getenv("app_id")
APP_KEY = os.getenv("app_key")
COUNTRY = "in"  # 'us' for USA, 'in' for India etc.

# Skill extraction (very basic for now, can improve)
SKILL_KEYWORDS = ["python", "java", "sql", "html", "css", "javascript", "aws", "react", "node", "django", "machine learning", "data science", "project management"]

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    text = text.lower()
    skills_found = [skill for skill in SKILL_KEYWORDS if skill in text]
    return skills_found

def search_jobs_adzuna(skills, location="Remote", page=1):
    results = []
    for skill in skills:
        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
        params = {
            "app_id":APP_ID,
            "app_key":APP_KEY,
            "what": skill,
            "where": location,
            "results_per_page": 10,
            "content-type": "application/json"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            jobs = response.json().get("results", [])
            for job in jobs:
                results.append({
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "salary": job.get("salary_is_predicted"),
                    "url": job.get("redirect_url")
                })
    return results
