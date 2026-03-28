import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "https://intelligent-erp-analytics-backend.onrender.com"

st.title("📊 Admin Analytics Dashboard")

# --- 1. INITIALIZE LOGIN STATE ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# --- 2. LOGIN FORM GATE ---
if not st.session_state.admin_logged_in:
    st.info("Restricted Access: Please log in to view analytics.")
    
    # Using st.form keeps the page from reloading until they click "Login"
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == "AdminOffice" and password == "Admin@123":
                st.session_state.admin_logged_in = True
                st.success("Login successful!")
                st.rerun()  # Forces Streamlit to instantly reload the page
            else:
                st.error("Invalid username or password.")
                
    # CRITICAL: This stops the code here. The charts below won't load!
    st.stop()

# --- 3. DASHBOARD (Only visible if logged in) ---

# Add a logout button to the top right
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

st.divider()

# SUBJECT AVERAGE
st.subheader("Subject Average")
data = requests.get(f"{API}/analytics/subject-average").json()
df = pd.DataFrame(data)
fig = px.bar(df, x="subject", y="average_marks", title="Average Marks per Subject")
st.plotly_chart(fig)

# TOP STUDENTS
st.subheader("Top Students")
data = requests.get(f"{API}/analytics/top-students").json()
df = pd.DataFrame(data)
st.table(df)

# PASS PERCENTAGE
st.subheader("Pass Percentage")
data = requests.get(f"{API}/analytics/pass-percentage").json()
st.metric("Pass Percentage", f"{data['pass_percentage']}%")

# MARKS DISTRIBUTION
st.subheader("Marks Distribution")
data = requests.get(f"{API}/analytics/marks-distribution").json()
df = pd.DataFrame(data)
fig = px.histogram(df, x="marks", nbins=10)
st.plotly_chart(fig)