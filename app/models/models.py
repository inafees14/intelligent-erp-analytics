from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(100), unique=True, nullable=False)
    user_password = Column(String(255), nullable=False)
    designation = Column(String(50), nullable=False)  # 'admin' or 'student'

    student = relationship("StudentTable", back_populates="user", uselist=False)
    admin = relationship("AdminTable", back_populates="user", uselist=False)


class StudentTable(Base):
    __tablename__ = "student_table"

    std_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_no = Column(String(20))
    email_id = Column(String(150))

    user = relationship("Users", back_populates="student")
    marksheets = relationship("MarksheetTable", back_populates="student")


class AdminTable(Base):
    __tablename__ = "admin_table"

    adm_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_no = Column(String(20))
    email_id = Column(String(150))

    user = relationship("Users", back_populates="admin")


class ExamTable(Base):
    __tablename__ = "exam_table"

    exam_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_name = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)

    marksheets = relationship("MarksheetTable", back_populates="exam")


class MarksheetTable(Base):
    __tablename__ = "marksheet_table"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    std_id = Column(Integer, ForeignKey("student_table.std_id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exam_table.exam_id"), nullable=False)
    subject_1_marks = Column(Float, nullable=False)
    subject_2_marks = Column(Float, nullable=False)
    total_marks = Column(Float, nullable=False)

    student = relationship("StudentTable", back_populates="marksheets")
    exam = relationship("ExamTable", back_populates="marksheets")


class StudentFeatures(Base):
    """Extended table for UCI dataset features used in analytics."""
    __tablename__ = "student_features"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    std_id = Column(Integer, ForeignKey("student_table.std_id"), nullable=False)
    attendance = Column(Float)
    study_hours = Column(Float)
    failures = Column(Integer)

    student = relationship("StudentTable")
