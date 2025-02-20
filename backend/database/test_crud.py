from sqlalchemy.orm import sessionmaker
from db_connection import engine
from crud import (
    create_student, get_student, get_all_students, update_student, delete_student,
    mark_attendance, get_attendance_by_student,
    apply_fine, get_fines_by_student, pay_fine,
    send_notification, get_notifications
)
from datetime import datetime, timedelta

# Create a session to interact with the database
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Test Data
student_data = {
    "name": "Gurnaj Singh Mann",
    "email": "gurnajsm.cs.22@nitj.ac.in",
    "phone": "9876543210",
    "room_number": 226,
    "hostel_id": 1,
    "emergency_contact": "1234567890"
}

# 🔹 1. Create a New Student
print("✅ Creating a new student...")
new_student = create_student(db, **student_data)
print(f"Student Created: {new_student.name}, ID: {new_student.student_id}")

# 🔹 2. Fetch Student by ID
print("\n🔍 Fetching student by ID...")
student = get_student(db, new_student.student_id)
print(f"Student Found: {student.name}, Email: {student.email}")

# 🔹 3. Fetch All Students
print("\n📜 Fetching all students...")
students = get_all_students(db)
for s in students:
    print(f"{s.student_id} - {s.name}")

# 🔹 4. Update Student Details
print("\n✏️ Updating student details...")
updated_student = update_student(db, new_student.student_id, name=student_data["name"])
print(f"Updated Student Name: {updated_student.name}")

# 🔹 5. Mark Attendance
print("\n📌 Marking attendance...")
attendance = mark_attendance(db, new_student.student_id, status="Present", location_verified=True, face_verified=True)
print(f"Attendance Marked: {attendance.status} at {attendance.date_time}")

# 🔹 6. Fetch Attendance Records
print("\n📜 Fetching attendance records...")
attendances = get_attendance_by_student(db, new_student.student_id)
for a in attendances:
    print(f"Date: {a.date_time}, Status: {a.status}")

# 🔹 7. Apply Fine
print("\n💰 Applying a fine...")
due_date = datetime.utcnow() + timedelta(days=7)
fine = apply_fine(db, new_student.student_id, amount=200, due_date=due_date)
print(f"Fine Applied: ₹{fine.amount}, Due Date: {fine.due_date}")

# 🔹 8. Get Pending Fines
print("\n📜 Fetching pending fines...")
fines = get_fines_by_student(db, new_student.student_id)
for f in fines:
    print(f"Fine: ₹{f.amount}, Status: {f.status}")

# 🔹 9. Pay Fine
print("\n✅ Paying a fine...")
paid_fine = pay_fine(db, fine.fine_id)
if paid_fine:
    print(f"Fine Status Updated: {paid_fine.status}")

# 🔹 10. Send Notification
print("\n🔔 Sending notification...")
notification = send_notification(db, new_student.student_id, message="Reminder: Mark your attendance before 10 PM!")
print(f"Notification Sent: {notification.message}")

# 🔹 11. Fetch Notifications
print("\n📜 Fetching notifications...")
notifications = get_notifications(db, new_student.student_id)
for n in notifications:
    print(f"Message: {n.message}, Status: {n.status}")

# 🔹 12. Delete Student
print("\n🗑️ Deleting student...")
deleted = delete_student(db, new_student.student_id)
if deleted:
    print("Student Deleted Successfully")
else:
    print("Student Not Found")

# Close the session
db.close()
