import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function StudentDashboard() {
  const [student, setStudent] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // Fetch student details
  useEffect(() => {
    if (!token) {
      navigate("/");
    } else {
      axios
        .get("http://localhost:8000/students/me", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          setStudent(response.data);
        })
        .catch((error) => {
          console.error("Error fetching student data", error);
        });
    }
  }, [token, navigate]);

  // Once student details are available, fetch their attendance records
  useEffect(() => {
    if (student && student.student_id) {
      axios
        .get(`http://localhost:8000/attendance/${student.student_id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          setAttendance(response.data.attendance);
        })
        .catch((error) => {
          console.error("Error fetching attendance data", error);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [student, token]);

  // Helper: get today's attendance record
  const getTodayAttendance = () => {
    if (!attendance.length) return null;
    const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    return attendance.find((record) => record.date_time.slice(0, 10) === today);
  };

  const todayAttendance = getTodayAttendance();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Student Dashboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
          {student && (
            <div className="mb-4">
              <h2 className="text-xl font-semibold mb-2">{student.name}</h2>
              <p>Email: {student.email}</p>
              <p>Room Number: {student.room_number}</p>
              <p>Hostel ID: {student.hostel_id}</p>
            </div>
          )}
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Today's Attendance</h3>
            {todayAttendance ? (
              <div>
                <p>Status: {todayAttendance.status}</p>
                <p>
                  Date:{" "}
                  {new Date(todayAttendance.date_time).toLocaleString()}
                </p>
              </div>
            ) : (
              <p>No attendance marked for today.</p>
            )}
          </div>
          <button
            onClick={() => navigate("/attendance")}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Mark Attendance
          </button>
        </div>
      )}
    </div>
  );
}
