# ERP Portal Documentation — Statistical & Bayesian Academic Intelligence

## 1. Introduction

This project implements a production-grade ERP Portal integrated with a Statistical, Machine Learning, and Bayesian Academic Intelligence system. It is built following the prescribed internship format with a FastAPI backend, PostgreSQL database, CSS-based frontend, and a Streamlit analytics dashboard.

## 2. Problem Statement

Educational institutions need a comprehensive system to manage student records, marks, and exams while also providing data-driven insights for academic performance analysis. This ERP portal addresses both the administrative needs (user management, marks entry) and the analytical requirements (statistical analysis, ML predictions, Bayesian uncertainty quantification).

## 3. System Architecture

```
┌────────────────────────────────────────────────┐
│                  Frontend                       │
│  ┌──────────────────┐  ┌────────────────────┐  │
│  │  Jinja2 + CSS    │  │  Streamlit         │  │
│  │  (ERP Portal)    │  │  (Analytics)       │  │
│  └────────┬─────────┘  └────────┬───────────┘  │
│           │                      │              │
├───────────┼──────────────────────┼──────────────┤
│           │     FastAPI Backend  │              │
│           ▼                      ▼              │
│  ┌────────────────────────────────────────┐     │
│  │  Authentication  │  Admin  │  Student  │     │
│  │  Routes          │  Routes │  Routes   │     │
│  └────────────────────────────────────────┘     │
│                      │                          │
├──────────────────────┼──────────────────────────┤
│              PostgreSQL Database                 │
│  ┌──────────────────────────────────────┐       │
│  │ Users │ Student │ Admin │ Marksheet  │       │
│  │       │ _table  │ _table│ _table     │       │
│  │ Exam_table │ Student_features        │       │
│  └──────────────────────────────────────┘       │
│                      │                          │
├──────────────────────┼──────────────────────────┤
│          Data Science Layer                      │
│  ┌──────────────────────────────────────┐       │
│  │ Statistical │ ML Models │ Bayesian   │       │
│  │ Analysis    │           │ Model      │       │
│  │             │           │            │       │
│  │ Academic Intelligence Layer          │       │
│  └──────────────────────────────────────┘       │
└────────────────────────────────────────────────┘
```

**Technology Stack:**
- **Backend:** FastAPI (Python 3.9)
- **Database:** PostgreSQL (Heroku Postgres) / SQLite (dev)
- **ORM:** SQLAlchemy
- **Frontend:** Jinja2 templates + CSS (no JS frameworks)
- **Analytics:** Streamlit
- **Deployment:** Heroku with Gunicorn

## 4. ERP Implementation

### Database Schema (Mandatory Tables)

| Table | Columns |
|-------|---------|
| Users | user_id, user_name, user_password, designation |
| Student_table | std_id, user_id, first_name, last_name, phone_no, email_id |
| Admin_table | adm_id, user_id, first_name, last_name, phone_no, email_id |
| Marksheet_table | id, std_id, exam_id, subject_1_marks, subject_2_marks, total_marks |
| Exam_table | exam_id, exam_name, year |
| Student_features | id, std_id, attendance, study_hours, failures *(additional)* |

### ERP Features

**Admin Portal:**
- Secure login with JWT authentication
- Dashboard with student performance overview
- Insert marks by student, exam, and subject
- Manage exams (add, view)
- View all students

**Student Portal:**
- Secure login
- Dashboard with personal analytics and risk assessment
- View marksheet for any exam
- Academic profile with insights

## 5. Statistical Modeling

### Analyses Performed:
- **Pearson & Spearman Correlation:** Measures linear and monotonic relationships between marks, attendance, and study hours
- **Hypothesis Testing:** Independent t-test comparing high vs low study hours groups
- **Linear Regression (OLS):** total_marks ~ attendance + study_hours with full diagnostics
- **ANOVA:** One-way ANOVA across study hour groups
- **Confidence Intervals:** 95% CI for total marks
- **VIF:** Multicollinearity check for predictors

## 6. Machine Learning Modeling

### Regression:
- Linear Regression and Random Forest Regressor
- Metrics: RMSE, MAE, R²
- Feature importance analysis

### Classification:
- Fail defined as total_marks < 10
- Logistic Regression and Random Forest Classifier
- Metrics: ROC-AUC, F1 Score, Confusion Matrix

### Clustering:
- KMeans (k=3) for student performance grouping
- Silhouette Score evaluation
- Cluster profiling

## 7. Bayesian Analysis

### Model Specification:
```
Marks_i ~ Normal(μ_i, σ)
μ_i = α + β₁ × attendance + β₂ × study_hours

Priors:
  α ~ Normal(0, 10)
  β ~ Normal(0, 10)
  σ ~ HalfNormal(10)
```

### Outputs:
- Posterior distributions for all parameters
- 94% HDI credible intervals
- Posterior predictive checks
- Interpretation of uncertainty in predictions

## 8. Results & Evaluation

The system provides:
- Comprehensive ERP functionality for marks and exam management
- Statistical insights revealing relationships between study factors and performance
- ML models for predicting student performance and identifying at-risk students
- Bayesian uncertainty quantification for parameter estimates
- Actionable recommendations for students and administrators

## 9. Deployment

### Heroku Deployment:
```bash
# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-postgres-url

# Deploy
git push heroku main
```

### Configuration:
- **Procfile:** Gunicorn with Uvicorn workers
- **runtime.txt:** Python 3.9.19
- **DATABASE_URL:** Environment variable (no hardcoded credentials)
- **Slug size:** Optimized to stay within 450MB limit

### Running Locally:
```bash
pip install -r requirements.txt
python scripts/init_db.py
python scripts/seed_data.py
uvicorn app.main:app --reload

# Streamlit dashboard (separate terminal)
streamlit run streamlit_app/dashboard.py
```

## 10. Conclusion

This project successfully integrates a compliant ERP portal with advanced data science capabilities. The ERP layer handles all mandatory requirements (user management, marks entry, marksheet viewing), while the data science layer provides statistical analysis, machine learning predictions, Bayesian uncertainty quantification, and an academic intelligence system that generates actionable insights for both administrators and students.
