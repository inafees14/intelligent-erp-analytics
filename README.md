# ERP Portal — Statistical & Bayesian Academic Intelligence

A production-grade ERP Portal integrated with Statistical, Machine Learning, and Bayesian Academic Intelligence, built with FastAPI, PostgreSQL, and Streamlit.

## Features

### ERP Portal
- **Admin:** Login, insert marks, manage exams, view students, performance dashboard
- **Student:** Login, view marksheet, personal analytics, risk assessment
- **Authentication:** JWT-based secure login with bcrypt password hashing

### Data Science
- **Statistical Analysis:** Pearson/Spearman correlation, hypothesis testing, linear regression, ANOVA, confidence intervals, VIF
- **Machine Learning:** Linear/Random Forest regression, Logistic/RF classification, KMeans clustering
- **Bayesian Modelling:** PyMC-based hierarchical model with posterior distributions and credible intervals
- **Academic Intelligence:** Performance prediction, risk probability, feature importance, personalized insights

## Tech Stack
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL (Heroku) / SQLite (dev)
- **Frontend:** Jinja2 + CSS (no JS frameworks)
- **Analytics:** Streamlit
- **Deployment:** Heroku + Gunicorn

## Quick Start

```bash
pip install -r requirements.txt
python scripts/init_db.py
python scripts/seed_data.py
uvicorn app.main:app --reload
```

Streamlit dashboard (separate terminal):
```bash
streamlit run streamlit_app/dashboard.py
```

## Default Credentials
- **Admin:** username: `admin`, password: `admin123`
- **Student:** username: `student1`, password: `pass123`

## Project Structure
```
├── app/                    # FastAPI application
│   ├── main.py            # Entry point
│   ├── config.py          # Configuration
│   ├── database.py        # Database connection
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API routes (auth, admin, student)
│   ├── templates/         # Jinja2 HTML templates
│   └── static/css/        # Stylesheets
├── data_science/          # Data science modules
│   ├── data_loader.py     # UCI dataset loader
│   ├── statistical_analysis.py
│   ├── ml_models.py
│   ├── bayesian_model.py
│   └── academic_intelligence.py
├── streamlit_app/         # Streamlit analytics dashboard
├── data/                  # UCI Student Performance Dataset
├── scripts/               # DB init and seed scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
├── Procfile               # Heroku deployment
├── runtime.txt            # Python version
└── requirements.txt       # Dependencies
```

## Dataset
Uses the UCI Student Performance Dataset with mapping:
- G1 → subject_1_marks
- G2 → subject_2_marks
- G3 → total_marks
- absences → attendance
- studytime → study_hours
- failures → risk indicator

## Testing
```bash
python -m pytest tests/ -v
```

## Documentation
See [docs/documentation.md](docs/documentation.md) for full project documentation.
