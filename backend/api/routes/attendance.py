from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.crud import mark_attendance, get_attendance_by_student, get_all_attendance
from backend.api.dependencies import get_db
from pydantic import BaseModel

router = APIRouter()

# ✅ Pydantic model for marking attendance
class AttendanceCreate(BaseModel):
    student_id: int
    status: str
    location_verified: bool
    face_verified: bool

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

# ✅ 8. POST - Mark attendance
@router.post("/")
def mark_student_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    if attendance.status not in ["Present", "Absent", "Late"]:
        raise HTTPException(status_code=400, detail="Invalid attendance status")
    
    new_attendance = mark_attendance(
        db,
        student_id=attendance.student_id,
        status=attendance.status,
        location_verified=attendance.location_verified,
        face_verified=attendance.face_verified
    )
    
    return {"message": "Attendance marked successfully", "attendance": new_attendance}
