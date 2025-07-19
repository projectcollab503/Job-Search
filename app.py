import streamlit as st
import pandas as pd
import re

# 📦 Manually added job info for accurate matching
data = {
    "Job Title": [
        "Data Analyst",
        "Mechanical Engineer",
        "Accountant",
        "Software Developer",
        "Pharmacist"
    ],
    "Company": [
        "Infosys",
        "L&T",
        "Deloitte",
        "TCS",
        "Apollo Hospitals"
    ],
    "Location": [
        "Bangalore",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Chennai"
    ],
    "Salary": [
        "₹6,00,000",
        "₹7,50,000",
        "₹5,00,000",
        "₹8,00,000",
        "₹4,80,000"
    ],
    "Required Skills": [
        "python, sql, data analysis, excel",
        "autocad, mechanical design, solidworks, manufacturing",
        "accounting, tally, gst, excel",
        "java, python, algorithms, software engineering",
        "pharmacy, pharmaceutical, medicine, prescriptions"
    ]
}

# Create a small job dataset
df = pd.DataFrame(data)

# Clean text function
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# Match jobs based on user input
def recommend_jobs(user_input, top_n=5):
    user_input = preprocess(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    def match(row_skills):
        job_skills = preprocess(row_skills).split(",")
        return any(skill in job_skills for skill in user_skills)
    
    filtered = df[df['Required Skills'].apply(match)]

    if filtered.empty:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Salary"])
    
    return filtered[["Job Title", "Company", "Location", "Salary"]].head(top_n).reset_index(drop=True)

# Streamlit UI
st.set_page_config(page_title="Job Recommender", layout="centered")
st.title("💼 Job Recommender Based on Your Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        if results.empty:
            st.error("❌ No matching jobs found.")
        else:
            st.success("✅ Top 5 Matching Jobs:")
            st.dataframe(results, use_container_width=True)
