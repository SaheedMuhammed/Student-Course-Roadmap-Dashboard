import pandas as pd
import plotly.express as px
import streamlit as st
import random

#  Page Config
st.set_page_config(page_title="Student Course Roadmap", page_icon="🎓", layout="wide")

#  Theme Toggle
theme = st.sidebar.radio(" Choose Theme", ["Light", "Dark"])

#  Dynamic CSS Styling
if theme == "Light":
    bg_color = "#F9FAFB"
    sidebar_bg = "linear-gradient(180deg, #4F46E5 0%, #6366F1 100%)"
    text_color = "#111827"
else:
    bg_color = "#1E1E2E"
    sidebar_bg = "linear-gradient(180deg, #0F172A 0%, #1E293B 100%)"
    text_color = "#E5E7EB"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}
[data-testid="stSidebar"] {{
    background: {sidebar_bg};
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{
    color: white !important;
}}
.big-title {{
    font-size: 32px !important;
    color: #4F46E5;
    font-weight: 700;
}}
.sub-text {{
    font-size: 18px !important;
    color: #6B7280;
}}
</style>
""", unsafe_allow_html=True)

#  Title
st.markdown("<p class='big-title'>🎓 Student Course Roadmap Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Analyze your learning progress, explore tools, and track your roadmap 🚀</p>", unsafe_allow_html=True)
st.markdown("---")

#  Load Data
try:
    df = pd.read_csv("all_courses_roadmap.csv")
    st.success(" Data loaded successfully!")
except FileNotFoundError:
    st.error(" 'all_courses_roadmap.csv' not found. Please add it to this folder.")
    st.stop()

#  Sidebar Filters
st.sidebar.header(" Filter Options")
courses = df['Course'].unique()
selected_course = st.sidebar.selectbox("Select Course:", courses)

filtered_df = df[df['Course'] == selected_course]
levels = filtered_df['Level'].unique()
selected_level = st.sidebar.multiselect("Filter by Level:", levels, default=levels)
filtered_df = filtered_df[filtered_df['Level'].isin(selected_level)]

#  Course Overview
st.subheader(f"📘 Roadmap Overview for {selected_course}")
st.dataframe(filtered_df, use_container_width=True)


#  Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Average Duration per Course")
    avg_duration = df.groupby('Course')['Duration_Weeks'].mean().reset_index()
    fig1 = px.bar(avg_duration, x='Course', y='Duration_Weeks', color='Duration_Weeks',
                  text_auto=True, color_continuous_scale='Purples')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🧠 Top Tools Used Across Courses")
    tools = df['Tools'].astype(str).str.split(',').explode().str.strip().value_counts().reset_index()
    tools.columns = ['Tool', 'Count']
    fig2 = px.bar(tools.head(10), x='Tool', y='Count', color='Count',
                  title='Top 10 Tools', color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

#  Skill Analysis
st.subheader("🔍 Skill Frequency in Selected Course")
skills = filtered_df['Skill'].astype(str).str.split(',').explode().str.strip().value_counts().reset_index()
skills.columns = ['Skill', 'Count']
fig3 = px.pie(skills, names='Skill', values='Count', title=f"Skill Breakdown for {selected_course}",
              color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig3, use_container_width=True)

#  Download Option
st.markdown("### 📥 Download Filtered Data")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Course Roadmap as CSV", data=csv_data,
                   file_name=f"{selected_course}_roadmap.csv", mime='text/csv')

#  Motivation of the Day
st.markdown("---")
st.markdown("###  Motivation of the Day")
quotes = [
    "“The expert in anything was once a beginner.” – Helen Hayes",
    "“Learn continually — there’s always one more thing to learn.” – Steve Jobs",
    "“Push yourself, because no one else is going to do it for you.”",
    "“Data is the new oil.” – Clive Humby",
    "“Small steps lead to big success.”"
]
st.success(random.choice(quotes))

#  Footer
st.markdown("---")
st.caption("Built with  by *Saheed Muhammed* — Empowering students to learn smarter ")
