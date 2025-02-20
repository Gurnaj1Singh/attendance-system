from sqlalchemy.orm import sessionmaker
from db_connection import engine
from models import Hostel, Student, Attendance, Fine, Notification
from crud import (
    create_student, mark_attendance, apply_fine, send_notification
)
from datetime import datetime, timedelta

# Create a session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 🔹 1. Add Hostels
hostel1 = db.query(Hostel).filter_by(name="NIT Jalandhar Hostel").first()
if not hostel1:
    print("🏨 Adding hostels...")
    hostel1 = Hostel(name="NIT Jalandhar Hostel", location="Punjab, India")
    hostel2 = Hostel(name="Boys Hostel Block A", location="Jalandhar, Punjab")
    db.add_all([hostel1, hostel2])
    db.commit()
    print("✅ Hostels added!")

# 🔹 2. Add Students
students_data = [
    {"name": "John Doe", "email": "john@example.com", "phone": "9876543210", "room_number": 101, "hostel_id": hostel1.hostel_id, "emergency_contact": "Jane Doe - 9999999999"},
    {"name": "Alice Smith", "email": "alice@example.com", "phone": "9876543222", "room_number": 102, "hostel_id": hostel1.hostel_id, "emergency_contact": "Bob Smith - 8888888888"},
    {"name": "Bob Johnson", "email": "bob@example.com", "phone": "9876543233", "room_number": 103, "hostel_id": hostel1.hostel_id, "emergency_contact": "Alice Johnson - 7777777777"},
]

for student in students_data:
    if not db.query(Student).filter_by(email=student["email"]).first():
        create_student(db, **student)
        print(f"✅ Student {student['name']} added!")

# 🔹 3. Mark Attendance for Students
print("\n📌 Marking attendance...")
students = db.query(Student).all()
for student in students:
    attendance = mark_attendance(db, student.student_id, status="Present", location_verified=True, face_verified=True)
    print(f"✅ Attendance marked for {student.name} - {attendance.status}")

# 🔹 4. Apply Fines
print("\n💰 Applying fines...")
fine_due_date = datetime.utcnow() + timedelta(days=7)
for student in students[:2]:  # Apply fines to first two students
    fine = apply_fine(db, student.student_id, amount=500, due_date=fine_due_date)
    print(f"✅ Fine of ₹{fine.amount} applied to {student.name}, Due Date: {fine.due_date}")

# 🔹 5. Send Notifications
print("\n🔔 Sending notifications...")
for student in students:
    notification = send_notification(db, student.student_id, message="Reminder: Mark your attendance before 10 PM!")
    print(f"✅ Notification sent to {student.name}: {notification.message}")

# Close session
db.close()
print("\n🎉 Seeding complete!")
