import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import datetime

from backend.recommender import recommend_career, recommend_courses, skill_gap

st.set_page_config(page_title="Career AI", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
h1, h2, h3 {
    color: #1f2937;
}
.card {
    background: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
.metric {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

if "skills" not in st.session_state:
    st.session_state.skills = ""

if "careers" not in st.session_state:
    st.session_state.careers = []

if "courses" not in st.session_state:
    st.session_state.courses = []

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:
    st.title("🔐 Career AI Login")

    role = st.selectbox("Login as", ["Student", "Parent", "Guest"])
    name = st.text_input("Name")

    roll = ""
    aadhar = ""

    if role == "Student":
        roll = st.text_input("Roll Number (6 digits)")
    elif role == "Parent":
        aadhar = st.text_input("Aadhar (12 digits)")

    if st.button("Login"):
        if role == "Guest":
            st.session_state.logged_in = True
            st.session_state.role = role

        elif role == "Student" and roll.isdigit() and len(roll) == 6:
            st.session_state.logged_in = True
            st.session_state.role = role

        elif role == "Parent" and aadhar.isdigit() and len(aadhar) == 12:
            st.session_state.logged_in = True
            st.session_state.role = role

        else:
            st.error("Invalid details")

    st.stop()

# ---------------- MAIN ----------------
st.title("🎯 Career Recommendation Platform")

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 Recommendation", "📜 History"])

# ---------------- DASHBOARD ----------------
with tab1:
    st.subheader("📊 Dashboard")

    skills = st.session_state.skills
    careers = st.session_state.careers
    courses = st.session_state.courses

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='metric'><h4>Skills</h4><h2>{len(skills.split(',')) if skills else 0}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric'><h4>Careers</h4><h2>{len(careers)}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric'><h4>Courses</h4><h2>{len(courses)}</h2></div>", unsafe_allow_html=True)

    st.write("")

    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        counts = Counter(skill_list)

        df = pd.DataFrame({
            "Skills": list(counts.keys()),
            "Count": list(counts.values())
        })

        colA, colB = st.columns(2)

        with colA:
            st.subheader("Skill Distribution")
            st.bar_chart(df.set_index("Skills"))

        with colB:
            fig, ax = plt.subplots()
            ax.pie(df["Count"], labels=df["Skills"], autopct='%1.1f%%')
            st.pyplot(fig)

# ---------------- RECOMMENDATION ----------------
with tab2:
    st.subheader("🤖 AI Recommendation")

    skills_input = st.text_input("Enter skills (comma separated)")

    if st.button("🚀 Recommend"):
        if skills_input:
            with st.spinner("Analyzing your profile..."):
                results, scores = recommend_career(skills_input)
                courses = recommend_courses(skills_input)

            # SAVE DATA
            st.session_state.skills = skills_input
            st.session_state.careers = [r[0] for r in results]
            st.session_state.courses = courses

            st.session_state.history.append({
                "skills": skills_input,
                "career": results[0][0] if results else "None",
                "time": str(datetime.datetime.now())
            })

            # 🔥 FIX: force refresh
            st.rerun()

    # SHOW RESULTS
    if st.session_state.careers:

        st.subheader("⭐ Best Career Match")
        st.success(st.session_state.careers[0])

        st.subheader("💼 Career Recommendations")
        for c in st.session_state.careers:
            st.markdown(f"<div class='card'>💼 {c}</div>", unsafe_allow_html=True)

        st.subheader("📚 Recommended Courses")
        for c in st.session_state.courses:
            st.markdown(f"<div class='card'>📘 {c}</div>", unsafe_allow_html=True)

        st.subheader("📉 Skill Gap")
        results, scores = recommend_career(st.session_state.skills)
        if scores:
            missing = skill_gap(st.session_state.skills, scores[0][0])
            for m in missing:
                st.markdown(f"<div class='card'>❌ {m}</div>", unsafe_allow_html=True)

# ---------------- HISTORY ----------------
with tab3:
    st.subheader("📜 History")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
    else:
        st.write("No history yet")