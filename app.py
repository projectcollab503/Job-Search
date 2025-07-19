import streamlit as st
import pandas as pd
import re

# ✅ Dataset with 50 job entries (5 per job type)
data = {
    "Job Title": [
        "Data Analyst", "Data Analyst", "Data Analyst", "Data Analyst", "Data Analyst",
        "Software Developer", "Software Developer", "Software Developer", "Software Developer", "Software Developer",
        "Machine Learning Engineer", "Machine Learning Engineer", "Machine Learning Engineer", "Machine Learning Engineer", "Machine Learning Engineer",
        "Frontend Developer", "Frontend Developer", "Frontend Developer", "Frontend Developer", "Frontend Developer",
        "Backend Developer", "Backend Developer", "Backend Developer", "Backend Developer", "Backend Developer",
        "Mechanical Engineer", "Mechanical Engineer", "Mechanical Engineer", "Mechanical Engineer", "Mechanical Engineer",
        "Accountant", "Accountant", "Accountant", "Accountant", "Accountant",
        "Pharmacist", "Pharmacist", "Pharmacist", "Pharmacist", "Pharmacist",
        "UI/UX Designer", "UI/UX Designer", "UI/UX Designer", "UI/UX Designer", "UI/UX Designer",
        "Marketing Analyst", "Marketing Analyst", "Marketing Analyst", "Marketing Analyst", "Marketing Analyst"
    ],
    "Company": [
        "Accenture", "Capgemini", "Zoho", "Infosys", "TCS",
        "Cognizant", "Cognizant", "Deloitte", "HCL", "Cognizant",
        "Wipro", "HCL", "Zoho", "Deloitte", "Capgemini",
        "Google", "Wipro", "Cognizant", "Deloitte", "Infosys",
        "AWS", "Google", "Capgemini", "Accenture", "Wipro",
        "L&T", "Siemens", "Tata Motors", "Gammon India", "Infosys",
        "PwC", "EY", "Deloitte", "Accenture", "Capgemini",
        "Apollo Hospitals", "Fortis", "Max Healthcare", "CloudNine", "AIIMS",
        "Byju's", "Amazon", "Flipkart", "Swiggy", "Zoho",
        "Google", "Amazon", "Flipkart", "Byju's", "TCS"
    ],
    "Location": [
        "Ahmedabad", "Bangalore", "Hyderabad", "Hyderabad", "Bangalore",
        "Chennai", "Ahmedabad", "Ahmedabad", "Bangalore", "Gurgaon",
        "Noida", "Chennai", "Mumbai", "Bangalore", "Gurgaon",
        "Delhi", "Hyderabad", "Pune", "Mumbai", "Noida",
        "Pune", "Kolkata", "Bangalore", "Noida", "Mumbai",
        "Mumbai", "Delhi", "Ahmedabad", "Kolkata", "Hyderabad",
        "Kolkata", "Bhopal", "Hyderabad", "Delhi", "Chennai",
        "Bangalore", "Delhi", "Lucknow", "Chennai", "Hyderabad",
        "Remote", "Gurgaon", "Hyderabad", "Remote", "Pune",
        "Chennai", "Mumbai", "Bangalore", "Delhi", "Noida"
    ],
    "Salary": [
        "₹9,00,000", "₹12,00,000", "₹8,00,000", "₹10,00,000", "₹8,00,000",
        "₹4,50,000", "₹8,00,000", "₹10,00,000", "₹5,00,000", "₹5,00,000",
        "₹12,00,000", "₹10,00,000", "₹9,00,000", "₹11,00,000", "₹8,00,000",
        "₹7,00,000", "₹6,50,000", "₹8,50,000", "₹6,80,000", "₹7,50,000",
        "₹9,00,000", "₹10,00,000", "₹7,50,000", "₹8,20,000", "₹7,80,000",
        "₹7,50,000", "₹6,80,000", "₹6,50,000", "₹5,90,000", "₹7,00,000",
        "₹6,00,000", "₹6,50,000", "₹5,80,000", "₹6,00,000", "₹7,50,000",
        "₹4,80,000", "₹3,60,000", "₹8,00,000", "₹4,50,000", "₹3,80,000",
        "₹5,50,000", "₹6,20,000", "₹5,00,000", "₹6,50,000", "₹5,90,000",
        "₹6,20,000", "₹6,80,000", "₹7,20,000", "₹6,00,000", "₹7,00,000"
    ],
    "Required Skills": [
        "python, sql, data analysis, excel, statistics, reporting, dashboards"
    ] * 5 + [
        "java, python, algorithms, software development, object oriented programming"
    ] * 5 + [
        "machine learning, deep learning, python, numpy, pandas, data science"
    ] * 5 + [
        "html, css, javascript, react, frontend, web development, ui design"
    ] * 5 + [
        "node.js, backend, api, databases, server, express.js, restful apis"
    ] * 5 + [
        "autocad, solidworks, mechanical design, manufacturing, machine drawing"
    ] * 5 + [
        "accounting, tally, excel, gst, financial reporting, bookkeeping, invoices"
    ] * 5 + [
        "pharmacy, pharmaceutical, prescriptions, drugs, medicine dispensing"
    ] * 5 + [
        "figma, wireframe, user experience, interface design, prototyping"
    ] * 5 + [
        "market research, excel, data visualization, strategy, surveys"
    ] * 5
}

df = pd.DataFrame(data)

# Text clean
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# Recommender function
def recommend_jobs(user_input, top_n=5):
    user_input = preprocess(user_input)
    user_skills = [skill.strip() for skill in user_input.split(",") if skill.strip()]
    
    def match(row_skills):
        row_skills = preprocess(row_skills)
        return any(skill in row_skills for skill in user_skills)
    
    filtered = df[df['Required Skills'].apply(match)]
    
    if filtered.empty:
        return pd.DataFrame(columns=["Job Title", "Company", "Location", "Salary"])
    
    return filtered[["Job Title", "Company", "Location", "Salary"]].drop_duplicates().head(top_n).reset_index(drop=True)

# Streamlit UI
st.set_page_config(page_title="Job Recommendation Based on Skills", layout="centered")
st.title("💼 Job Recommendation Based on Skills")

user_input = st.text_input("🔍 Enter your skills (comma-separated):", placeholder="e.g. python, accounting, mechanical design")

if st.button("Get Recommendations"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter at least one skill.")
    else:
        results = recommend_jobs(user_input)
        if results.empty:
            st.error("❌ No matching jobs found.")
        else:
            st.success("✅ Top 5 Jobs Matching Your Skills:")
            st.dataframe(results, use_container_width=True)
