import streamlit as st
import pandas as pd
import re

# ✅ Extended job dataset with 30+ diverse job entries
data = {
    "Job Title": [
        "Data Analyst", "Software Developer", "Machine Learning Engineer", "Frontend Developer",
        "Backend Developer", "Database Administrator", "DevOps Engineer", "Cloud Engineer",
        "Cybersecurity Analyst", "IT Support Engineer",

        "Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Automobile Engineer", "Site Engineer",

        "Accountant", "Tax Consultant", "Auditor", "Financial Analyst", "Investment Banker",

        "Pharmacist", "Medical Lab Technician", "Radiologist", "Physiotherapist", "Nursing Assistant",

        "Graphic Designer", "UI/UX Designer", "HR Executive", "Marketing Analyst", "Digital Marketer"
    ],
    "Company": [
        "Infosys", "TCS", "Google", "Zoho", "Wipro", "HCL", "Capgemini", "AWS", "Cisco", "Dell",
        "L&T", "Gammon India", "Siemens", "Tata Motors", "Shapoorji Pallonji",
        "Deloitte", "PwC", "EY", "ICICI Bank", "Morgan Stanley",
        "Apollo Hospitals", "Fortis", "Max Healthcare", "CloudNine", "AIIMS",
        "Byju's", "Swiggy", "Reliance Retail", "Amazon", "Flipkart"
    ],
    "Location": [
        "Bangalore", "Hyderabad", "Pune", "Chennai", "Noida", "Gurgaon", "Mumbai", "Remote", "Delhi", "Kochi",
        "Mumbai", "Delhi", "Nagpur", "Ahmedabad", "Kolkata",
        "Kolkata", "Jaipur", "Indore", "Bhopal", "Gurgaon",
        "Chennai", "Bangalore", "Delhi", "Lucknow", "Hyderabad",
        "Remote", "Hyderabad", "Mumbai", "Gurgaon", "Bangalore"
    ],
    "Salary": [
        "₹6,50,000", "₹8,00,000", "₹12,00,000", "₹7,00,000", "₹7,80,000", "₹6,90,000", "₹8,20,000", "₹9,50,000", "₹7,50,000", "₹5,20,000",
        "₹7,50,000", "₹6,80,000", "₹6,70,000", "₹6,50,000", "₹5,90,000",
        "₹5,50,000", "₹6,20,000", "₹6,00,000", "₹8,50,000", "₹12,50,000",
        "₹4,80,000", "₹3,60,000", "₹8,00,000", "₹4,50,000", "₹3,80,000",
        "₹5,00,000", "₹6,50,000", "₹5,80,000", "₹7,20,000", "₹6,00,000"
    ],
    "Required Skills": [
        "python, sql, data analysis, excel, statistics",
        "java, python, algorithms, software development",
        "machine learning, deep learning, python, numpy, pandas",
        "html, css, javascript, react, frontend",
        "node.js, backend, api, databases, server",
        "sql, oracle, database tuning, administration",
        "docker, jenkins, kubernetes, linux, deployment",
        "cloud computing, aws, azure, virtual machines",
        "network security, firewalls, risk assessment",
        "technical support, troubleshooting, it helpdesk",

        "autocad, solidworks, mechanical design, manufacturing",
        "construction, civil engineering, site management, autocad",
        "circuits, wiring, power systems, electrical maintenance",
        "vehicle design, engine systems, CAD, automobile",
        "construction site, project execution, estimation",

        "accounting, tally, excel, gst, financial reporting",
        "income tax, gst, audit, finance, accounting",
        "internal audit, compliance, ms excel, analysis",
        "financial modeling, ms excel, budgeting, reporting",
        "investment banking, equity research, valuation",

        "pharmacy, pharmaceutical, prescriptions, drugs",
        "lab testing, pathology, sample collection, reports",
        "radiology, imaging, medical scans, diagnostics",
        "rehabilitation, exercises, physical therapy",
        "patient care, nursing, assistance, hygiene",

        "photoshop, illustrator, visual design, creativity",
        "figma, wireframe, user experience, interface design",
        "recruitment, onboarding, HRMS, employee engagement",
        "market research, excel, data visualization, strategy",
        "seo, google ads, content writing, campaigns"
    ]
}

# ✅ Load data into DataFrame
df = pd.DataFrame(data)

# 🔧 Text cleaning
def preprocess(text):
    return re.sub(r'[^a-zA-Z0-9, ]', '', text.lower())

# 💡 Skill-based recommender
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
            st.success("✅ Top 5 Jobs Matching Your Skills:")
            st.dataframe(results, use_container_width=True)
