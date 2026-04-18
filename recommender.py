import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Load data directly (no data/ folder)
jobs = pd.read_csv("jobs.csv")
courses = pd.read_csv("courses.csv")

jobs.dropna(inplace=True)

# Combine text for better matching
jobs['combined'] = jobs['Job_Title'] + " " + jobs['Skills']

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(jobs['combined'])


def recommend_career(user_skills):
    user_skills = user_skills.lower()

    filtered_jobs = jobs[jobs['Skills'].str.contains('|'.join(user_skills.split(',')), case=False)]

    if filtered_jobs.empty:
        filtered_jobs = jobs

    filtered_matrix = vectorizer.transform(filtered_jobs['combined'])

    user_vector = vectorizer.transform([user_skills])
    similarity = cosine_similarity(user_vector, filtered_matrix)

    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []
    for i in scores[:5]:
        job = filtered_jobs.iloc[i[0]]['Job_Title']
        score = round(i[1] * 100, 2)
        if score > 5:
            results.append((job, score))

    return results, scores


def recommend_courses(user_skills):
    skill_list = [s.strip().lower() for s in user_skills.split(",")]

    result = courses[courses['skills'].apply(
        lambda x: any(skill in x.lower() for skill in skill_list)
    )]

    return result['course_name'].head(5).tolist()


def skill_gap(user_skills, job_index):
    job_skills = jobs.iloc[job_index]['Skills'].lower().split(" ")
    user_skills = [s.strip().lower() for s in user_skills.split(",")]

    missing = [skill for skill in job_skills if skill not in user_skills]
    return list(set(missing))[:5]
