import streamlit as st
import pandas as pd
import re

# ✅ Load the dataset from CSV (must be in same folder as app.py)
df = pd.read_csv("job_data.csv")

# 🔧 Fill missing values
df['Required Skills'] = df['Required Skills'].fillna('')
df['Category'] = df['Category'].fillna('Other')
df['Company'] = df['Company'].fillna('Unknown')
df['Location'] = df['Location'].fillna('Not Specified')
df['Salary'] = df['Salary'].fillna('Not Mentioned')
df['Job Title'] = df['Job Title'].fillna('Unknown')

# 🔍 Preprocessing function
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# 🎯 Job Recommendation Function with Category Filtering
def recommend_jobs(user_input, selected_category, top_n=5):
    user_input = preprocess(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    # Filter by selected category/domain
    category_df = df[df['Category'].str.lower() == selected_category.lower()]
    
    def match(row_skills):
        row_skills = preprocess(row_skills)
        return any(skill in row_skills for skill in user_skills)
    
    filtered = category_df[category_df['Required Skills'].apply(match)]
    
    if filtered.empty:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Salary"])
    
    return (
        filtered[["Job Title", "Company", "Location", "Salary"]]
        .drop_duplicates()
        .head(top_n)
        .reset_index(drop=True)
    )

# 🚀 Streamlit UI
st.set_page_config(page_title="Job Recommendation Based on Skills", layout="centered")
st.markdown("<h1 style='text-align: center;'>💼 Job Recommendation Based on Skills</h1>", unsafe_allow_html=True)

# 👉 Skills input
user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical design")

# 👉 Category dropdown
categories = sorted(df['Category'].dropna().unique())
category = st.selectbox("🎯 Select your job domain:", categories)

# 🔘 Recommend button
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
