from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.crud import (
    get_all_students, get_student, create_student, update_student, delete_student
)
from backend.api.dependencies import get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# ✅ Pydantic models for validation
class StudentCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    room_number: int
    hostel_id: int
    emergency_contact: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    room_number: Optional[int] = None

# ✅ 1. GET all students
@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return {"students": get_all_students(db)}

# ✅ 2. GET a student by ID
@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ✅ 3. POST - Add a new student
@router.post("/")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    return {"message": "Student added successfully", "student": create_student(db, **student.dict())}

# ✅ 4. PUT - Update student details
@router.put("/{student_id}")
def modify_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, **student_update.dict(exclude_unset=True))
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully", "student": updated_student}

# ✅ 5. DELETE - Remove a student
@router.delete("/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    if not delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
