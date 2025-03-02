from sqlalchemy.orm import sessionmaker
from backend.database.db_connection import engine
from backend.database.crud import mark_attendance, get_attendance_by_student, is_valid_attendance_time, is_location_valid

# Create a new session for testing
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 📍 Hostel Coordinates
HOSTEL_LAT = 31.3949
HOSTEL_LON = 75.5331

# ✅ Test 1: Valid Attendance
def test_valid_attendance():
    student_id = 7 
    assert is_location_valid(HOSTEL_LAT, HOSTEL_LON) == True  # Check location

    attendance = mark_attendance(db, student_id, "Present", True, True, HOSTEL_LAT, HOSTEL_LON)
    assert attendance is not None
    assert attendance.status == "Present"
    print("✅ Test 1 Passed: Valid Attendance")

# ❌ Test 2: Attendance Outside Hostel
def test_attendance_outside_hostel():
    student_id = 7
    student_lat = 31.3940  # Outside hostel
    student_lon = 75.5330

    assert is_location_valid(student_lat, student_lon) == False  # Should fail
    try:
        mark_attendance(db, student_id, "Present", True, True, student_lat, student_lon)
    except Exception as e:
        assert "You must be inside the hostel" in str(e)
    print("✅ Test 2 Passed: Attendance Outside Hostel Rejected")

# ❌ Test 3: Attendance Outside Allowed Time (Before 8 PM)
def test_attendance_before_time():
    assert is_valid_attendance_time() == False  # Should fail
    print("✅ Test 3 Passed: Attendance Before 8 PM Rejected")

# ❌ Test 4: Attendance After Allowed Time (After 10 PM)
def test_attendance_after_time():
    assert is_valid_attendance_time() == False  # Should fail
    print("✅ Test 4 Passed: Attendance After 10 PM Rejected")

# 🏁 Run All Tests
if __name__ == "__main__":
    test_valid_attendance()
    test_attendance_outside_hostel()
    test_attendance_before_time()
    test_attendance_after_time()
    print("\n🎉 All Test Cases Passed Successfully!")
