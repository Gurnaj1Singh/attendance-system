import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Attendance from "./pages/Attendance";
import StudentDashboard from "./pages/StudentDashboard";
import StudentHome from "./pages/home";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/home" element={<StudentHome />} />
                <Route path="/attendance" element={<Attendance />} />
                <Route path="/dashboard" element={<StudentDashboard />} />
            </Routes>
        </Router>
    );
}

export default App;
