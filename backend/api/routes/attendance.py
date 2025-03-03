from fastapi import  Depends, HTTPException,APIRouter ,File, UploadFile, Form
from sqlalchemy.orm import Session
from backend.database.crud import mark_attendance, get_attendance_by_student, get_all_attendance
from backend.api.dependencies import get_db
from backend.database.models import Hostel, Student

from pydantic import BaseModel
import shutil
import os
from geopy.distance import geodesic


router = APIRouter()

# ✅ Pydantic model for marking attendance
class AttendanceCreate(BaseModel):
    student_id: int
    status: str
    location_verified: bool
    face_verified: bool
    latitude: float
    longitude: float

# ✅ 6. GET all attendance records
@router.get("/")
def get_all_attendance_records(db: Session = Depends(get_db)):
    return {"attendance": get_all_attendance(db)}

# ✅ 7. GET attendance by student ID
@router.get("/{student_id}")
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    attendance = get_attendance_by_student(db, student_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return {"attendance": attendance}

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from backend.database.crud import mark_attendance
from backend.api.dependencies import get_db
from backend.face_recog_system import face_recog
from backend.database.crud import db_mark_attendance

UPLOAD_DIR = "backend/face_recog_system/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Hostel Location (NIT Jalandhar Coordinates)
HOSTEL_LOCATION = (31.3949, 75.5331)
ALLOWED_DISTANCE_METERS = 150  # 100 meters radius

@router.post("/mark")
def mark_attendance(
    token: str = Form(...),
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    db: Session = Depends(get_db)
):
    """Marks attendance if location and face recognition match."""
    # Get student from token
    student = get_student_from_token(token, db)
    if not student:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Hostel Location (NIT Jalandhar Coordinates)
    HOSTEL_LOCATION = (31.3949, 75.5331)  # ✅ Ensure this is correct
    ALLOWED_DISTANCE_METERS = 100  # ✅ Increase range if needed

    # Verify location
    student_location = (latitude, longitude)
    distance = geodesic(HOSTEL_LOCATION, student_location).meters

    print(f"📏 Calculated Distance: {distance} meters")  # ✅ Debugging log

    location_verified = distance <= ALLOWED_DISTANCE_METERS

    # Save uploaded image
    file_path = os.path.join(UPLOAD_DIR, f"{student.student_id}.png")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Perform face recognition
    recognized_name = face_recog.recognize_face(file_path)
    face_verified = recognized_name == student.name

    # Mark attendance if both checks pass
    if not location_verified:
        raise HTTPException(status_code=400, detail=f"Location verification failed. You are {distance:.2f}m away.")
    if not face_verified:
        raise HTTPException(status_code=400, detail="Face recognition failed")

    attendance_record = db_mark_attendance(
        db,
        student_id=student.student_id,
        status="Present",
        location_verified=location_verified,
        face_verified=face_verified,
        latitude=latitude,
        longitude=longitude
    )

    return {"message": "Attendance marked successfully", "attendance": attendance_record}



def get_student_from_token(token: str, db: Session):
    from backend.api.routes.auth import get_authenticated_student
    return get_authenticated_student(token, db)





