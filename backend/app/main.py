from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import students, subjects, marks, analytics, ml_analytics
from .seed_data import seed_database

# Create tables
Base.metadata.create_all(bind=engine)

# Used lifespan to run the seed script on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    seed_database()
    yield
    # Anything after yield runs when the server shuts down

app = FastAPI(title="Intelligent ERP Analytics API", lifespan=lifespan)

app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(marks.router)
app.include_router(analytics.router)
app.include_router(ml_analytics.router)

@app.get("/")
def root():
    return {"message": "ERP Backend Running Successfully"}