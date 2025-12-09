from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import authenticate_teacher, hash_password
from services.db_service import db
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    teacher = authenticate_teacher(email, password)
    if teacher:
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("teacher_id", str(teacher["id"]))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    teacher_id = request.cookies.get("teacher_id")
    if not teacher_id:
        return RedirectResponse(url="/")
    teacher = db.fetch_one("SELECT name FROM teachers WHERE id = %s", (teacher_id,))
    return templates.TemplateResponse("dashboard.html", {"request": request, "teacher": teacher})

@router.post("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("teacher_id")
    return response

@router.get("/signup")
async def get_signup(request: Request):
    subjects = db.fetch_all("SELECT * FROM subjects")
    return templates.TemplateResponse("teacher_signup.html", {"request": request, "subjects": subjects})

@router.post("/signup")
async def post_signup(request: Request, email: str = Form(...), name: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), subjects: List[str] = Form(...)):
    if password != confirm_password:
        subjects = db.fetch_all("SELECT * FROM subjects")
        return templates.TemplateResponse("teacher_signup.html", {"request": request, "subjects": subjects, "message": "Passwords do not match"})

    hashed_password = hash_password(password)
    try:
        existing_teacher = db.fetch_one("SELECT id FROM teachers WHERE email = %s", (email,))
        if existing_teacher:
            teacher_id = existing_teacher['id']
        else:
            db.execute("INSERT INTO teachers (email, password, name) VALUES (%s, %s, %s)", (email, hashed_password.decode('utf-8'), name))
            teacher_id = db.fetch_one("SELECT LAST_INSERT_ID() as id")['id']

        for subject_id in subjects:
            db.execute("INSERT INTO teacher_subjects (teacher_id, subject_id) VALUES (%s, %s)", (teacher_id, subject_id))
        return templates.TemplateResponse("login.html", {"request": request, "message": "Teacher signed up successfully"})
    except Exception as e:
        subjects = db.fetch_all("SELECT * FROM subjects")
        return templates.TemplateResponse("teacher_signup.html", {"request": request, "subjects": subjects, "message": "Error signing up teacher"})

