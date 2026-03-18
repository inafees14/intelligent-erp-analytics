import streamlit as st
import requests
import pandas as pd

import os

API = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("🎓 Student Result Portal")
st.caption("Academic Performance System")

enroll = st.text_input("Enrollment Number", "GN0580")
semester = st.number_input("Semester", min_value=1, max_value=6, value=1)

if st.button("Get Result"):

    response = requests.get(
        f"{API}/analytics/student-result-by-enroll/{enroll}/{semester}"
    )

    data = response.json()

    # error handling
    if "subjects" not in data:
        st.error(data.get("message", "Result not found"))
        st.stop()

    df = pd.DataFrame(data["subjects"])

    st.subheader("Subject Marks")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    col1.metric("Percentage", f"{data['total_percentage']}%")
    col2.metric("GPA", data["GPA"])