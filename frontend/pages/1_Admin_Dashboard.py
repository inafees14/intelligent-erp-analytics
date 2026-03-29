import streamlit as st
import requests
import pandas as pd

API = "https://intelligent-erp-analytics-backend.onrender.com"

st.title("📊 Admin Panel")

# --- 1. SECURE LOGIN GATE ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.info("Restricted Access: Please log in to the XYZ College Admin Portal.")
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == "AdminOffice" and password == "Admin@123":
                st.session_state.admin_logged_in = True
                st.success("Login successful!")
                st.rerun() 
            else:
                st.error("Invalid credentials.")
    st.stop() 

col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

st.divider()

# --- 2. STUDENT MARKS ENTRY FORM ---
st.subheader("📝 Insert/Update Student Marks")
st.markdown("Use this form to add academic records and VLE engagement data to the database.")

with st.form("marks_entry_form", clear_on_submit=True):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        enroll_no = st.text_input("Enrollment No. (e.g., GN0501)")
        sessional_marks = st.number_input("Sessional Marks (Max 30)", min_value=0, max_value=30, step=1)
        engagement_clicks = st.number_input("VLE Engagement Clicks", min_value=0, step=1)
        
    with col_b:
        paper_code = st.text_input("Paper Code (e.g., PHX1)")
        endsem_marks = st.number_input("Endsem Marks (Max 70)", min_value=0, max_value=70, step=1)
        
    with col_c:
        semester = st.number_input("Semester", min_value=1, max_value=8, step=1)
        prev_attempts = st.number_input("Previous Attempts", min_value=0, step=1)
    
    submit_marks = st.form_submit_button("Submit Records to Database")
    
    if submit_marks:
        payload = {
            "enroll_no": enroll_no.strip(),
            "paper_code": paper_code.strip().upper(), # Auto-capitalizes the code!
            "semester": semester,
            "sessional_marks": sessional_marks,
            "endsem_marks": endsem_marks,
            "num_of_prev_attempts": prev_attempts,
            "engagement_clicks": engagement_clicks
        }
        try:
            res = requests.post(f"{API}/marks/", json=payload)
            if res.ok:
                st.success(f"✅ {res.json().get('message', 'Marks saved successfully!')}")
            else:
                st.error(f"❌ Validation Failed: {res.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Server connection error: {e}")

st.divider()

# --- 3. QUICK OVERVIEW (Graphs Removed) ---
st.subheader("📈 Quick Overview")

col_m1, col_m2 = st.columns(2)

def fetch_data(endpoint):
    try:
        res = requests.get(f"{API}/{endpoint}", timeout=10)
        return res.json() if res.ok else []
    except:
        return []

with col_m1:
    pass_data = fetch_data("analytics/pass-percentage")
    if isinstance(pass_data, dict) and "pass_percentage" in pass_data:
        st.metric("College Overall Pass Percentage", f"{pass_data['pass_percentage']}%")

with col_m2:
    st.write("**Top Performing Students**")
    df_top = pd.DataFrame(fetch_data("analytics/top-students"))
    if not df_top.empty:
        st.dataframe(df_top, use_container_width=True)
    else:
        st.info("No data available.")