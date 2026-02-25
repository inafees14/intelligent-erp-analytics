"""Seed database with UCI Student Performance Dataset."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from passlib.context import CryptContext

from app.database import SessionLocal, engine, Base
from app.models.models import (
    Users, StudentTable, AdminTable, ExamTable, MarksheetTable, StudentFeatures,
)
from data_science.data_loader import load_raw_dataset

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Users).first():
            print("Database already seeded. Skipping.")
            return

        # Create admin user
        admin_user = Users(
            user_name="admin",
            user_password=pwd_context.hash("admin123"),
            designation="admin",
        )
        db.add(admin_user)
        db.flush()

        admin = AdminTable(
            user_id=admin_user.user_id,
            first_name="System",
            last_name="Admin",
            phone_no="0000000000",
            email_id="admin@erp.edu",
        )
        db.add(admin)

        # Create exams
        exams = [
            ExamTable(exam_name="First Period", year=2024),
            ExamTable(exam_name="Second Period", year=2024),
            ExamTable(exam_name="Final Exam", year=2024),
        ]
        db.add_all(exams)
        db.flush()

        # Load UCI dataset
        raw_df = load_raw_dataset()

        # Limit to ~395 students (full dataset)
        for idx, row in raw_df.iterrows():
            # Create student user
            username = f"student{idx + 1}"
            student_user = Users(
                user_name=username,
                user_password=pwd_context.hash("pass123"),
                designation="student",
            )
            db.add(student_user)
            db.flush()

            student = StudentTable(
                user_id=student_user.user_id,
                first_name=f"Student",
                last_name=f"{idx + 1}",
                phone_no=f"555{str(idx + 1).zfill(7)}",
                email_id=f"{username}@student.edu",
            )
            db.add(student)
            db.flush()

            # Insert marks for each exam period (G1, G2, G3)
            # Exam 1: First Period with G1 marks
            db.add(MarksheetTable(
                std_id=student.std_id,
                exam_id=exams[0].exam_id,
                subject_1_marks=float(row["G1"]),
                subject_2_marks=float(row["G2"]),
                total_marks=float(row["G1"]) + float(row["G2"]),
            ))
            # Exam 2: Second Period
            db.add(MarksheetTable(
                std_id=student.std_id,
                exam_id=exams[1].exam_id,
                subject_1_marks=float(row["G2"]),
                subject_2_marks=float(row["G3"]),
                total_marks=float(row["G2"]) + float(row["G3"]),
            ))
            # Exam 3: Final Exam with G3 as total
            db.add(MarksheetTable(
                std_id=student.std_id,
                exam_id=exams[2].exam_id,
                subject_1_marks=float(row["G1"]),
                subject_2_marks=float(row["G2"]),
                total_marks=float(row["G3"]),
            ))

            # Insert student features
            db.add(StudentFeatures(
                std_id=student.std_id,
                attendance=float(row["absences"]),
                study_hours=float(row["studytime"]),
                failures=int(row["failures"]),
            ))

        db.commit()
        print(f"Seeded {len(raw_df)} students with marks and features.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
