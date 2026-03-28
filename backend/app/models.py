from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    enroll_no = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    marks = relationship("Marks", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String)
    semester = Column(Integer)
    
    # --- NEW ML FEATURES ---
    credits = Column(Integer, default=4)
    weight = Column(Integer, default=100)

    marks = relationship("Marks", back_populates="subject")

class Marks(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    semester = Column(Integer)
    sessional_marks = Column(Integer)
    endsem_marks = Column(Integer)

    # --- NEW ML FEATURES ---
    num_of_prev_attempts = Column(Integer, default=0)
    engagement_clicks = Column(Integer, default=0)  # Proxy for sum_click

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")

    __table_args__ = (
        UniqueConstraint(
            'student_id',
            'subject_id',
            'semester',
            name='unique_student_subject_semester'
        ),
    )