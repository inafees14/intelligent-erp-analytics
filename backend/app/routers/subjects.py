from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/")
def create_subject(subject_name: str, semester: int, db: Session = Depends(get_db)):
    subject = models.Subject(
        subject_name=subject_name,
        semester=semester
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@router.get("/")
def get_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()