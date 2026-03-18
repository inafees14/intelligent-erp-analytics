import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("🤖 Machine Learning Analytics")

st.subheader("Model Training Status")

status = requests.get(f"{API}/ml/status").json()

st.info(f"Model Status: {status['model_status']}")

st.subheader("Risk Prediction")

student_id = st.number_input("Student ID", min_value=1)

if st.button("Predict Risk"):

    result = requests.get(
        f"{API}/ml/predict-risk/{student_id}"
    ).json()

    st.write(result)