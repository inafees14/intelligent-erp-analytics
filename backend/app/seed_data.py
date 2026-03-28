# backend/app/seed_data.py
import random
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models

def seed_database():
    db: Session = SessionLocal()
    try:
        # 1. Prevent Duplication: Check if students already exist
        if db.query(models.Student).first():
            print("Database already seeded. Skipping initial data injection...")
            return

        print("Empty database detected. Seeding with realistic B.Sc. Statistics dummy data...")

        # 2. Add Realistic Subjects
        subjects_data = [
            {"subject_name": "Descriptive Statistics", "semester": 1},
            {"subject_name": "Calculus & Matrices", "semester": 1},
            {"subject_name": "Physics I", "semester": 1},
            {"subject_name": "Programming in Python", "semester": 1},
            {"subject_name": "General English", "semester": 1},
            {"subject_name": "Probability Theory", "semester": 2},
            {"subject_name": "Linear Algebra", "semester": 2},
        ]
        
        db_subjects = []
        for sub in subjects_data:
            subject = models.Subject(**sub)
            db.add(subject)
            db_subjects.append(subject)
        
        db.commit()
        for sub in db_subjects:
            db.refresh(sub)

        # 3. Add Realistic Students
        first_names = ["Mohammad", "Syed", "Nazreen", "Abdul", "Kamrul", "Taha", "Aarav", "Aditi", "Priya", "Rahul", "Zoya", "Karan", "Sneha", "Aisha", "Rohan"]
        last_names = ["Iqbal", "Ali", "Khan", "Aziz", "Hussain", "Rahman", "Sharma", "Gupta", "Patel", "Singh", "Das", "Verma"]
        
        db_students = []
        for i in range(1, 61):  # Creating 60 students
            first = random.choice(first_names)
            last = random.choice(last_names)
            # Generating realistic enrollment numbers (e.g., GN0581)
            enrollment = f"GN{str(500 + i).zfill(4)}" 
            
            student = models.Student(
                enroll_no=enrollment,
                first_name=first,
                last_name=last,
                email=f"{first.lower()}.{last.lower()}{i}@example.com",
                phone=f"98{random.randint(10000000, 99999999)}"
            )
            db.add(student)
            db_students.append(student)
            
        db.commit()
        for std in db_students:
            db.refresh(std)

        # 4. Add Marks (Sessional out of 30, Endsem out of 70)
        sem1_subjects = [s for s in db_subjects if s.semester == 1]
        
        for student in db_students:
            # Create varied student performance profiles for better ML analytics visualization
            profile = random.choice(["excellent", "average", "struggling"])
            
            for subject in sem1_subjects:
                if profile == "excellent":
                    sess = random.randint(24, 29)
                    end = random.randint(55, 68)
                elif profile == "average":
                    sess = random.randint(16, 23)
                    end = random.randint(35, 54)
                else: # struggling
                    sess = random.randint(8, 15)
                    end = random.randint(12, 34)
                
                mark = models.Marks(
                    student_id=student.id,
                    subject_id=subject.id,
                    semester=1,
                    sessional_marks=sess,
                    endsem_marks=end
                )
                db.add(mark)
                
        db.commit()
        print("Database successfully seeded with 60 students and their academic records!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()