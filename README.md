# 🎯 AI Career Recommendation System

An AI-powered web application that recommends the most suitable career paths based on user skills, along with course suggestions and skill gap analysis.

---

## 🚀 Features

✅ Role-based login (Student / Parent / Guest)  
✅ AI-based career recommendation system  
✅ Skill gap analysis (what you’re missing)  
✅ Course suggestions based on skills  
✅ Interactive dashboard with charts  
✅ Clean and modern UI (Streamlit)  
✅ Session-based data tracking  
✅ Smart filtering (no random career suggestions)

---

## 🧠 How It Works

1. User enters skills (comma-separated)
2. System processes input using NLP (CountVectorizer)
3. Matches skills with job dataset
4. Calculates similarity scores
5. Recommends:
   - 🎯 Best career match  
   - 💼 Top career options  
   - 📚 Relevant courses  
   - 📉 Missing skills  

---

## 🛠️ Tech Stack

- Python 🐍  
- Streamlit 🎨  
- Pandas 📊  
- Scikit-learn 🤖  

---

## 📂 Project Structure
AI-Career-Recommendation-System/
│
├── frontend/
│ └── app.py
│
├── backend/
│ └── recommender.py
│
├── data/
│ ├── jobs.csv
│ └── courses.csv
│
├── requirements.txt
└── README.md

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run frontend/app.py

📊 Sample Input
skills: python, data analysis, machine learning

📈 Output Includes
🎯 Best Career Match
💼 Career Recommendations
📚 Course Suggestions
📉 Skill Gap

🔐 Future Improvements
Real login authentication system
Database integration (MySQL / Firebase)
Better AI model (ML / Deep Learning)
Resume-based recommendations
Deployment on cloud

👩‍💻 Authors

Deepika Jhaked
Harshita Dubey
Devansh Mishra
