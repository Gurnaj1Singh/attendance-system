from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.database.crud import (
    get_all_students, get_student, create_student, update_student, delete_student, get_student_by_email
)
from backend.api.dependencies import get_db
from backend.database.models import Hostel, Student
from fastapi.security import OAuth2PasswordBearer
from backend.api.routes.auth import get_authenticated_student

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
    password: str

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/student-login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
def get_student_id_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        print(f"🔍 Received Token: {token}")  # ✅ Log the received token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        print(f"🔍 Extracted Email: {email}")  # ✅ Log extracted email

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        student = db.query(Student).filter(Student.email == email).first()

        print(f"🔍 Found Student: {student}")  # ✅ Log student object

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        print(f"✅ Returning Student ID: {student.student_id}")  # ✅ Log returned student ID

        return student.student_id

    except JWTError as e:
        print(f"❌ Token Decoding Error: {str(e)}")  # ✅ Log token decoding error
        raise HTTPException(status_code=401, detail="Invalid token")



@router.get("/me", tags=["Students"])
def get_current_student_details(
    student=Depends(get_authenticated_student),
    db: Session = Depends(get_db)
):
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
        "phone": student.phone,
        "room_number": student.room_number,
        "hostel_id": student.hostel_id,
        "emergency_contact": student.emergency_contact
    }
    
@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

