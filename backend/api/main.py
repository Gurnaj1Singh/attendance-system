from fastapi import FastAPI
from backend.database.models import Base
from backend.database.db_connection import engine
from backend.api.routes import students, attendance , fines , notifications, auth 
from backend.api.routes.face_recog_system import main as face_recog_router

app = FastAPI(title="Attendance API", version="1.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include route modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(face_recog_router.router, prefix="/face_recog", tags=["Face Recognition"])

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(fines.router, prefix="/fines", tags=["Fines"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])



