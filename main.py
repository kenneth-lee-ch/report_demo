import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import statsmodels.api as sm

# Set page configuration for a professional look
st.set_page_config(page_title="Purdue Engineering Employment Report", layout="wide")

# Title and introduction
st.title("Purdue Engineering Employment Report")
st.markdown("""
This interactive dashboard presents insights on the employment trends of Purdue Engineering graduates.
The report now includes a larger synthetic dataset that highlights complex patterns, along with a statistical 
causal analysis that examines the relationship between technical skill proficiency and graduate recruitment.
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
job_titles = {
    "Software Engineer": ["Python", "Java", "C++", "SQL", "JavaScript"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Data Visualization"],
    "Aerospace Engineer": ["CAD", "Aerodynamics", "Materials", "Systems Engineering", "Flight Dynamics"],
    "Electrical Engineer": ["Circuit Design", "Embedded Systems", "Signal Processing", "MATLAB", "VHDL"],
    "Mechanical Engineer": ["CAD", "Thermal Systems", "Materials", "Finite Element Analysis", "Dynamics"]
}

skillset_records = []
for job, skills in job_titles.items():
    for skill in skills:
        frequency = np.random.randint(40, 150)
        skillset_records.append({"Job Title": job, "Skill": skill, "Frequency": frequency})
skillset_data = pd.DataFrame(skillset_records)

# 3. Expanded Majors Distribution by Job Title
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

# Companies Bar Chart
st.header("1. Companies Actively Recruiting Purdue Engineering Graduates")
fig_companies = px.bar(companies_data, x="Company", y="Graduates", 
                         title="Number of Purdue Engineering Graduates by Company",
                         labels={"Graduates": "Number of Graduates"},
                         text="Graduates")
fig_companies.update_traces(texttemplate='%{text}', textposition='outside')
st.plotly_chart(fig_companies, use_container_width=True)

# Skillsets by Job Title
st.header("2. Desired Skillsets by Job Title")
fig_skills = px.bar(skillset_data, x="Job Title", y="Frequency", color="Skill", barmode="group",
                    title="Desired Skillsets by Job Title",
                    labels={"Frequency": "Skill Frequency"})
st.plotly_chart(fig_skills, use_container_width=True)

# Majors Distribution (Sunburst Chart)
st.header("3. Majors Hired for Different Job Titles")
fig_majors = px.sunburst(majors_data, path=["Job Title", "Major"], values="Count",
                         title="Distribution of Majors by Job Title")
st.plotly_chart(fig_majors, use_container_width=True)

# Additional Analysis: Skill Frequency Heatmap
st.header("4. Skill Frequency Heatmap")
heatmap_data = skillset_data.pivot(index="Skill", columns="Job Title", values="Frequency").fillna(0)
fig_heatmap = px.imshow(heatmap_data, 
                        title="Heatmap of Skill Frequencies by Job Title",
                        labels=dict(x="Job Title", y="Skill", color="Frequency"),
                        aspect="auto")
st.plotly_chart(fig_heatmap, use_container_width=True)

# -------------------------------
# Statistical Causal Analysis
# -------------------------------
st.header("5. Statistical Analysis: Linking Technical Skill Proficiency to Graduate Recruitment")

st.markdown("""
We simulate a synthetic scenario where an overall **Technical Skill Score** (aggregating high-demand skills)
may influence the number of graduates recruited. In this synthetic dataset, we assume:
- Higher technical skill scores are associated with increased recruitment.
- We model the relationship using a linear regression.
""")

# Create synthetic data for statistical analysis
np.random.seed(42)
n_obs = 50
skill_score = np.random.uniform(20, 100, size=n_obs)  # Simulated overall technical skill score
# Assume a linear relationship: Graduates = 50 + 3 * Skill_Score + noise
graduates_synthetic = 50 + 3 * skill_score + np.random.normal(0, 15, size=n_obs)
causal_data = pd.DataFrame({
    "Skill_Score": skill_score,
    "Graduates": graduates_synthetic
})

# Fit a linear regression model using statsmodels
X = sm.add_constant(causal_data["Skill_Score"])
model = sm.OLS(causal_data["Graduates"], X).fit()

# Display regression summary (first few lines for brevity)
st.subheader("Regression Analysis Summary")
st.text(model.summary().as_text())

# Plot scatter with regression line
fig_reg = px.scatter(causal_data, x="Skill_Score", y="Graduates",
                     title="Regression: Skill Score vs. Graduate Recruitment",
                     labels={"Skill_Score": "Overall Technical Skill Score", "Graduates": "Number of Graduates"})
# Add regression line
reg_line = model.params["const"] + model.params["Skill_Score"] * causal_data["Skill_Score"]
fig_reg.add_traces(px.line(x=causal_data["Skill_Score"], y=reg_line, labels={"y": "Fitted Graduates"}).data)
st.plotly_chart(fig_reg, use_container_width=True)

# -------------------------------
# Data-Driven Recommendations
# -------------------------------
st.header("6. Data-Driven Recommendations")
st.markdown("""
Based on the regression analysis:
- **Coefficient Interpretation**: The estimated coefficient for **Skill Score** is approximately **{coef:.2f}** (p-value: {pval:.3f}). 
  This suggests that for each additional point in the skill score, the number of recruited graduates increases by about **{coef:.2f}** on average.
- **Implication**: Enhancing technical training (e.g., in programming, machine learning, CAD) can potentially drive higher recruitment numbers.
  
**Recommendations for Administration**:
1. **Curriculum Enhancement**: Expand and update technical courses focusing on high-impact skills to boost the overall technical skill score of graduates.
2. **Targeted Training Programs**: Implement workshops and certifications in key areas identified by the regression analysis.
3. **Industry Partnerships**: Foster closer ties with companies that value these skills to provide real-world projects and internship opportunities.
4. **Ongoing Evaluation**: Regularly analyze graduate outcomes with updated data to continuously refine training programs and maintain industry relevance.
""".format(coef=model.params["Skill_Score"], pval=model.pvalues["Skill_Score"]))

# Footer / Data Source
st.markdown("""
---
*Note: All analyses are based on synthetic data for demonstration purposes. For robust causal conclusions, 
detailed individual-level data and advanced causal inference techniques should be employed.*
""")
