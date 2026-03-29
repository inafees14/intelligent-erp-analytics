import streamlit as st

st.set_page_config(
    page_title="Home Page",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 XYZ College ERP System")
st.markdown("### Welcome to the Centralized Education Management Portal")

st.markdown("---")

st.markdown("""
**About XYZ College:**
XYZ College is dedicated to fostering academic excellence and empowering students to reach their highest potential. 
Our state-of-the-art ERP system seamlessly integrates student records, academic tracking, and advanced predictive analytics 
to ensure every student receives the proactive support they need to succeed.

Use the navigation menu on the left to access the different modules of the ERP system:
""")

# Navigation Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 **Admin Panel**")
    st.markdown("For faculty and administration to input student marks and oversee institutional pass percentages.")
    st.page_link("pages/1_Admin_Dashboard.py", label="Go to Admin Panel", icon="📈")

with col2:
    st.success("👨‍🎓 **Student Dashboard**")
    st.markdown("For students to securely view their grades, attendance, and personalized academic progress.")
    st.page_link("pages/2_Student_Dashboard.py", label="Go to Student Dashboard", icon="🎓")

with col3:
    st.warning("🤖 **ML Analytics**")
    st.markdown("AI-driven predictions to identify students who may require additional academic assistance.")
    st.page_link("pages/3_ML_Analytics.py", label="Go to ML Analytics", icon="🧠")