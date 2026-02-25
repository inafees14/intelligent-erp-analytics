from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.database as database
from app.models.models import (
    Users, StudentTable, AdminTable, MarksheetTable, ExamTable, StudentFeatures,
)
from app.routers import auth, admin, student

app = FastAPI(title="ERP Portal - Statistical & Bayesian Academic Intelligence")


@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(student.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
