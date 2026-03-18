import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"

st.title("📊 Admin Analytics Dashboard")

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