from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..dependencies import get_db
from .. import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# 1️⃣ Subject Average
@router.get("/subject-average")
def subject_average(db: Session = Depends(get_db)):

    total_marks_expr = (
        models.Marks.sessional_marks +
        models.Marks.endsem_marks
    )

    results = (
        db.query(
            models.Subject.subject_name,
            func.avg(total_marks_expr).label("average_marks")
        )
        .join(models.Marks, models.Subject.id == models.Marks.subject_id)
        .group_by(models.Subject.subject_name)
        .all()
    )

    return [
        {"subject": r[0], "average_marks": round(r[1], 2)}
        for r in results
    ]


# 2️⃣ Top Students
@router.get("/top-students")
def top_students(db: Session = Depends(get_db)):

    total_marks_expr = (
        models.Marks.sessional_marks +
        models.Marks.endsem_marks
    )

    results = (
        db.query(
            models.Student.first_name,
            models.Student.last_name,
            func.sum(total_marks_expr).label("total_marks")
        )
        .join(models.Marks, models.Student.id == models.Marks.student_id)
        .group_by(models.Student.id)
        .order_by(func.sum(total_marks_expr).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "name": f"{r[0]} {r[1]}",
            "total_marks": r[2]
        }
        for r in results
    ]


# 3️⃣ Marks Distribution
@router.get("/marks-distribution")
def marks_distribution(db: Session = Depends(get_db)):

    records = db.query(
        models.Marks.sessional_marks,
        models.Marks.endsem_marks
    ).all()

    marks_list = [
        r[0] + r[1]
        for r in records
    ]

    return {"marks": marks_list}


# 4️⃣ Pass Percentage
@router.get("/pass-percentage")
def pass_percentage(db: Session = Depends(get_db)):

    total_marks_expr = (
        models.Marks.sessional_marks +
        models.Marks.endsem_marks
    )

    total = db.query(models.Marks).count()

    passed = db.query(models.Marks).filter(
        total_marks_expr >= 40
    ).count()

    if total == 0:
        return {"pass_percentage": 0}

    percentage = (passed / total) * 100
    return {"pass_percentage": round(percentage, 2)}


# 5️⃣ Student Result by Enrollment
@router.get("/student-result-by-enroll/{enroll}/{semester}")
def student_result_by_enroll(enroll: str, semester: int, db: Session = Depends(get_db)):

    # Find student using enrollment number
    student = db.query(models.Student).filter(
        models.Student.enroll_no == enroll
    ).first()

    if not student:
        return {"message": "Student not found"}

    # Fetch marks
    records = db.query(models.Marks).filter(
        models.Marks.student_id == student.id,
        models.Marks.semester == semester
    ).all()

    if not records:
        return {"message": "No records found"}

    total_marks = 0
    max_marks = 100 * len(records)

    subjects = []

    for r in records:
        total = r.sessional_marks + r.endsem_marks
        total_marks += total

        subjects.append({
            "subject": r.subject.subject_name,
            "sessional": r.sessional_marks,
            "endsem": r.endsem_marks,
            "total": total,
            "status": "Pass" if total >= 40 else "Fail"
        })

    percentage = (total_marks / max_marks) * 100
    gpa = round(percentage / 9.0, 2)

    return {
        "student": f"{student.first_name} {student.last_name}",
        "enroll_no": student.enroll_no,
        "semester": semester,
        "subjects": subjects,
        "total_percentage": round(percentage, 2),
        "GPA": gpa
    }