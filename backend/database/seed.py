from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from db_connection import engine
from models import Admin, Hostel, Student, Attendance, Fine, Notification
from crud import create_student, mark_attendance, apply_fine, send_notification

# Create a session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 🔹 1. Add Admins
admins = [
    {"username": "warden", "email": "warden@hostel.com", "password": "wardenpass", "role": "Warden"},
    {"username": "staff", "email": "staff@hostel.com", "password": "staffpass", "role": "Staff"}
]
for admin_data in admins:
    existing_admin = db.query(Admin).filter_by(email=admin_data["email"]).first()
    if not existing_admin:
        admin = Admin(**admin_data)
        db.add(admin)
db.commit()
print("✅ Admins added!")

# 🔹 2. Add Hostels with GPS Coordinates
hostels = [
    {"name": "NIT Jalandhar Hostel", "location": "Punjab, India", "latitude": 31.3949, "longitude": 75.5331},
    {"name": "Boys Hostel Block A", "location": "Jalandhar, Punjab", "latitude": 31.3951, "longitude": 75.5340}
]
for hostel_data in hostels:
    existing_hostel = db.query(Hostel).filter_by(name=hostel_data["name"]).first()
    if not existing_hostel:
        hostel = Hostel(**hostel_data)
        db.add(hostel)
db.commit()
print("✅ Hostels added!")

# ✅ Fetch hostel IDs after committing
hostel_nit = db.query(Hostel).filter_by(name="NIT Jalandhar Hostel").first()
hostel_boys = db.query(Hostel).filter_by(name="Boys Hostel Block A").first()

# 🔹 3. Add Students (Use Fetched Hostel IDs)
students = [
    {"name": "John Doe", "email": "john@example.com", "phone": "9876543210", "room_number": 101, "hostel_id": hostel_nit.hostel_id, "emergency_contact": "Jane Doe - 9999999999", "password": "johnpass"},
    {"name": "Alice Smith", "email": "alice@example.com", "phone": "9876543222", "room_number": 102, "hostel_id": hostel_boys.hostel_id, "emergency_contact": "Bob Smith - 8888888888", "password": "alicepass"}
]
for student_data in students:
    existing_student = db.query(Student).filter_by(email=student_data["email"]).first()
    if not existing_student:
        create_student(db, **student_data)
db.commit()
print("✅ Students added!")

# 🔹 4. Mark Attendance
print("\n📌 Marking attendance...")
students = db.query(Student).all()
for student in students:
    mark_attendance(db, student.student_id, "Present", True, True, 31.3949, 75.5331)
    print(f"✅ Attendance marked for {student.name}")

# 🔹 5. Apply Fines
print("\n💰 Applying fines...")
fine_due_date = datetime.utcnow() + timedelta(days=7)
for student in students[:2]:  # Apply fines to first two students
    apply_fine(db, student.student_id, amount=500, due_date=fine_due_date)
    print(f"✅ Fine of ₹500 applied to {student.name}")

# 🔹 6. Send Notifications
print("\n🔔 Sending notifications...")
for student in students:
    send_notification(db, student.student_id, message="Reminder: Mark your attendance before 10 PM!")
    print(f"✅ Notification sent to {student.name}")

# Close session
db.close()
print("\n🎉 Seeding complete!")
