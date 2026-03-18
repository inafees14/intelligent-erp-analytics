import random
import os
from app.database import engine, Base, SessionLocal
from app import models

# Remove old DB
if os.path.exists("erp.db"):
    os.remove("erp.db")

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ---------------- STUDENTS ----------------
students = [
    ("GN0580","NAFEES","IQBAL","Physics"),
    ("GN0028","SHUMAYAL","ALI","Economics"),
    ("GM9000","ZAINUL","MEHDI","Physics"),
    ("GM9999","AAMIR","SUHAIL","Economics"),
    ("GM8687","TALHA","USMANI","Physics"),
    ("GM8789","FARHAN","KHAN","Economics"),
    ("GN1001","RAHIL","ANSARI","Physics"),
    ("GN1002","SAAD","SIDDIQUI","Economics"),
    ("GN1003","ARHAM","RIZVI","Physics"),
    ("GN1004","HAMZA","QURESHI","Economics")
]

student_objs = []
for e,f,l,s in students:
    obj = models.Student(
        enroll_no=e,
        first_name=f,
        last_name=l,
        email=f.lower()+"@test.com",
        phone="9999999999"
    )
    db.add(obj)
    student_objs.append(obj)

db.commit()

# ---------------- SUBJECTS ----------------
subjects = [
    ("Statistics-I",1),
    ("Mathematics-I",1),
    ("Physics-I",1),
    ("Economics-I",1),
    ("English-I",1),
    ("Urdu-B",1),

    ("Statistics-II",2),
    ("Mathematics-II",2),
    ("Physics-II",2),
    ("Economics-II",2),
    ("English-II",2)
]

subject_objs = []
for name, sem in subjects:
    obj = models.Subject(subject_name=name, semester=sem)
    db.add(obj)
    subject_objs.append(obj)

db.commit()

# ---------------- MARKS ----------------
for student in student_objs:
    for subject in subject_objs:

        # Skip Physics for Economics students
        if "Physics" in subject.subject_name and student.id % 2 == 0:
            continue

        # Skip Economics for Physics students
        if "Economics" in subject.subject_name and student.id % 2 != 0:
            continue

        sessional = random.randint(10,30)
        endsem = random.randint(20,70)

        mark = models.Marks(
            student_id=student.id,
            subject_id=subject.id,
            semester=subject.semester,
            sessional_marks=sessional,
            endsem_marks=endsem
        )

        db.add(mark)

db.commit()
db.close()

print("Correct erp.db created successfully ✅")