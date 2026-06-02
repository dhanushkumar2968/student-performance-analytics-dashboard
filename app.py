import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r"C:\Users\dhanu\Downloads\student_data_50000.csv")

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)
st.title("🎓 Student Performance Analytics Dashboard")
st.caption("Interactive dashboard for analyzing student performance, attendance, GPA, and departmental trends.")

st.sidebar.header("🎛️ Filters")
department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

academic_year = st.sidebar.multiselect(
    "Academic Year",
    options=df["Academic_Year"].unique(),
    default=df["Academic_Year"].unique()
)

semester = st.sidebar.multiselect(
    "Semester",
    options=df["Semester"].unique(),
    default=df["Semester"].unique()
)

df_selection = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["Academic_Year"].isin(academic_year)) &
    (df["Semester"].isin(semester))
]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "👨‍🎓 Total Students",
        f"{len(df_selection):,}"
   )
with col2:
    st.metric(
        "📊 Average GPA",
        round(df_selection["GPA"].mean(), 2)
    )
with col3:
    st.metric(
        "📅 Avg Attendance",
        f"{df_selection['Attendance'].mean():.1f}%"
    )
with col4:
    st.metric(
        "🏫 Departments",
        df_selection["Department"].nunique()
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "🏆 Highest GPA",
        round(df_selection["GPA"].max(), 2)
    )
with col2:
    st.metric(
        "📝 Avg Final Marks",
        round(df_selection["Final_Marks"].mean(), 1)
    )
with col3:
    pass_rate = (
        (df_selection["GPA"] >= 2.5).mean()
    ) * 100
    st.metric(
        "✅ Pass Rate",
        f"{pass_rate:.1f}%"
    )
with col4:
    st.metric(
        "📚 Academic Years",
        df_selection["Academic_Year"].nunique()
    )
excellent = len(df_selection[df_selection["GPA"] >= 3.5])
good = len(
    df_selection[
        (df_selection["GPA"] >= 3.0) &
        (df_selection["GPA"] < 3.5)
    ]
)
average = len(
    df_selection[
        (df_selection["GPA"] >= 2.5) &
        (df_selection["GPA"] < 3.0)
    ]
)
poor = len(df_selection[df_selection["GPA"] < 2.5])
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌟 Excellent", excellent)
col2.metric("👍 Good", good)
col3.metric("📘 Average", average)
col4.metric("⚠️ Needs Improvement", poor)
    
#st.dataframe(df_selection)

col1, col2, col3 ,col4 = st.columns(4)

with col1:
    st.subheader("📊 GPA Distribution")
    fig, ax = plt.subplots()
    ax.hist(df_selection["GPA"], bins=20)
    ax.set_title("GPA Distribution")
    st.pyplot(fig)
with col2:
    st.subheader("📅 Attendance Distribution")
    fig, ax = plt.subplots()
    ax.hist(df_selection["Attendance"], bins=20)
    ax.set_title("Attendance Distribution")
    st.pyplot(fig)
with col3:
    st.subheader("📊 Department-wise GPA")
    dept_gpa = (
    df_selection.groupby("Department")["GPA"]
    .mean()
    .sort_values(ascending=False))
    fig, ax = plt.subplots(figsize=(8,4))
    dept_gpa.plot(
    kind="bar",
    ax=ax
    )
    ax.set_title("Average GPA by Department")
    ax.set_ylabel("Average GPA")
    st.pyplot(fig)
with col4:
    st.subheader("📊 Gender Analysis")
    gender_gpa = (
    df_selection.groupby("Gender")["GPA"]
    .mean())
    fig, ax = plt.subplots()
    gender_gpa.plot(
    kind="bar",
    ax=ax
    )
    ax.set_title("Average GPA by Gender")
    ax.set_ylabel("Average GPA")
    st.pyplot(fig)

st.subheader("🏆 Top 10 Students")
top_students = (
    df_selection
    .sort_values("GPA", ascending=False)
    .head(10)
)

st.dataframe(
    top_students[
        [
            "Student_ID",
            "Department",
            "Gender",
            "GPA",
            "Attendance",
            "Final_Marks"
        ]
    ],
    use_container_width=True
)

st.subheader("🏫 Department Summary")

department_summary = (
    df_selection
    .groupby("Department")
    .agg(
        Total_Students=("Student_ID", "count"),
        Avg_GPA=("GPA", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Avg_Final_Marks=("Final_Marks", "mean")
    )
    .round(2)
)

st.dataframe(
    department_summary,
    use_container_width=True
)

st.subheader("🔍 Filtered Dataset")

st.dataframe(
    df_selection,
    use_container_width=True,
    height=400
)

csv = df_selection.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

