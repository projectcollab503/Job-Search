import streamlit as st
import pandas as pd
import re

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("job_recommendation_dataset.csv")
    df['Required Skills'] = df['Required Skills'].fillna('')
    df['Company'] = df['Company'].fillna('Unknown')
    df['Location'] = df['Location'].fillna('Not Specified')
    df['Salary'] = df['Salary'].fillna('Not Mentioned')
    df['Job Title'] = df['Job Title'].fillna('Unknown')
    return df

df = load_data()

# Clean text
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# Match jobs based on skill presence
def recommend_jobs(user_input, top_n=10):
    user_input = preprocess(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    def matches(row_skills):
        job_skills = preprocess(row_skills).split(",")
        return any(skill in job_skills for skill in user_skills)
    
    filtered = df[df['Required Skills'].apply(matches)]

    if filtered.empty:
        return pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Salary'])

    return filtered[['Job Title', 'Company', 'Location', 'Salary']].drop_duplicates().head(top_n).reset_index(drop=True)

# Streamlit UI
st.set_page_config(page_title="AI Job Recommender", layout="centered")
st.title("💼 Job Recommender Based on Your Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter some skills.")
    else:
        results = recommend_jobs(user_input)
        if results.empty:
            st.error("❌ No matching jobs found.")
        else:
            st.success("✅ Here are job recommendations for your skills:")
            st.dataframe(results, use_container_width=True)
