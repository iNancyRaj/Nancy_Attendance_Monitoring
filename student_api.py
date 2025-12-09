from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.student_service import register_student_with_photos
import os
from PIL import Image

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register-student", response_class=HTMLResponse)
def student_register_page(request: Request):
    return templates.TemplateResponse("student_register.html", {"request": request})

@router.post("/register-student")
async def student_register(
    request: Request,
    name: str = Form(...),
    roll_number: str = Form(...),
    photo1: UploadFile = File(...),
    photo2: UploadFile = File(None),
    photo3: UploadFile = File(None),
    photo4: UploadFile = File(None),
):
    photos = [photo for photo in [photo1, photo2, photo3, photo4] if photo and photo.file and photo.filename]
    await register_student_with_photos(name, roll_number, photos)

    # Create thumbnail for 1st image
    thumbnail_dir = "static/faces"
    os.makedirs(thumbnail_dir, exist_ok=True)
    thumbnail_path = f"{thumbnail_dir}/{roll_number}.jpg"
    image = Image.open(f"known_faces/{roll_number}/1.jpg")
    image = image.convert('RGB')
    image.thumbnail((100, 100))  # Resize to 100x100 pixels
    image.save(thumbnail_path)

    request.session["success_message"] = f"Student {name} with roll number {roll_number} registered successfully."
    request.session["roll_number"] = roll_number
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/dashboard")
async def dashboard(request: Request):
    success_message = request.session.pop("success_message", None)
    roll_number = request.session.pop("roll_number", None)
    return templates.TemplateResponse("dashboard.html", {"request": request, "success_message": success_message, "roll_number": roll_number})
