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

    total = data.sessional_marks + data.endsem_marks

    # 2️⃣ Check existing record
    existing = db.query(models.Marks).filter(
        models.Marks.student_id == data.student_id,
        models.Marks.subject_id == data.subject_id,
        models.Marks.semester == data.semester
    ).first()

    if existing:
        # Update instead of duplicate
        existing.sessional_marks = data.sessional_marks
        existing.endsem_marks = data.endsem_marks
        db.commit()
        return {"message": "Marks updated successfully"}

    # 3️⃣ Insert new
    new_mark = models.Marks(**data.dict())
    db.add(new_mark)
    db.commit()

    return {"message": "Marks added successfully"}