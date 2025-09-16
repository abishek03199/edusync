from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List
from datetime import datetime
import random

from models import (
    Student, StudentCreate, StudentRead,
    Attendance, AttendanceCreate, AttendanceRead,
    Task, TaskRead, StudentTask, StudentTaskRead
)

# Database setup
sqlite_file_name = "edusync.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# FastAPI app
app = FastAPI(
    title="EduSync API",
    description="Smart Attendance and Learning Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Seed initial data
    with Session(engine) as session:
        # Check if data already exists
        existing_students = session.exec(select(Student)).first()
        if not existing_students:
            # Create sample students
            sample_students = [
                Student(
                    name="Arun Kumar",
                    email="arun@example.com",
                    roll_number="CS21001",
                    class_name="Computer Science A",
                    career_interest="Software Engineer"
                ),
                Student(
                    name="Divya Sharma",
                    email="divya@example.com",
                    roll_number="CS21002",
                    class_name="Computer Science A",
                    career_interest="Data Scientist"
                ),
                Student(
                    name="Rahul Patel",
                    email="rahul@example.com",
                    roll_number="CS21003",
                    class_name="Computer Science B",
                    career_interest="Mobile Developer"
                ),
                Student(
                    name="Priya Singh",
                    email="priya@example.com",
                    roll_number="CS21004",
                    class_name="Computer Science B",
                    career_interest="AI Engineer"
                )
            ]
            
            # Create sample tasks
            sample_tasks = [
                Task(
                    title="Complete Python Basics Tutorial",
                    description="Learn Python fundamentals with hands-on coding",
                    subject="Programming",
                    difficulty_level="easy",
                    estimated_time=45,
                    task_type="practice"
                ),
                Task(
                    title="Math Problem Set - Calculus",
                    description="Solve 10 integration problems",
                    subject="Mathematics",
                    difficulty_level="medium",
                    estimated_time=60,
                    task_type="assignment"
                ),
                Task(
                    title="Data Structures Project",
                    description="Implement a binary search tree",
                    subject="Computer Science",
                    difficulty_level="hard",
                    estimated_time=120,
                    task_type="project"
                )
            ]
            
            for student in sample_students:
                session.add(student)
            for task in sample_tasks:
                session.add(task)
            
            session.commit()

# Student endpoints
@app.get("/students", response_model=List[StudentRead])
def get_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students

@app.post("/students", response_model=StudentRead)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student.from_orm(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Attendance endpoints
@app.post("/attendance/{student_id}", response_model=AttendanceRead)
def mark_attendance(
    student_id: int, 
    subject: str = "General", 
    session: Session = Depends(get_session)
):
    # Verify student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create attendance record
    attendance = Attendance(
        student_id=student_id,
        subject=subject,
        attendance_type="present",
        marked_by="system"
    )
    session.add(attendance)
    session.commit()
    session.refresh(attendance)
    return attendance

@app.get("/attendance/{student_id}", response_model=List[AttendanceRead])
def get_student_attendance(
    student_id: int, 
    session: Session = Depends(get_session)
):
    attendance_records = session.exec(
        select(Attendance).where(Attendance.student_id == student_id)
    ).all()
    return attendance_records

@app.get("/attendance", response_model=List[AttendanceRead])
def get_all_attendance(session: Session = Depends(get_session)):
    attendance_records = session.exec(select(Attendance)).all()
    return attendance_records

# Task endpoints
@app.get("/tasks", response_model=List[TaskRead])
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.is_active == True)).all()
    return tasks

@app.get("/students/{student_id}/recommended-tasks")
def get_recommended_tasks(
    student_id: int, 
    session: Session = Depends(get_session)
):
    # Verify student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get available tasks
    tasks = session.exec(select(Task).where(Task.is_active == True)).all()
    
    # Simple recommendation: randomly select 3 tasks
    # In production, this would use ML algorithms based on student interests, performance, etc.
    recommended_tasks = random.sample(list(tasks), min(3, len(tasks)))
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "career_interest": student.career_interest,
        "recommended_tasks": recommended_tasks
    }

@app.post("/students/{student_id}/assign-task/{task_id}")
def assign_task_to_student(
    student_id: int, 
    task_id: int, 
    session: Session = Depends(get_session)
):
    # Verify student and task exist
    student = session.get(Student, student_id)
    task = session.get(Task, task_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Create student-task assignment
    student_task = StudentTask(
        student_id=student_id,
        task_id=task_id,
        status="assigned"
    )
    session.add(student_task)
    session.commit()
    session.refresh(student_task)
    
    return {
        "message": f"Task '{task.title}' assigned to {student.name}",
        "student_task": student_task
    }

# Dashboard endpoints
@app.get("/dashboard/stats")
def get_dashboard_stats(session: Session = Depends(get_session)):
    total_students = len(session.exec(select(Student)).all())
    total_attendance_today = len(session.exec(
        select(Attendance).where(
            Attendance.timestamp >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
    ).all())
    total_tasks = len(session.exec(select(Task).where(Task.is_active == True)).all())
    
    return {
        "total_students": total_students,
        "attendance_today": total_attendance_today,
        "active_tasks": total_tasks,
        "attendance_percentage": round((total_attendance_today / total_students) * 100, 1) if total_students > 0 else 0
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to EduSync API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)