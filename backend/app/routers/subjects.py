from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import models, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/")
def create_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    # Check if paper code already exists
    existing = db.query(models.Subject).filter(models.Subject.paper_code == data.paper_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Subject with this Paper Code already exists.")
        
    subject = models.Subject(**data.dict())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@router.get("/")
def get_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()