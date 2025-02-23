from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.db_connection import engine
from backend.database.models import Base, Admin, Student  # Fixed import
from backend.api.dependencies import get_db
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from backend.database.crud import (
    get_student_by_email, create_student
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Secret key & algorithm for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Pydantic models
class AdminCreate(BaseModel):
    username: str
    password: str
    role: str
    email: EmailStr

class AdminLogin(BaseModel):
    username: str
    password: str

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    room_number: int
    hostel_id: int
    emergency_contact: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ 1. Admin Signup
@router.post("/signup")
def create_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    if not admin_data.email:
        raise HTTPException(status_code=400, detail="Email is required")

    existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    hashed_password = hash_password(admin_data.password)

    new_admin = Admin(
        username=admin_data.username,
        email=admin_data.email,
        password=hashed_password,
        role=admin_data.role
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin created successfully"}

# ✅ 2. Admin Login
@router.post("/login")
def login_admin(admin_data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if not admin or not verify_password(admin_data.password, admin.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({"sub": admin.username, "role": admin.role})
    return {"access_token": token, "token_type": "bearer"}

# ✅ 3. Student Signup
@router.post("/student-signup")
def create_student_account(student_data: StudentCreate, db: Session = Depends(get_db)):
    if not student_data.email:
        raise HTTPException(status_code=400, detail="Email is required")

    existing_student = get_student_by_email(db, student_data.email)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email already exists")

    hashed_password = hash_password(student_data.password)

    new_student = create_student(db, **student_data.dict(exclude={"password"}), password=hashed_password)

    return {"message": "Student account created successfully"}

# ✅ 4. Student Login
@router.post("/student-login")
def student_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    student = get_student_by_email(db, form_data.username)
    if not student or not verify_password(form_data.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": student.email, "role": "student"})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ 5. Verify Token - Protect Student Routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/student-login")

def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        student = get_student_by_email(db, email)
        if student is None:
            raise HTTPException(status_code=401, detail="Student not found")
        return student
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2x_scheme = OAuth2PasswordBearer(tokenUrl="/auth/admin-login")

def get_current_admin(token: str = Depends(oauth2x_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return db.query(Admin).filter(Admin.username == username).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
