import streamlit as st

st.set_page_config(
    page_title="Intelligent ERP Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Intelligent ERP Analytics System")
st.markdown("### An End-to-End MLOps Pipeline for Educational Interventions")

st.markdown("---")

st.markdown("""
Welcome to the **Intelligent ERP Analytics System**, a prototype built for an M.Sc. Data Science dissertation. 
This platform integrates a Machine Learning backend with a centralized educational dashboard to predict student outcomes and facilitate proactive interventions.
""")

st.subheader("🚀 System Modules")

# Create 3 columns for navigation cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 **Admin Dashboard**")
    st.markdown("A restricted overview for faculty and administration to monitor global metrics, pass percentages, and subject-wise performance.")
    st.page_link("pages/1_Admin_Dashboard.py", label="Go to Admin Dashboard", icon="📈")

with col2:
    st.success("👨‍🎓 **Student Dashboard**")
    st.markdown("A personalized portal for students to track their academic marks, VLE (Virtual Learning Environment) engagement, and academic progress.")
    st.page_link("pages/2_Student_Dashboard.py", label="Go to Student Dashboard", icon="🎓")

with col3:
    st.warning("🤖 **ML Analytics**")
    st.markdown("The predictive engine powered by XGBoost. It analyzes historical engagement and scores to identify students at risk of dropping out.")
    st.page_link("pages/3_ML_Analytics.py", label="Go to ML Analytics", icon="🧠")

st.markdown("---")
st.markdown("### 🛠️ Architecture Highlights")
st.markdown("""
* **Backend:** FastAPI (Python) serving a RESTful API.
* **Database:** PostgreSQL hosted in the cloud.
* **Machine Learning:** XGBoost & Random Forest models trained on the OULAD dataset.
* **Frontend:** Streamlit (Python) for real-time interactive dashboards.
""")