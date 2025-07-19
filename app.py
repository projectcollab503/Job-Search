import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load and prepare the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("job_recommendation_dataset.csv")
    df['Required Skills'] = df['Required Skills'].fillna('')
    df['Company'] = df['Company'].fillna('Unknown')
    df['Location'] = df['Location'].fillna('Not Specified')
    df['Salary'] = df['Salary'].fillna('Not Mentioned')
    df['Job Title'] = df['Job Title'].fillna('Unknown')
    # Optional: If you have Industry or Experience Level columns, uncomment below
    # df['Industry'] = df['Industry'].fillna('General')
    return df

df = load_data()

# 🔍 Clean and preprocess skills text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9, ]', '', text)  # remove special characters
    return text

df['Cleaned Skills'] = df['Required Skills'].apply(preprocess_text)

# Vectorize using cleaned skills
vectorizer = TfidfVectorizer()
skill_matrix = vectorizer.fit_transform(df['Cleaned Skills'])

# ✅ Recommend jobs
def recommend_jobs(user_skills, top_n=5):
    cleaned_input = preprocess_text(user_skills)
    user_vec = vectorizer.transform([cleaned_input])
    similarity_scores = cosine_similarity(user_vec, skill_matrix).flatten()
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][['Job Title', 'Company', 'Location', 'Salary', 'Required Skills']].reset_index(drop=True)

# 🌐 Streamlit UI
st.set_page_config(page_title="Job Recommender", layout="centered")
st.title("💼 Job Recommender Based on Your Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, sql, accounting, mechanical engineering")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        st.success("Here are your top job recommendations:")
        st.dataframe(results, use_container_width=True)
