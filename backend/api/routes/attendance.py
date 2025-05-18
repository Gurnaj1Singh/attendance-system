from fastapi import  Depends, HTTPException, APIRouter, File, UploadFile, Form
from sqlalchemy.orm import Session
from backend.database.crud import get_attendance_by_student, get_all_attendance
from backend.api.dependencies import get_db
from backend.database.models import  Attendance, Hostel
from pydantic import BaseModel
from backend.api.routes.auth import get_authenticated_student
import shutil, os, json
from geopy.distance import geodesic
from backend.database.crud import db_mark_attendance
from sqlalchemy import func
from datetime import datetime
import face_recognition
import numpy as np



router = APIRouter()

class AttendanceCreate(BaseModel):
    student_id: int
    status: str
    location_verified: bool
    face_verified: bool
    latitude: float
    longitude: float

# 1. GET all attendance records
@router.get("/")
def get_all_attendance_records(db: Session = Depends(get_db)):
    return {"attendance": get_all_attendance(db)}

# 2. GET attendance by student ID
@router.get("/{student_id}")
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    attendance = get_attendance_by_student(db, student_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return {"attendance": attendance}



UPLOAD_DIR = "backend/api/routes/face_recog_system/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/mark")
def mark_attendance(
    token: str = Form(...),
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    db: Session = Depends(get_db)
):
    """Marks attendance if location and face recognition match, ensuring that
    a student can only mark attendance once per day."""

    # Step 1: Get student from token
    student = get_authenticated_student(token, db)
    if not student:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Step 2: Ensure attendance is not already marked for today
    today_date = datetime.utcnow().date()
    existing_attendance = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student.student_id,
            func.date(Attendance.date_time) == today_date
        )
        .first()
    )
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Attendance already marked for today")

    # Step 3: Location verification using DB
    hostel = db.query(Hostel).filter(Hostel.hostel_id == student.hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found for this student")

    HOSTEL_LOCATION = (float(hostel.latitude), float(hostel.longitude))
    student_location = (float(latitude), float(longitude))
    ALLOWED_DISTANCE_METERS = 100

    distance = geodesic(HOSTEL_LOCATION, student_location).meters
    print(f"📏 Calculated Distance from hostel: {distance:.2f} meters")

    location_verified = distance <= ALLOWED_DISTANCE_METERS
    if not location_verified:
        raise HTTPException(
            status_code=400,
            detail=f"Location verification failed. You are {distance:.2f}m away from your hostel."
        )

    # Step 4: Save uploaded image
    file_path = os.path.join(UPLOAD_DIR, f"{student.student_id}.png")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 5: Face verification using DB encoding
    if not student.face_data:
        raise HTTPException(status_code=400, detail="No face encoding found in database for this student")

    try:
        stored_encoding = np.array(json.loads(student.face_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid face encoding in DB: {str(e)}")

    image = face_recognition.load_image_file(file_path)
    face_encodings = face_recognition.face_encodings(image)
    if not face_encodings:
        raise HTTPException(status_code=400, detail="No face detected in uploaded image")

    face_verified = face_recognition.compare_faces([stored_encoding], face_encodings[0], tolerance=0.6)[0]
    if not face_verified:
        raise HTTPException(status_code=400, detail="Face recognition failed")

    # Step 6: Mark attendance
    attendance_record = db_mark_attendance(
        db,
        student_id=student.student_id,
        status="Present",
        location_verified=location_verified,
        face_verified=face_verified,
        latitude=latitude,
        longitude=longitude
    )

    return {"message": "✅ Attendance marked successfully", "attendance": attendance_record}


def get_student_from_token(token: str, db: Session):
    from backend.api.routes.auth import get_authenticated_student
    return get_authenticated_student(token, db)





