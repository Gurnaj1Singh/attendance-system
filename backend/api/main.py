from fastapi import FastAPI
from backend.database.models import Base
from backend.database.db_connection import engine
from backend.api.routes import students, attendance , fines , notifications

# Initialize FastAPI app
app = FastAPI(title="Smart Hostel API", version="1.0")

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# ✅ Include route modules
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(fines.router, prefix="/fines", tags=["Fines"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
