from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.db_connection import engine
from backend.database.models import Base, Admin
from backend.api.dependencies import get_db
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

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

# ✅ 1. Signup - Create an Admin User
@router.post("/signup")
def create_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    # ✅ Check if email is empty or missing
    if not admin_data.email:
        raise HTTPException(status_code=400, detail="Email is required")

    # ✅ Check if an admin with the same email already exists
    existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    # ✅ Hash password before storing
    hashed_password = pwd_context.hash(admin_data.password)

    # ✅ Insert into the database
    new_admin = Admin(
        username=admin_data.username,
        email=admin_data.email,  # ✅ Ensure email is included
        password=hashed_password,
        role=admin_data.role
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin created successfully"}

# ✅ 2. Login - Authenticate and Get JWT Token

@router.post("/login")
def login_admin(admin_data: AdminLogin, db: Session = Depends(get_db)):
    # ✅ Find admin by username
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    if not admin:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # ✅ Verify password
    if not pwd_context.verify(admin_data.password, admin.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # ✅ Generate JWT token
    token = create_access_token({"sub": admin.username, "role": admin.role})

    return {"access_token": token, "token_type": "bearer"}

# ✅ 3. Verify Token - Protect Routes
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return db.query(Admin).filter(Admin.username == username).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
