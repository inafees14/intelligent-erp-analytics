import streamlit as st
import requests

import os

API = "https://intelligent-erp-analytics-backend.onrender.com"

st.title("🤖 Machine Learning Analytics")

st.subheader("Model Training Status")

status = requests.get(f"{API}/ml/status").json()

st.info(f"Model Status: {status['model_status']}")

st.subheader("Risk Prediction")

student_id = st.number_input("Student ID", min_value=1)

if st.button("Predict Risk"):

    response = requests.get(f"{API}/ml/predict-risk/{student_id}")
    
    if response.ok:
        result = response.json()
        st.write(result)
        # You can make this look nicer later, e.g., st.metric("Risk Level", result['prediction'])
    else:
        st.error(f"Backend Error: {response.text}")