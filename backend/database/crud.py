from sqlalchemy.orm import Session
from backend.database.models import Student, Attendance, Fine, Notification, Hostel, Admin
from datetime import datetime
from geopy.distance import geodesic
from fastapi import HTTPException

# 📌 Create a Student
def create_student(db: Session, name: str, email: str, phone: str, room_number: int, hostel_id: int, emergency_contact: str, password: str):
    valid_hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if not valid_hostel:
        raise HTTPException(status_code=400, detail="Invalid hostel ID. Please choose a valid hostel.")
    new_student = Student(
        name=name,
        email=email,
        phone=phone,
        room_number=room_number,
        hostel_id=hostel_id,
        emergency_contact=emergency_contact,
        password=password  # Storing hashed password
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 📌 Get a Student by ID
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.student_id == student_id).first()

# 📌 Get a Student by Email (NEW FUNCTION)
def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

# 📌 Get All Students
def get_all_students(db: Session):
    return db.query(Student).all()

# 📌 Update Student Details
def update_student(db: Session, student_id: int, name: str = None, email: str = None, phone: str = None, room_number: int = None):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return None
    if name:
        student.name = name
    if email:
        student.email = email
    if phone:
        student.phone = phone
    if room_number:
        student.room_number = room_number
    db.commit()
    db.refresh(student)
    return student

# 📌 Delete a Student
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

# 📍 Hostel Coordinates (NIT Jalandhar)
HOSTEL_LOCATION = (31.3949, 75.5331)

# 🕗 Allowed Attendance Time: 8 PM - 10 PM IST
ATTENDANCE_START = 20  # 8 PM
ATTENDANCE_END = 22  # 10 PM

# ✅ Function to check if attendance is within allowed time
def is_valid_attendance_time():
    current_time = datetime.now().hour
    return ATTENDANCE_START <= current_time < ATTENDANCE_END

# ✅ Function to check if student's location is valid (within hostel area)
def is_location_valid(student_lat, student_lon):
    student_location = (student_lat, student_lon)
    distance = geodesic(HOSTEL_LOCATION, student_location).meters
    return distance <= 100  # Allowed range: 100 meters



# 📌 Mark Attendance
def mark_attendance(db: Session, student_id: int, status: str, location_verified: bool, face_verified: bool,latitude: float, longitude: float):
    attendance = Attendance(
        student_id=student_id,
        date_time=datetime.utcnow(),
        status=status,
        location_verified=location_verified,
        face_verified=face_verified,
        latitude=latitude,  # ✅ Store student latitude
        longitude=longitude  # ✅ Store student longitude
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

# 📌 Get Attendance for a Student
def get_attendance_by_student(db: Session, student_id: int):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()

# 📌 Apply Fine to Student
def apply_fine(db: Session, student_id: int, amount: float, due_date: datetime):
    fine = Fine(
        student_id=student_id,
        amount=amount,
        due_date=due_date
    )
    db.add(fine)
    db.commit()
    db.refresh(fine)
    return fine

# 📌 Get Pending Fines for a Student
def get_fines_by_student(db: Session, student_id: int):
    return db.query(Fine).filter(Fine.student_id == student_id, Fine.status == "Pending").all()

# 📌 Mark Fine as Paid
def pay_fine(db: Session, fine_id: int):
    fine = db.query(Fine).filter(Fine.fine_id == fine_id).first()
    if fine:
        fine.status = "Paid"
        db.commit()
        db.refresh(fine)
        return fine
    return None

# 📌 Send Notification
def send_notification(db: Session, student_id: int, message: str):
    notification = Notification(
        student_id=student_id,
        message=message,
        sent_at=datetime.utcnow(),
        status="Unread"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

# 📌 Get Notifications for a Student
def get_notifications(db: Session, student_id: int):
    return db.query(Notification).filter(Notification.student_id == student_id).all()

def get_all_attendance(db: Session):
    return db.query(Attendance).all()

from backend.database.models import Fine

# ✅ Get fines by student ID
def get_fines_by_student(db: Session, student_id: int):
    return db.query(Fine).filter(Fine.student_id == student_id).all()

# ✅ Mark a fine as paid
def pay_fine(db: Session, fine_id: int):
    fine = db.query(Fine).filter(Fine.fine_id == fine_id).first()
    if fine:
        fine.status = "Paid"
        db.commit()
        db.refresh(fine)
        return fine
    return None

from backend.database.models import Notification
from datetime import datetime

# ✅ Get notifications by student ID
def get_notifications(db: Session, student_id: int):
    return db.query(Notification).filter(Notification.student_id == student_id).all()

# ✅ Send a notification
def send_notification(db: Session, student_id: int, message: str):
    notification = Notification(
        student_id=student_id,
        message=message,
        sent_at=datetime.utcnow(),
        status="Unread"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

# ✅ Mark a notification as read
def mark_notification_as_read(db: Session, notification_id: int):
    notification = db.query(Notification).filter(Notification.notification_id == notification_id).first()
    if notification:
        notification.status = "Read"
        db.commit()
        db.refresh(notification)
        return notification
    return None

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def get_admin_by_username(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()

# 📌 Get Hostel Coordinates
def get_hostel_coordinates(db: Session, hostel_id: int):
    hostel = db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()
    if hostel:
        return {"latitude": hostel.latitude, "longitude": hostel.longitude}
    return None

def db_mark_attendance(
    db: Session,
    student_id: int,
    status: str,
    location_verified: bool,
    face_verified: bool,
    latitude: float,
    longitude: float
):
    """Stores the attendance record in the database."""
    attendance = Attendance(
        student_id=student_id,
        date_time=datetime.utcnow(),
        status=status,
        location_verified=location_verified,
        face_verified=face_verified,
        latitude=latitude,
        longitude=longitude
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance
