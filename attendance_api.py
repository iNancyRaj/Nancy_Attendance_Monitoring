from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from services.attendance_service import process_attendance_upload
import csv
from datetime import datetime, date
from services.db_service import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/upload-attendance", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload_attendance.html", {"request": request})

@router.post("/upload-attendance")
async def upload_image(request: Request, image: UploadFile = File(...)):
    teacher_id = int(request.cookies.get("teacher_id", "0"))
    results = await process_attendance_upload(image, teacher_id)
    return {
        "present_students": results["present"],
        "absent_students": results["absent"]
    }

@router.get("/attendance/export")
async def export_attendance(request: Request):
    teacher_id = int(request.cookies.get("teacher_id", "0"))
    today = date.today()
    attendance_data = db.fetch_all(
        "SELECT s.roll_number, s.name, a.status FROM attendance a JOIN students s ON a.student_id = s.id WHERE a.teacher_id = %s AND a.attendance_date = %s",
        (teacher_id, today)
    )

    filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Roll Number', 'Name', 'Attendance Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for student in attendance_data:
            writer.writerow({
                'Roll Number': student['roll_number'],
                'Name': student['name'],
                'Attendance Status': student['status']
            })
    return FileResponse(filename, media_type='text/csv', filename=filename)