import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [students, setStudents] = useState([]);
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [dashboardStats, setDashboardStats] = useState({});
  const [recommendedTasks, setRecommendedTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [activeTab, setActiveTab] = useState('attendance');

  // Fetch students on component mount
  useEffect(() => {
    fetchStudents();
    fetchDashboardStats();
    fetchAllAttendance();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/students`);
      const data = await response.json();
      setStudents(data);
    } catch (error) {
      console.error('Error fetching students:', error);
      setMessage('Error loading students');
    }
  };

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
      const data = await response.json();
      setDashboardStats(data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const fetchAllAttendance = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/attendance`);
      const data = await response.json();
      setAttendanceRecords(data);
    } catch (error) {
      console.error('Error fetching attendance records:', error);
    }
  };

  const markAttendance = async (studentId, studentName) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/attendance/${studentId}?subject=General`, {
        method: 'POST',
      });
      const data = await response.json();
      setMessage(`✅ Attendance marked for ${studentName} at ${new Date(data.timestamp).toLocaleTimeString()}`);
      fetchDashboardStats(); // Refresh stats
      fetchAllAttendance(); // Refresh attendance records
    } catch (error) {
      console.error('Error marking attendance:', error);
      setMessage('❌ Error marking attendance');
    } finally {
      setLoading(false);
    }
  };

  const getRecommendedTasks = async (studentId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/students/${studentId}/recommended-tasks`);
      const data = await response.json();
      setRecommendedTasks(data.recommended_tasks || []);
      setSelectedStudent(data);
    } catch (error) {
      console.error('Error fetching recommended tasks:', error);
    }
  };

  const assignTask = async (studentId, taskId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/students/${studentId}/assign-task/${taskId}`, {
        method: 'POST',
      });
      const data = await response.json();
      setMessage(`📚 ${data.message}`);
    } catch (error) {
      console.error('Error assigning task:', error);
      setMessage('❌ Error assigning task');
    }
  };

  const getAttendanceForStudent = (studentId) => {
    return attendanceRecords.filter(record => record.student_id === studentId);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎓 EduSync - Smart Attendance & Learning Platform</h1>
        <p>Smart India Hackathon 2025 - Problem Statement SIH25011</p>
      </header>

      {/* Dashboard Stats */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>👥 Total Students</h3>
          <p>{dashboardStats.total_students || 0}</p>
        </div>
        <div className="stat-card">
          <h3>📅 Today's Attendance</h3>
          <p>{dashboardStats.attendance_today || 0}</p>
        </div>
        <div className="stat-card">
          <h3>📊 Attendance %</h3>
          <p>{dashboardStats.attendance_percentage || 0}%</p>
        </div>
        <div className="stat-card">
          <h3>📚 Active Tasks</h3>
          <p>{dashboardStats.active_tasks || 0}</p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={activeTab === 'attendance' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('attendance')}
        >
          📋 Attendance
        </button>
        <button 
          className={activeTab === 'tasks' ? 'tab active' : 'tab'}
          onClick={() => setActiveTab('tasks')}
        >
          📚 Learning Tasks
        </button>
      </div>

      {/* Message Display */}
      {message && (
        <div className="message">
          {message}
          <button onClick={() => setMessage('')}>✕</button>
        </div>
      )}

      {/* Attendance Tab */}
      {activeTab === 'attendance' && (
        <div className="tab-content">
          <h2>👥 Student Attendance Management</h2>
          <div className="students-grid">
            {students.map(student => {
              const studentAttendance = getAttendanceForStudent(student.id);
              return (
                <div key={student.id} className="student-card">
                  <div className="student-info">
                    <h3>{student.name}</h3>
                    <p><strong>Roll:</strong> {student.roll_number}</p>
                    <p><strong>Class:</strong> {student.class_name}</p>
                    <p><strong>Career Interest:</strong> {student.career_interest}</p>
                    <p><strong>Total Attendance:</strong> {studentAttendance.length} days</p>
                  </div>
                  <div className="student-actions">
                    <button 
                      className="attendance-btn"
                      onClick={() => markAttendance(student.id, student.name)}
                      disabled={loading}
                    >
                      {loading ? '⏳ Marking...' : '✅ Mark Present'}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Recent Attendance Records */}
          <div className="recent-attendance">
            <h3>📊 Recent Attendance Records</h3>
            <div className="attendance-list">
              {attendanceRecords.slice(-10).reverse().map(record => {
                const student = students.find(s => s.id === record.student_id);
                return (
                  <div key={record.id} className="attendance-record">
                    <span className="student-name">{student?.name || 'Unknown'}</span>
                    <span className="subject">{record.subject}</span>
                    <span className="time">{new Date(record.timestamp).toLocaleString()}</span>
                    <span className="status">✅ {record.attendance_type}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Learning Tasks Tab */}
      {activeTab === 'tasks' && (
        <div className="tab-content">
          <h2>📚 Personalized Learning Tasks</h2>
          <div className="task-section">
            <h3>Select a student to get personalized task recommendations:</h3>
            <div className="student-selector">
              {students.map(student => (
                <button
                  key={student.id}
                  className={selectedStudent?.student_id === student.id ? 'student-btn active' : 'student-btn'}
                  onClick={() => getRecommendedTasks(student.id)}
                >
                  {student.name}
                </button>
              ))}
            </div>

            {selectedStudent && (
              <div className="selected-student-info">
                <h3>🎯 Recommendations for {selectedStudent.student_name}</h3>
                <p><strong>Career Interest:</strong> {selectedStudent.career_interest}</p>
                
                <div className="recommended-tasks">
                  {recommendedTasks.map(task => (
                    <div key={task.id} className="task-card">
                      <h4>{task.title}</h4>
                      <p>{task.description}</p>
                      <div className="task-details">
                        <span className="task-subject">📖 {task.subject}</span>
                        <span className="task-difficulty">⭐ {task.difficulty_level}</span>
                        <span className="task-time">⏱️ {task.estimated_time} min</span>
                        <span className="task-type">📋 {task.task_type}</span>
                      </div>
                      <button 
                        className="assign-btn"
                        onClick={() => assignTask(selectedStudent.student_id, task.id)}
                      >
                        📌 Assign Task
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <footer className="app-footer">
        <p>🔗 API Documentation: <a href={`${API_BASE_URL}/docs`} target="_blank" rel="noopener noreferrer">
          {API_BASE_URL}/docs
        </a></p>
        <p>Built for Smart India Hackathon 2025 🇮🇳</p>
      </footer>
    </div>
  );
}

export default App;