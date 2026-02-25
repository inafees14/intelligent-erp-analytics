from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.models import (
    Users, StudentTable, AdminTable, MarksheetTable, ExamTable, StudentFeatures,
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


def require_admin(request: Request, db: Session):
    user = get_current_user(request, db)
    if not user or user.designation != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_admin(request, db)
    admin = db.query(AdminTable).filter(AdminTable.user_id == user.user_id).first()

    total_students = db.query(StudentTable).count()
    total_exams = db.query(ExamTable).count()
    total_marksheets = db.query(MarksheetTable).count()

    avg_marks = db.query(func.avg(MarksheetTable.total_marks)).scalar() or 0
    max_marks = db.query(func.max(MarksheetTable.total_marks)).scalar() or 0
    min_marks = db.query(func.min(MarksheetTable.total_marks)).scalar() or 0

    recent_marks = (
        db.query(MarksheetTable)
        .join(StudentTable)
        .join(ExamTable)
        .order_by(MarksheetTable.id.desc())
        .limit(10)
        .all()
    )

    pass_count = db.query(MarksheetTable).filter(MarksheetTable.total_marks >= 10).count()
    fail_count = db.query(MarksheetTable).filter(MarksheetTable.total_marks < 10).count()

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "admin": admin,
            "total_students": total_students,
            "total_exams": total_exams,
            "total_marksheets": total_marksheets,
            "avg_marks": round(avg_marks, 2),
            "max_marks": max_marks,
            "min_marks": min_marks,
            "recent_marks": recent_marks,
            "pass_count": pass_count,
            "fail_count": fail_count,
        },
    )


@router.get("/insert-marks", response_class=HTMLResponse)
async def insert_marks_form(request: Request, db: Session = Depends(get_db)):
    require_admin(request, db)
    students = db.query(StudentTable).all()
    exams = db.query(ExamTable).all()
    return templates.TemplateResponse(
        "admin/insert_marks.html",
        {"request": request, "students": students, "exams": exams},
    )


@router.post("/insert-marks")
async def insert_marks(
    request: Request,
    std_id: int = Form(...),
    exam_id: int = Form(...),
    subject_1_marks: float = Form(...),
    subject_2_marks: float = Form(...),
    db: Session = Depends(get_db),
):
    require_admin(request, db)
    total_marks = subject_1_marks + subject_2_marks
    marksheet = MarksheetTable(
        std_id=std_id,
        exam_id=exam_id,
        subject_1_marks=subject_1_marks,
        subject_2_marks=subject_2_marks,
        total_marks=total_marks,
    )
    db.add(marksheet)
    db.commit()
    return RedirectResponse(url="/admin/dashboard?success=1", status_code=303)


@router.get("/manage-exams", response_class=HTMLResponse)
async def manage_exams(request: Request, db: Session = Depends(get_db)):
    require_admin(request, db)
    exams = db.query(ExamTable).order_by(ExamTable.year.desc()).all()
    return templates.TemplateResponse(
        "admin/manage_exams.html",
        {"request": request, "exams": exams},
    )


@router.post("/add-exam")
async def add_exam(
    request: Request,
    exam_name: str = Form(...),
    year: int = Form(...),
    db: Session = Depends(get_db),
):
    require_admin(request, db)
    exam = ExamTable(exam_name=exam_name, year=year)
    db.add(exam)
    db.commit()
    return RedirectResponse(url="/admin/manage-exams", status_code=303)


@router.get("/students", response_class=HTMLResponse)
async def list_students(request: Request, db: Session = Depends(get_db)):
    require_admin(request, db)
    students = db.query(StudentTable).all()
    return templates.TemplateResponse(
        "admin/students.html",
        {"request": request, "students": students},
    )
