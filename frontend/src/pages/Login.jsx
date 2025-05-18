import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";


const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        
        try {
            const formData = new FormData();
            formData.append("username", email);  // OAuth expects "username" instead of "email"
            formData.append("password", password);
            formData.append("grant_type", "password");  // Required for OAuth2
    
            const response = await axios.post("http://localhost:8000/auth/student-login", formData, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });
    
            localStorage.setItem("token", response.data.access_token);
            navigate("/home");
        } catch (err) {
            setError("Invalid credentials. Please try again.");
        }
    };
    

    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white p-6 rounded-xl shadow-md w-80">
          <h2 className="text-2xl font-semibold text-center mb-4">Login</h2>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
          <form onSubmit={handleLogin} className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Login
            </button>
          </form>
          <p className="text-center text-sm mt-4">
            Don't have an account?
            <button
              onClick={() => navigate("/signup")}
              className="text-blue-600 hover:underline ml-1"
            >
              Sign up
            </button>
          </p>
        </div>
      </div>
    );
};

export default Login;