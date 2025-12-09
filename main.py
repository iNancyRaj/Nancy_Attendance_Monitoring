from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from api import auth_api, student_api, attendance_api

app = FastAPI()

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="bc33f78ed797a1b6ade04b26d9d2cdb74e11d1ce8cbaa9244e1c1a46bdc80c6a",
)

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_api.router)
app.include_router(student_api.router)
app.include_router(attendance_api.router)