import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";


export default function StudentHome() {
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (token) {
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
  }, [token]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6 text-center">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">
        Welcome {student ? student.name : "Student"}
      </h1>
      <div className="flex space-x-4">
        <button
          onClick={() => navigate("/dashboard")}
          className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-3 rounded-lg shadow-md transition-all duration-300"
        >
          Dashboard
        </button>
        <button
          onClick={() => navigate("/attendance")}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-lg shadow-md transition-all duration-300"
        >
          Mark Attendance
        </button>
      </div>
    </div>
  );
}
