import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Load the dataset
df = pd.read_csv("job_data.csv")

# 🔧 Clean missing values
df['Required Skills'] = df['Required Skills'].fillna('')
df['Category'] = df['Category'].fillna('Other')

# 📦 Preprocess function
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# 🎯 Accurate Job Recommender (TF-IDF + Category Filter)
def recommend_jobs(user_input, selected_category, top_n=5):
    # Filter by category first
    category_df = df[df['Category'].str.lower() == selected_category.lower()]
    if category_df.empty:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Salary"])

    # Vectorize
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(category_df['Required Skills'])
    
    user_input_clean = preprocess(user_input)
    user_vec = vectorizer.transform([user_input_clean])

    # Cosine similarity
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Return top matching jobs
    results = category_df.iloc[top_indices][["Job Title", "Company", "Location", "Salary"]]
    return results.reset_index(drop=True)

# 🚀 Streamlit App UI
st.set_page_config(page_title="Job Recommendation Based on Skills", layout="centered")
st.markdown("<h1 style='text-align: center;'>💼 Job Recommendation Based on Skills</h1>", unsafe_allow_html=True)

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical design")
categories = sorted(df['Category'].dropna().unique())
category = st.selectbox("🎯 Select your job domain:", categories)

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input, category)
        if results.empty:
            st.error("❌ No matching jobs found.")
        else:
            st.success("✅ Top 5 Jobs Matching Your Skills:")
            st.dataframe(results, use_container_width=True)
