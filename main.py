import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration for a professional look
st.set_page_config(page_title="Purdue Engineering Employment Report", layout="wide")

# Title and introduction
st.title("Purdue Engineering Employment Report")
st.markdown("""
This interactive dashboard presents insights on the employment trends of Purdue Engineering graduates.
The report now includes a larger synthetic dataset that highlights complex patterns including:
- **Notable Employers**: Expanded list of companies and the number of Purdue graduates employed.
- **Desired Skillsets**: Detailed view of skill frequencies across multiple job titles.
- **Major Distribution**: Breakdown of engineering majors hired for various job roles.
""")

# -------------------------------
# Synthetic Data Generation
# -------------------------------

# 1. Expanded Companies Dataset
companies = ["Google", "Microsoft", "Boeing", "General Electric", "Apple", "Lockheed Martin", 
             "Northrop Grumman", "Amazon", "IBM", "Intel"]
np.random.seed(42)
graduates = np.random.randint(50, 200, size=len(companies))
companies_data = pd.DataFrame({
    "Company": companies,
    "Graduates": graduates
})

# 2. Expanded Skillsets by Job Title
# Define job titles and associated skills
job_titles = {
    "Software Engineer": ["Python", "Java", "C++", "SQL", "JavaScript"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Data Visualization"],
    "Aerospace Engineer": ["CAD", "Aerodynamics", "Materials", "Systems Engineering", "Flight Dynamics"],
    "Electrical Engineer": ["Circuit Design", "Embedded Systems", "Signal Processing", "MATLAB", "VHDL"],
    "Mechanical Engineer": ["CAD", "Thermal Systems", "Materials", "Finite Element Analysis", "Dynamics"]
}

# Generate synthetic frequencies for each skill per job title
skillset_records = []
for job, skills in job_titles.items():
    for skill in skills:
        # Random frequency between 40 and 150, with slight variation by job title
        frequency = np.random.randint(40, 150)
        skillset_records.append({"Job Title": job, "Skill": skill, "Frequency": frequency})
skillset_data = pd.DataFrame(skillset_records)

# 3. Expanded Majors Distribution by Job Title
# Assume each job title hires from several related majors with random counts
majors_options = {
    "Software Engineer": ["Computer Engineering", "Software Engineering", "Electrical Engineering"],
    "Data Scientist": ["Computer Engineering", "Electrical Engineering", "Mathematics", "Statistics"],
    "Aerospace Engineer": ["Aerospace Engineering", "Mechanical Engineering", "Materials Science"],
    "Electrical Engineer": ["Electrical Engineering", "Computer Engineering", "Physics"],
    "Mechanical Engineer": ["Mechanical Engineering", "Aerospace Engineering", "Industrial Engineering"]
}

majors_records = []
for job, majors in majors_options.items():
    for major in majors:
        count = np.random.randint(20, 100)
        majors_records.append({"Job Title": job, "Major": major, "Count": count})
majors_data = pd.DataFrame(majors_records)

# -------------------------------
# Visualizations
# -------------------------------

# Visualization: Companies Bar Chart
st.header("1. Companies Actively Recruiting Purdue Engineering Graduates")
fig_companies = px.bar(companies_data, x="Company", y="Graduates", 
                         title="Number of Purdue Engineering Graduates by Company",
                         labels={"Graduates": "Number of Graduates"},
                         text="Graduates")
fig_companies.update_traces(texttemplate='%{text}', textposition='outside')
st.plotly_chart(fig_companies, use_container_width=True)

# Visualization: Skillsets by Job Title
st.header("2. Desired Skillsets by Job Title")
fig_skills = px.bar(skillset_data, x="Job Title", y="Frequency", color="Skill", barmode="group",
                    title="Desired Skillsets by Job Title",
                    labels={"Frequency": "Skill Frequency"})
st.plotly_chart(fig_skills, use_container_width=True)

# Visualization: Majors Distribution (Sunburst Chart)
st.header("3. Majors Hired for Different Job Titles")
fig_majors = px.sunburst(majors_data, path=["Job Title", "Major"], values="Count",
                         title="Distribution of Majors by Job Title")
st.plotly_chart(fig_majors, use_container_width=True)

# Additional Analysis: Skill Frequency Heatmap
st.header("4. Skill Frequency Heatmap")
# Pivot the data for a heatmap
heatmap_data = skillset_data.pivot(index="Skill", columns="Job Title", values="Frequency").fillna(0)
fig_heatmap = px.imshow(heatmap_data, 
                        title="Heatmap of Skill Frequencies by Job Title",
                        labels=dict(x="Job Title", y="Skill", color="Frequency"),
                        aspect="auto")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer / Data Source
st.markdown("""
---
*Note: This report uses synthetic data for demonstration purposes. In a production environment, replace the datasets with actual data from Purdue's career reports or internal surveys.*
""")
