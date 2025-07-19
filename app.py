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
    return df

df = load_data()

# Clean skill text
def preprocess_text(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

df['Cleaned Skills'] = df['Required Skills'].apply(preprocess_text)

# Recommendation function
def recommend_jobs(user_input, top_n=5):
    user_input = preprocess_text(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    # Filter rows where at least one skill matches
    mask = df['Cleaned Skills'].apply(lambda x: any(skill in x for skill in user_skills))
    filtered_df = df[mask].copy()

    # If no match found
    if filtered_df.empty:
        return pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Salary'])

    # TF-IDF on filtered jobs only
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered_df['Cleaned Skills'])
    user_vector = vectorizer.transform([' '.join(user_skills)])

    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    return filtered_df.iloc[top_indices][['Job Title', 'Company', 'Location', 'Salary']].reset_index(drop=True)

# Streamlit app
st.set_page_config(page_title="Job Recommender", layout="centered")
st.title("💼 Job Recommender Based on Your Skills")
user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, sql, accounting, mechanical engineering")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        if results.empty:
            st.error("❌ No matching jobs found for your skills.")
        else:
            st.success("Here are your top job recommendations:")
            st.dataframe(results, use_container_width=True)
