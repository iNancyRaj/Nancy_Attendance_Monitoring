import os
import shutil
import face_recognition
from uuid import uuid4
from services.db_service import db

STUDENT_FACE_DIR = "known_faces"
os.makedirs(STUDENT_FACE_DIR, exist_ok=True)

async def register_student_with_photos(name, roll_number, photos):
    student_dir = os.path.join(STUDENT_FACE_DIR, roll_number)
    os.makedirs(student_dir, exist_ok=True)

    # Save photos and extract encodings
    for i, photo in enumerate(photos):
        content = await photo.read()
        filename = f"{i+1}.jpg"
        filepath = os.path.join(student_dir, filename)
        with open(filepath, "wb") as f:
            f.write(content)

    # Save student in DB
    db.execute(
        "INSERT INTO students (name, roll_number, photo_dir) VALUES (%s, %s, %s)",
        (name, roll_number, student_dir)
    )