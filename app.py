import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and prepare the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("job_data.csv")
    df['Required Skills'] = df['Required Skills'].fillna('')
    df['Company'] = df['Company'].fillna('Unknown')
    df['Location'] = df['Location'].fillna('Not Specified')
    df['Salary'] = df['Salary'].fillna('Not Mentioned')
    df['Job Title'] = df['Job Title'].fillna('Unknown')
    return df

df = load_data()

# Vectorize skills
vectorizer = TfidfVectorizer()
skill_matrix = vectorizer.fit_transform(df['Required Skills'])

# Recommend jobs
def recommend_jobs(user_skills, top_n=5):
    user_vec = vectorizer.transform([user_skills])
    similarity = cosine_similarity(user_vec, skill_matrix).flatten()
    indices = similarity.argsort()[-top_n:][::-1]
    return df.iloc[indices][['Job Title', 'Company', 'Location', 'Salary']].reset_index(drop=True)

# Streamlit UI
st.title("💼 Job Recommender Based on Your Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, sql, machine learning")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        st.success("Here are your top job recommendations:")
        st.dataframe(results, use_container_width=True)
