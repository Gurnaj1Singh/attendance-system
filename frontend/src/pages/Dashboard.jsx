import { useEffect, useState } from "react";
import axios from "axios";


const Dashboard = () => {
    const [attendanceData, setAttendanceData] = useState([]);
    const [finesData, setFinesData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const attendanceRes = await axios.get("http://localhost:8000/attendance/");
            const finesRes = await axios.get("http://localhost:8000/fines/");
            
            setAttendanceData(attendanceRes.data.attendance);
            setFinesData(finesRes.data.fines);
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
        <h1 className="text-2xl font-semibold mb-4">Admin Dashboard</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <div className="w-full max-w-4xl bg-white p-4 rounded-xl shadow-md mb-6">
              <h2 className="text-lg font-semibold mb-2">Attendance Records</h2>
              <div className="overflow-auto max-h-60">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-gray-200">
                      <th className="border p-2">Student ID</th>
                      <th className="border p-2">Status</th>
                      <th className="border p-2">Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attendanceData.map((record, index) => (
                      <tr key={index} className="border">
                        <td className="p-2 text-center">{record.student_id}</td>
                        <td className="p-2 text-center">{record.status}</td>
                        <td className="p-2 text-center">
                          {new Date(record.date_time).toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="w-full max-w-4xl bg-white p-4 rounded-xl shadow-md">
              <h2 className="text-lg font-semibold mb-2">Fines</h2>
              <div className="overflow-auto max-h-60">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-gray-200">
                      <th className="border p-2">Student ID</th>
                      <th className="border p-2">Amount</th>
                      <th className="border p-2">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {finesData.map((fine, index) => (
                      <tr key={index} className="border">
                        <td className="p-2 text-center">{fine.student_id}</td>
                        <td className="p-2 text-center">₹{fine.amount}</td>
                        <td className="p-2 text-center">{fine.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    );
};

export default Dashboard;