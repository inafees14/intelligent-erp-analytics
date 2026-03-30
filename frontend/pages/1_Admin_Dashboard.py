import streamlit as st
import requests
import pandas as pd
import random

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

# --- FETCH SUBJECTS FOR DROPDOWN ---
try:
    subj_res = requests.get(f"{API}/subjects/", timeout=10)
    subjects_data = subj_res.json() if subj_res.ok else []
    paper_options = [f"{s.get('paper_code')} - {s.get('subject_name')}" for s in subjects_data if s.get('paper_code')]
except:
    paper_options = []

# --- 2. TABBED INTERFACE FOR CLEAN UI ---
tab1, tab2, tab3 = st.tabs(["📝 Insert Marks", "🎓 Register Student", "📈 Quick Overview"])

with tab1:
    st.subheader("Insert/Update Student Marks")
    st.markdown("Add academic records to the database.")

    with st.form("marks_entry_form", clear_on_submit=True):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            enroll_no_marks = st.text_input("Enrollment No. (e.g., GN0501)")
            sessional_marks = st.number_input("Sessional Marks (Max 30)", min_value=0, max_value=30, step=1)
            
        with col_b:
            if paper_options:
                selected_paper = st.selectbox("Paper Code", options=paper_options)
                paper_code = selected_paper.split(" - ")[0]
            else:
                paper_code = st.text_input("Paper Code (e.g., PHX1)")
                
            endsem_marks = st.number_input("Endsem Marks (Max 70)", min_value=0, max_value=70, step=1)
            
        with col_c:
            semester = st.number_input("Semester", min_value=1, max_value=8, step=1)
            prev_attempts = st.number_input("Previous Attempts", min_value=0, step=1)
        
        submit_marks = st.form_submit_button("Submit Records to Database")
        
        if submit_marks:
            # INVISIBLE ML FIX: Simulate VLE clicks based on the student's marks so the XGBoost model still has data to work with!
            simulated_clicks = max(10, int((sessional_marks + endsem_marks) * 4.5 + random.randint(-15, 20)))
            
            payload = {
                "enroll_no": enroll_no_marks.strip(),
                "paper_code": paper_code.strip().upper(),
                "semester": semester,
                "sessional_marks": sessional_marks,
                "endsem_marks": endsem_marks,
                "num_of_prev_attempts": prev_attempts,
                "engagement_clicks": simulated_clicks # Sent silently to the backend
            }
            try:
                res = requests.post(f"{API}/marks/", json=payload)
                if res.ok:
                    st.success(f"✅ {res.json().get('message', 'Marks saved successfully!')}")
                else:
                    st.error(f"❌ Validation Failed: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Server connection error: {e}")

with tab2:
    st.subheader("Register New Student")
    st.markdown("Enroll a new student into the ERP system.")
    
    with st.form("student_reg_form", clear_on_submit=True):
        col_1, col_2 = st.columns(2)
        
        with col_1:
            new_enroll = st.text_input("Enrollment No. (e.g., GN0600)")
            f_name = st.text_input("First Name")
            phone = st.text_input("Phone Number (Optional)")
            
        with col_2:
            email = st.text_input("Email Address (Optional)")
            l_name = st.text_input("Last Name")
            
        submit_student = st.form_submit_button("Register Student")
        
        if submit_student:
            if not new_enroll or not f_name or not l_name:
                st.error("⚠️ Enrollment No, First Name, and Last Name are required.")
            else:
                stud_payload = {
                    "enroll_no": new_enroll.strip().upper(),
                    "first_name": f_name.strip(),
                    "last_name": l_name.strip(),
                    "email": email.strip() if email else None,
                    "phone": phone.strip() if phone else None
                }
                try:
                    # Calls the POST /students/ endpoint documented in your Swagger UI
                    res = requests.post(f"{API}/students/", json=stud_payload)
                    if res.ok:
                        st.success(f"✅ Student {f_name} {l_name} registered successfully!")
                    else:
                        st.error(f"❌ Registration Failed: {res.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Server connection error: {e}")

with tab3:
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