from services.db_service import db
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_teacher(email, password):
    teacher = db.fetch_one("SELECT * FROM teachers WHERE email = %s", (email,))
    if teacher and verify_password(password, teacher['password']):
        return teacher
    return None