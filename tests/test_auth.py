"""Tests for ERP Portal authentication and core functionality."""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create in-memory test engine with shared connection
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Patch database module before importing the app
import app.database
app.database.engine = test_engine
app.database.SessionLocal = TestSession

from app.database import Base
from app.models.models import Users, StudentTable, AdminTable, ExamTable, MarksheetTable
from app.main import app as fastapi_app
from fastapi.testclient import TestClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = TestClient(fastapi_app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestSession()

    # Create test admin
    admin_user = Users(
        user_name="testadmin",
        user_password=pwd_context.hash("adminpass"),
        designation="admin",
    )
    db.add(admin_user)
    db.flush()
    db.add(AdminTable(
        user_id=admin_user.user_id, first_name="Test", last_name="Admin",
        phone_no="1234567890", email_id="admin@test.com",
    ))

    # Create test student
    student_user = Users(
        user_name="teststudent",
        user_password=pwd_context.hash("studentpass"),
        designation="student",
    )
    db.add(student_user)
    db.flush()
    student = StudentTable(
        user_id=student_user.user_id, first_name="Test", last_name="Student",
        phone_no="0987654321", email_id="student@test.com",
    )
    db.add(student)
    db.flush()

    # Create test exam
    exam = ExamTable(exam_name="Test Exam", year=2024)
    db.add(exam)
    db.flush()

    # Create test marksheet
    db.add(MarksheetTable(
        std_id=student.std_id, exam_id=exam.exam_id,
        subject_1_marks=15.0, subject_2_marks=12.0, total_marks=27.0,
    ))
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=test_engine)


def test_login_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "ERP Portal" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_invalid_credentials():
    response = client.post(
        "/login",
        data={"user_name": "invalid", "user_password": "wrong"},
    )
    assert response.status_code == 200
    assert "Invalid" in response.text


def test_admin_login():
    response = client.post(
        "/login",
        data={"user_name": "testadmin", "user_password": "adminpass"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "/admin/dashboard" in response.headers["location"]


def test_student_login():
    response = client.post(
        "/login",
        data={"user_name": "teststudent", "user_password": "studentpass"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "/student/dashboard" in response.headers["location"]


def test_admin_dashboard_requires_auth():
    fresh_client = TestClient(fastapi_app)
    response = fresh_client.get("/admin/dashboard", follow_redirects=False)
    assert response.status_code == 403


def test_student_dashboard_requires_auth():
    fresh_client = TestClient(fastapi_app)
    response = fresh_client.get("/student/dashboard", follow_redirects=False)
    assert response.status_code == 403


def test_logout():
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 303
