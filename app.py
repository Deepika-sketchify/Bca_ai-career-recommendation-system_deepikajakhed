import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import datetime

# ✅ Correct import
from recommender import recommend_career, recommend_courses, skill_gap

st.set_page_config(page_title="Career AI", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #f5f7fa; }
.card {
    background: white;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.metric {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
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

        elif role == "Student" and roll.isdigit() and len(roll) == 6:
            st.session_state.logged_in = True

        elif role == "Parent" and aadhar.isdigit() and len(aadhar) == 12:
            st.session_state.logged_in = True

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

    col1.metric("Skills", len(skills.split(',')) if skills else 0)
    col2.metric("Careers", len(careers))
    col3.metric("Courses", len(courses))

    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",")]
        counts = Counter(skill_list)

        df = pd.DataFrame({
            "Skills": list(counts.keys()),
            "Count": list(counts.values())
        })

        st.bar_chart(df.set_index("Skills"))

# ---------------- RECOMMEND ----------------
with tab2:
    st.subheader("🤖 AI Recommendation")

    skills_input = st.text_input("Enter skills (comma separated)")

    if st.button("🚀 Recommend"):
        if skills_input:
            results, scores = recommend_career(skills_input)
            courses = recommend_courses(skills_input)

            st.session_state.skills = skills_input
            st.session_state.careers = [r[0] for r in results]
            st.session_state.courses = courses

            st.session_state.history.append({
                "skills": skills_input,
                "career": results[0][0] if results else "None",
                "time": str(datetime.datetime.now())
            })

            st.rerun()

    if st.session_state.careers:
        st.success(st.session_state.careers[0])

        for c in st.session_state.careers:
            st.write("💼", c)

        for c in st.session_state.courses:
            st.write("📘", c)

        results, scores = recommend_career(st.session_state.skills)
        if scores:
            missing = skill_gap(st.session_state.skills, scores[0][0])
            for m in missing:
                st.write("❌", m)

# ---------------- HISTORY ----------------
with tab3:
    st.subheader("📜 History")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)
    else:
        st.write("No history yet")
