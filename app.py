import streamlit as st
import pandas as pd
import re

# 📦 Manually added job info for realistic matching
data = {
    "Job Title": [
        "Data Analyst",
        "Software Developer",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Mechanical Engineer",
        "Civil Engineer",
        "Accountant",
        "Tax Consultant",
        "Pharmacist",
        "Medical Lab Technician"
    ],
    "Company": [
        "Infosys",
        "TCS",
        "Google",
        "Zoho",
        "L&T",
        "Gammon India",
        "Deloitte",
        "PwC",
        "Apollo Hospitals",
        "Fortis Healthcare"
    ],
    "Location": [
        "Bangalore",
        "Hyderabad",
        "Pune",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Kolkata",
        "Ahmedabad",
        "Chennai",
        "Bangalore"
    ],
    "Salary": [
        "₹6,50,000",
        "₹8,00,000",
        "₹12,00,000",
        "₹7,00,000",
        "₹7,50,000",
        "₹6,80,000",
        "₹5,50,000",
        "₹6,20,000",
        "₹4,80,000",
        "₹3,60,000"
    ],
    "Required Skills": [
        "python, sql, data analysis, excel, statistics",
        "java, python, algorithms, software development",
        "machine learning, deep learning, python, numpy, pandas",
        "html, css, javascript, react, frontend",
        "autocad, solidworks, mechanical design, manufacturing",
        "construction, civil engineering, site management, autocad",
        "accounting, tally, excel, gst, financial reporting",
        "income tax, gst, audit, finance, accounting",
        "pharmacy, pharmaceutical, prescriptions, drugs",
        "lab testing, pathology, sample collection, reports"
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# 🔧 Text cleaning
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# 💡 Job matching function
def recommend_jobs(user_input, top_n=5):
    user_input = preprocess(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    def match(row_skills):
        job_skills = preprocess(row_skills).split(",")
        return any(skill in job_skills for skill in user_skills)
    
    filtered = df[df['Required Skills'].apply(match)]
    
    if filtered.empty:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Salary"])
    
    return filtered[["Job Title", "Company", "Location", "Salary"]].drop_duplicates().head(top_n).reset_index(drop=True)

# 🖥️ Streamlit UI
st.set_page_config(page_title="AI Job Recommender", layout="centered")
st.title("💼 AI Job Recommender Based on Your Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical design")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        if results.empty:
            st.error("❌ No matching jobs found.")
        else:
            st.success("✅ Here are your top 5 matching jobs:")
            st.dataframe(results, use_container_width=True)
