from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum, DECIMAL,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.db_connection import engine  
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 📌 Student Model
class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True)
    room_number = Column(Integer, nullable=False)
    hostel_id = Column(Integer, ForeignKey("hostels.hostel_id"))
    face_data = Column(Text)  # Stores face embeddings
    location_coordinates = Column(Text)
    emergency_contact = Column(String(100))
    password = Column(String(255), nullable=False)


    # Relationships
    hostel = relationship("Hostel", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    fines = relationship("Fine", back_populates="student", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="student", cascade="all, delete-orphan")

# 📌 Hostel Model
class Hostel(Base):
    __tablename__ = "hostels"

    hostel_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(Text, nullable=False)
    warden_id = Column(Integer, ForeignKey("admins.admin_id"))
    latitude = Column(Float, nullable=False)   
    longitude = Column(Float, nullable=False)

    # Relationships
    students = relationship("Student", back_populates="hostel")
    admin = relationship("Admin", back_populates="hostel")

# 📌 Admin Model (Fix)
class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("Warden", "Staff", name="admin_role"), nullable=False)
    email = Column(String(100), unique=True, nullable=True) 

    # Relationship
    hostel = relationship("Hostel", back_populates="admin")


# 📌 Attendance Model
class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum("Present", "Absent", "Late", name="attendance_status"), default="Absent")
    location_verified = Column(Boolean, default=False)
    face_verified = Column(Boolean, default=False)

    # ✅ NEW: Store student's live GPS coordinates for verification
    latitude = Column(Float, nullable=True)   # Stores student latitude
    longitude = Column(Float, nullable=True)  # Stores student longitude
    
    # Relationship
    student = relationship("Student", back_populates="attendance_records")

# 📌 Fine Model
class Fine(Base):
    __tablename__ = "fines"

    fine_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum("Pending", "Paid", name="fine_status"), default="Pending")
    due_date = Column(DateTime, nullable=False)

    # Relationship
    student = relationship("Student", back_populates="fines")

# 📌 Notification Model
class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum("Read", "Unread", name="notification_status"), default="Unread")

    # Relationship
    student = relationship("Student", back_populates="notifications")

# Create all tables
Base.metadata.create_all(engine)

