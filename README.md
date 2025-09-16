# EduSync - Smart Attendance & Learning Platform

A comprehensive educational platform that automates attendance tracking and provides personalized learning recommendations for students during free periods.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🐳 Docker Setup (Alternative)

```bash
docker-compose up --build
```

## 📁 Project Structure

```
edusync/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🎯 Features

- **Automated Attendance**: Mark attendance with a single click
- **Student Management**: View and manage student records
- **Real-time Updates**: Live attendance tracking
- **Responsive Design**: Works on desktop and mobile
- **API Documentation**: Auto-generated Swagger docs

## 🛠 Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLModel (Database ORM)
- SQLite (Development database)
- Uvicorn (ASGI server)

**Frontend:**
- React 18
- Modern JavaScript (ES6+)
- CSS3 with responsive design
- Fetch API for HTTP requests

## 🌐 API Endpoints

- `GET /students` - Get all students
- `POST /attendance/{student_id}` - Mark attendance
- `GET /attendance/{student_id}` - Get student attendance history
- `GET /docs` - API documentation

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for educational purposes.

## 🎓 SIH 2025 Submission

This project is part of Smart India Hackathon 2025 submission for Problem Statement SIH25011: "Smart Curriculum Activity & Attendance App" by Government of Punjab.

**Team:** [Your Team Name]
**Problem ID:** SIH25011