"""Initialize database tables."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import engine, Base
from app.models.models import (
    Users, StudentTable, AdminTable, ExamTable, MarksheetTable, StudentFeatures,
)


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
