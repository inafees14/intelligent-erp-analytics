from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.models import (
    Users, StudentTable, MarksheetTable, ExamTable, StudentFeatures,
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/student")
templates = Jinja2Templates(directory="app/templates")


def require_student(request: Request, db: Session):
    user = get_current_user(request, db)
    if not user or user.designation != "student":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


@router.get("/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_student(request, db)
    student = db.query(StudentTable).filter(StudentTable.user_id == user.user_id).first()

    marksheets = (
        db.query(MarksheetTable)
        .filter(MarksheetTable.std_id == student.std_id)
        .join(ExamTable)
        .all()
    )

    features = (
        db.query(StudentFeatures)
        .filter(StudentFeatures.std_id == student.std_id)
        .first()
    )

    avg_total = 0
    if marksheets:
        avg_total = round(sum(m.total_marks for m in marksheets) / len(marksheets), 2)

    risk_level = "Low"
    if features and features.failures and features.failures >= 2:
        risk_level = "High"
    elif features and features.failures and features.failures >= 1:
        risk_level = "Medium"

    return templates.TemplateResponse(
        "student/dashboard.html",
        {
            "request": request,
            "student": student,
            "marksheets": marksheets,
            "features": features,
            "avg_total": avg_total,
            "risk_level": risk_level,
        },
    )


@router.get("/marksheet", response_class=HTMLResponse)
async def view_marksheet(request: Request, db: Session = Depends(get_db)):
    user = require_student(request, db)
    student = db.query(StudentTable).filter(StudentTable.user_id == user.user_id).first()
    exams = db.query(ExamTable).all()
    return templates.TemplateResponse(
        "student/marksheet.html",
        {"request": request, "student": student, "exams": exams},
    )


@router.get("/marksheet/{exam_id}", response_class=HTMLResponse)
async def view_marksheet_detail(
    request: Request, exam_id: int, db: Session = Depends(get_db)
):
    user = require_student(request, db)
    student = db.query(StudentTable).filter(StudentTable.user_id == user.user_id).first()

    marksheet = (
        db.query(MarksheetTable)
        .filter(
            MarksheetTable.std_id == student.std_id,
            MarksheetTable.exam_id == exam_id,
        )
        .first()
    )

    exam = db.query(ExamTable).filter(ExamTable.exam_id == exam_id).first()

    return templates.TemplateResponse(
        "student/marksheet_detail.html",
        {
            "request": request,
            "student": student,
            "marksheet": marksheet,
            "exam": exam,
        },
    )
