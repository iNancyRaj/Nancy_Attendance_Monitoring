import os
import face_recognition
import io
from datetime import date
from services.db_service import db

def load_known_faces():
    known_encodings = []
    known_ids = []
    students = db.fetch_all("SELECT id, photo_dir FROM students")

    for student in students:
        photo_dir = student["photo_dir"]
        for img_file in os.listdir(photo_dir):
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(photo_dir, img_file)
                img = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_ids.append(student["id"])

    return known_encodings, known_ids

async def process_attendance_upload(file, teacher_id):
    image_bytes = await file.read()
    img = face_recognition.load_image_file(io.BytesIO(image_bytes))

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    known_encodings, known_ids = load_known_faces()
    present_ids = set()

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        if True in matches:
            match_index = matches.index(True)
            present_ids.add(known_ids[match_index])

    # Fetch all student IDs
    all_students = db.fetch_all("SELECT id, name, roll_number FROM students")
    today = date.today()

    present = []
    absent = []

    for student in all_students:
        is_present = student["id"] in present_ids
        db.execute(
            "INSERT INTO attendance (student_id, teacher_id, attendance_date, status) VALUES (%s, %s, %s, %s)",
            (student["id"], teacher_id, today, "Present" if is_present else "Absent")
        )
        if is_present:
            present.append(student)
        else:
            absent.append(student)

    return {
        "present": present,
        "absent": absent,
        "total": len(all_students)
    }