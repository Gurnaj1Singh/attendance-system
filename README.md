# 📸 Smart Hostel Attendance System

A secure and intelligent face recognition-based hostel attendance system that ensures students are physically present at their hostel using GPS location verification and facial matching.

![Smart Hostel Banner](https://via.placeholder.com/1000x300?text=Smart+Hostel+Attendance+System) <!-- Optional custom banner -->

---

## 🚀 Features

✅ Face Recognition using `face_recognition` and OpenCV  
✅ Location Verification using GPS (Geopy + Browser Geolocation)  
✅ Attendance Window Restriction (e.g. 8PM–10PM only)  
✅ Secure Student Login & Token-based Authentication  
✅ Admin Dashboard for Real-time Attendance Monitoring  
✅ Live Camera Feed — No Manual Uploads  
✅ React Frontend + FastAPI Backend  
✅ MySQL Database Integration

---

## 🧠 Tech Stack

| Frontend   | Backend     | Database | Location & Vision |
|------------|-------------|----------|-------------------|
| React.js   | FastAPI     | MySQL    | Geopy, OpenCV, face_recognition |

---

## 📸 How It Works

1. Student logs in using email & password.
2. System requests camera & location access.
3. Student captures their face in real-time.
4. Backend verifies:
   - If the face matches the saved encoding
   - If the student is physically near their hostel (within 100m)
   - If the current time is within the allowed window (e.g., 8PM–10PM)
5. If all checks pass ✅ → Attendance is recorded.

---

## 🛠️ Installation

### 🧩 Backend (FastAPI + MySQL)
git clone https://github.com/your-username/smart-hostel-attendance.git
cd smart-hostel-attendance/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn backend.api.main:app --reload

### Frontend
cd ../frontend
npm install
npm run dev

### 📷 Dataset Setup for Face Recognition
# Create a folder: backend/face_recog_system/dataset/
Add clear front-facing .jpg or .png images named exactly as the student’s name (e.g., John Doe.jpg)
# Run:
- python backend/face_recog_system/face_recog.py
- This will generate encodings and save them to the database.

