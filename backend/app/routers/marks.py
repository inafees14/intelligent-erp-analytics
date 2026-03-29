from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models, schemas

router = APIRouter(prefix="/marks", tags=["Marks"])

PASS_MARK = 40
SESSIONAL_MAX = 30
ENDSEM_MAX = 70

@router.post("/")
def add_or_update_marks(data: schemas.MarksCreate, db: Session = Depends(get_db)):

    # 1️⃣ Validate limits
    if data.sessional_marks > SESSIONAL_MAX:
        raise HTTPException(status_code=400, detail="Sessional marks exceed 30")

    if data.endsem_marks > ENDSEM_MAX:
        raise HTTPException(status_code=400, detail="End Semester marks exceed 70")

    # 2️⃣ TRANSLATE ENROLLMENT NO TO STUDENT ID
    student = db.query(models.Student).filter(models.Student.enroll_no == data.enroll_no).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with Enrollment No '{data.enroll_no}' not found.")

    # 3️⃣ TRANSLATE PAPER CODE TO SUBJECT ID
    subject = db.query(models.Subject).filter(models.Subject.paper_code == data.paper_code).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject with Paper Code '{data.paper_code}' not found.")

    # 4️⃣ Check existing record using the translated integer IDs
    existing = db.query(models.Marks).filter(
        models.Marks.student_id == student.id,
        models.Marks.subject_id == subject.id,
        models.Marks.semester == data.semester
    ).first()

    if existing:
        # Update instead of duplicate
        existing.sessional_marks = data.sessional_marks
        existing.endsem_marks = data.endsem_marks
        existing.num_of_prev_attempts = data.num_of_prev_attempts
        existing.engagement_clicks = data.engagement_clicks
        db.commit()
        return {"message": "Marks updated successfully"}

    # 5️⃣ Insert new record using the translated integer IDs
    new_mark = models.Marks(
        student_id=student.id,
        subject_id=subject.id,
        semester=data.semester,
        sessional_marks=data.sessional_marks,
        endsem_marks=data.endsem_marks,
        num_of_prev_attempts=data.num_of_prev_attempts,
        engagement_clicks=data.engagement_clicks
    )
    db.add(new_mark)
    db.commit()

    return {"message": "Marks added successfully"}