# backend/app/seed_data.py
import random
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models

def seed_database():
    db: Session = SessionLocal()
    try:
        if db.query(models.Student).first():
            print("Database already seeded. Skipping initial data injection...")
            return

        print("Empty database detected. Seeding with ML-ready feature data...")

        # 2. Add Subjects with Credits and Weight
        subjects_data = [
            {"subject_name": "Descriptive Statistics", "semester": 1, "credits": 4, "weight": 100},
            {"subject_name": "Calculus & Matrices", "semester": 1, "credits": 4, "weight": 100},
            {"subject_name": "Physics I", "semester": 1, "credits": 3, "weight": 100},
            {"subject_name": "Programming in Python", "semester": 1, "credits": 3, "weight": 100},
            {"subject_name": "General English", "semester": 1, "credits": 2, "weight": 100},
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
        first_names = ["Syed", "Nazreen", "Abdul", "Kamrul", "Taha", "Aarav", "Aditi", "Priya", "Rahul", "Zoya", "Karan", "Sneha", "Aisha", "Rohan"]
        last_names = ["Ali", "Khan", "Aziz", "Hussain", "Rahman", "Sharma", "Gupta", "Patel", "Singh", "Das", "Verma"]
        
        db_students = []
        for i in range(1, 61):  
            first = random.choice(first_names)
            last = random.choice(last_names)
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

        # 4. Add ML-Ready Marks & Engagement
        sem1_subjects = [s for s in db_subjects if s.semester == 1]
        
        for student in db_students:
            # 5% chance of being a repeat student
            prev_attempts = 1 if random.random() > 0.95 else 0 
            
            for subject in sem1_subjects:
                sess = int(random.gauss(21, 4))
                sess = max(0, min(30, sess))
                
                end = int(random.gauss(48, 10))
                end = max(0, min(70, end))
                
                # Correlate engagement clicks with performance (higher marks = more clicks)
                total_score = sess + end
                base_clicks = total_score * 5 
                clicks = int(random.gauss(base_clicks, 50))
                clicks = max(10, clicks) # Minimum 10 clicks
                
                mark = models.Marks(
                    student_id=student.id,
                    subject_id=subject.id,
                    semester=1,
                    sessional_marks=sess,
                    endsem_marks=end,
                    num_of_prev_attempts=prev_attempts,
                    engagement_clicks=clicks
                )
                db.add(mark)
                
        db.commit()
        print("Database successfully seeded with ML features (credits, clicks, attempts)!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()