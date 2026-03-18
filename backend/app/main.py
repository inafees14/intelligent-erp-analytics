from fastapi import FastAPI
from .database import engine, Base
from .routers import students, subjects, marks, analytics, ml_analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent ERP Analytics API")

app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(marks.router)
app.include_router(analytics.router)
app.include_router(ml_analytics.router)

@app.get("/")
def root():
    return {"message": "ERP Backend Running Successfully"}