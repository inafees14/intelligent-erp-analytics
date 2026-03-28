from pydantic import BaseModel
from typing import Optional


# ---------- STUDENT ----------

class StudentCreate(BaseModel):
    enroll_no: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class StudentOut(StudentCreate):
    id: int

    class Config:
        from_attributes = True


# ---------- SUBJECT ----------
class SubjectCreate(BaseModel):
    subject_name: str
    semester: int
    credits: int = 4
    weight: int = 100

class SubjectOut(SubjectCreate):
    id: int
    class Config:
        from_attributes = True


# ---------- EXAM ----------

class ExamCreate(BaseModel):
    exam_name: str
    year: int
    semester: int


class ExamOut(ExamCreate):
    id: int

    class Config:
        from_attributes = True


# ---------- MARKS ----------
class MarksCreate(BaseModel):
    student_id: int
    subject_id: int
    semester: int
    sessional_marks: int
    endsem_marks: int
    num_of_prev_attempts: int = 0
    engagement_clicks: int = 0

class MarksOut(MarksCreate):
    id: int
    class Config:
        from_attributes = True