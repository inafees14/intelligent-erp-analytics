import streamlit as st
import requests
import os

API = "https://intelligent-erp-analytics-backend.onrender.com"

st.title("🤖 Machine Learning Analytics")
st.subheader("Model Training Status")

try:
    status = requests.get(f"{API}/ml/status").json()
    if status.get('model_status') == 'trained':
        st.success("✅ Model Status: Active & Trained (XGBoost)")
    else:
        st.warning("⚠️ Model Status: Not Trained")
except:
    st.error("Backend API is currently unreachable.")

st.divider()

st.subheader("Student Risk Prediction")
st.markdown("Analyze a student's VLE engagement and academic performance to predict dropout risk.")

# CHANGED: Text Input for Enrollment Number
enroll_no = st.text_input("Enter Student Enrollment Number (e.g., GN0501)", "GN0501")

if st.button("Predict Risk", type="primary"):
    with st.spinner(f"Analyzing data for {enroll_no}..."):
        response = requests.get(f"{API}/ml/predict-risk/{enroll_no}")
        
        if response.ok:
            result = response.json()
            
            # Create a nice layout for the results
            col1, col2 = st.columns(2)
            
            with col1:
                # Color code the prediction
                risk_color = "red" if result['prediction'] == "At Risk" else "green"
                st.markdown(f"### Prediction: :{risk_color}[{result['prediction']}]")
                st.write(f"**Student:** {result['student_name']}")
                
            with col2:
                # Show probability as a percentage
                prob_percentage = result['risk_probability'] * 100
                st.metric(label="Probability of Dropout", value=f"{prob_percentage:.1f}%")
            
            # Hide the raw data inside an expander so the UI stays clean
            with st.expander("View Raw Model Features (Extracted from DB)"):
                st.json(result['model_inputs'])
                
        else:
            try:
                error_msg = response.json().get('detail', 'Unknown Error')
            except:
                error_msg = response.text
            st.error(f"Error: {error_msg}")