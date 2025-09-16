from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class StudentBase(SQLModel):
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    roll_number: str = Field(unique=True, index=True)
    class_name: str
    career_interest: Optional[str] = None

class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int
    created_at: datetime

class AttendanceBase(SQLModel):
    student_id: int = Field(foreign_key="student.id")
    subject: str
    attendance_type: str = "present"  # present, absent, late

class Attendance(AttendanceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    marked_by: str = "system"  # system, teacher, student

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceRead(AttendanceBase):
    id: int
    timestamp: datetime
    marked_by: str

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None
    difficulty_level: str = "medium"  # easy, medium, hard
    estimated_time: int = 30  # minutes
    task_type: str = "assignment"  # assignment, project, reading, practice

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    is_active: bool

class StudentTaskBase(SQLModel):
    student_id: int = Field(foreign_key="student.id")
    task_id: int = Field(foreign_key="task.id")
    status: str = "assigned"  # assigned, in_progress, completed, skipped

class StudentTask(StudentTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    feedback: Optional[str] = None

class StudentTaskRead(StudentTaskBase):
    id: int
    assigned_at: datetime
    completed_at: Optional[datetime]
    feedback: Optional[str]