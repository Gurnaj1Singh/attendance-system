import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function AttendancePage() {
  const [token, setToken] = useState(null);
  const [student, setStudent] = useState(null);
  const [attendanceStatus, setAttendanceStatus] = useState(null);
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
      fetchStudentData(savedToken);
    }
    getLocation();
    startCamera();
  }, []);

  const fetchStudentData = async (token) => {
    try {
      const response = await axios.get("http://localhost:8000/students/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStudent(response.data);
    } catch (error) {
      console.error("❌ Error fetching student data", error.response || error);
    }
  };

  const getLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        console.log("📍 Location Fetched:", pos.coords.latitude, pos.coords.longitude);
        setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude });
      },
      (err) => {
        console.error("❌ Location error", err);
        alert("⚠️ Location access is required to mark attendance.");
      },
      { enableHighAccuracy: true }
    );
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      alert("⚠️ Camera access is required for marking attendance.");
      console.error("❌ Error accessing camera", error);
    }
  };

  const markAttendance = async () => {
    setLoading(true);

    // Validate required fields
    if (!token) {
      alert("❌ User not authenticated. Please log in again.");
      setLoading(false);
      return;
    }
    if (!location.latitude || !location.longitude) {
      alert("❌ Location not available. Please enable location services.");
      getLocation();
      setLoading(false);
      return;
    }
    if (!student) {
      alert("❌ Student data is missing. Please refresh the page.");
      setLoading(false);
      return;
    }

    try {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");

      // Capture image from video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);
      const capturedImage = canvas.toDataURL("image/png");

      // Prepare form data
      const formData = new FormData();
      formData.append("token", token);
      formData.append("file", dataURItoBlob(capturedImage), "capture.png");
      formData.append("latitude", location.latitude);
      formData.append("longitude", location.longitude);

      console.log("🚀 Sending Face Recognition Request...");

      // Face Recognition Request
      const faceResponse = await axios.post("http://127.0.0.1:8001/recognize-face/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "json",
      });

      console.log("✅ Face Recognition Response:", faceResponse.data);

      // Validate Face Recognition
      if (!faceResponse.data.name || faceResponse.data.name === "Unknown" || faceResponse.data.name !== student.name) {
        alert("❌ Face recognition failed! Ensure proper lighting and try again.");
        setLoading(false);
        return;
      }

      console.log("✅ Face Matched with:", faceResponse.data.name);

      console.log("🚀 Sending Attendance Marking Request...");

      // Attendance Marking Request
      const attendanceResponse = await axios.post("http://localhost:8000/attendance/mark", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("✅ Attendance API Response:", attendanceResponse.data);

      if (!attendanceResponse.data || !attendanceResponse.data.message) {
        throw new Error("⚠️ Invalid response from server. Expected 'message' field.");
      }

      setAttendanceStatus(attendanceResponse.data.message);
    } catch (error) {
      console.error("❌ Error marking attendance:", error.response?.data || error.message);
      alert(error.response?.data?.detail || "❌ Failed to mark attendance. Please try again.");
    }
    setLoading(false);
  };

  function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(",")[1]);
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6 text-center rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Attendance Portal</h1>
      {student && <p className="text-lg mb-4 text-gray-700">Welcome, <span className="font-semibold">{student.name}</span></p>}
      <div className="relative w-96 h-72 border-4 border-gray-300 rounded-lg overflow-hidden shadow-md">
        <video ref={videoRef} autoPlay className="w-full h-full object-cover"></video>
      </div>
      <canvas ref={canvasRef} className="hidden"></canvas>
      <button
        onClick={markAttendance}
        className="mt-6 bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-3 rounded-lg shadow-md transition-all duration-300 ease-in-out disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Marking Attendance..." : "Capture & Mark Attendance"}
      </button>
      {attendanceStatus && <p className="mt-4 text-lg font-semibold text-green-600">{attendanceStatus}</p>}
    </div>
  );
}
