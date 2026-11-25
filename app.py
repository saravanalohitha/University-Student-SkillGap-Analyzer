
import streamlit as st
import pandas as pd
import plotly.express as px

from career_management import career_roles
from skill_analyzer import analyze_skills


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="University Student Skill Gap Analyzer",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "students" not in st.session_state:
    st.session_state.students = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_student_id" not in st.session_state:
    st.session_state.analysis_student_id = None

if "analysis_career" not in st.session_state:
    st.session_state.analysis_career = None


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("🎓 University Student Skill Gap Analyzer")

st.subheader(
    "Discover your skills. Identify your gaps. Build your career."
)

st.write(
    "A smart platform to analyze student skills "
    "and identify career opportunities."
)

st.divider()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choose a Page",
    [
        "Home",
        "Student Registration",
        "Registered Students",
        "Skill Gap Analysis",
        "Visual Analytics"
    ]
)


# ==========================================
# HOME DASHBOARD
# ==========================================

if page == "Home":

    st.header("📊 Dashboard Overview")

    total_students = len(st.session_state.students)

    total_careers = len(career_roles)

    if total_students > 0:

        all_matches = []

        for student in st.session_state.students:

            for career in career_roles:

                result = analyze_skills(
                    student["Skills"],
                    career
                )

                all_matches.append(
                    result["match_percentage"]
                )

        average_match = sum(all_matches) / len(all_matches)

    else:
        average_match = 0

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Students",
        total_students
    )

    col2.metric(
        "Career Options",
        total_careers
    )

    col3.metric(
        "Average Career Match",
        f"{average_match:.1f}%"
    )

    st.divider()

    st.subheader("🚀 Welcome to the Analyzer")

    st.write(
        "Register students, analyze their skills, "
        "compare career requirements and discover "
        "which skills they need to improve."
    )

    if total_students == 0:
        st.info(
            "Start by registering your first student."
        )

    else:
        st.success(
            f"{total_students} student profile(s) registered."
        )


# ==========================================
# STUDENT REGISTRATION
# ==========================================

elif page == "Student Registration":

    st.header("📝 Student Registration")

    with st.form("student_registration"):

        name = st.text_input(
            "Student Name",
            value="Lohitha"
        )

        student_id = st.text_input(
            "Student ID",
            value="1234"
        )

        course = st.text_input(
            "Course",
            value="CSE (DSML)"
        )

        skills = st.multiselect(
            "Select Your Skills",
            [
                "Python",
                "SQL",
                "Excel",
                "C",
                "C++",
                "Java",
                "OOP",
                "Data Structures",
                "Statistics",
                "Power BI",
                "HTML",
                "CSS",
                "JavaScript",
                "Git",
                "Machine Learning",
                "Data Visualization"
            ],
            default=["Python", "SQL", "Excel"]
        )

        submitted = st.form_submit_button(
            "Register Student"
        )

        if submitted:

            if (
                not name.strip()
                or not student_id.strip()
                or not course.strip()
            ):

                st.error(
                    "Please enter all required details."
                )

            elif not skills:

                st.warning(
                    "Please select at least one skill."
                )

            elif any(
                s["Student ID"] == student_id.strip()
                for s in st.session_state.students
            ):

                st.error(
                    "Student ID already exists."
                )

            else:

                student = {
                    "Name": name.strip(),
                    "Student ID": student_id.strip(),
                    "Course": course.strip(),
                    "Skills": skills
                }

                st.session_state.students.append(student)

                # Clear previous analysis
                st.session_state.analysis_result = None

                st.success(
                    "Student registered successfully!"
                )

                st.subheader("Student Profile")

                st.json(student)


# ==========================================
# REGISTERED STUDENTS
# ==========================================

elif page == "Registered Students":

    st.header("📋 Registered Students")

    if st.session_state.students:

        st.metric(
            "Total Registered Students",
            len(st.session_state.students)
        )

        df = pd.DataFrame(
            st.session_state.students
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No student records available. "
            "Please register a student first."
        )


# ==========================================
# CAREER SKILL GAP ANALYSIS
# ==========================================

elif page == "Skill Gap Analysis":

    st.header("🎯 Career Skill Gap Analysis")

    if st.session_state.students:

        # Student selection
        student_ids = [
            student["Student ID"]
            for student in st.session_state.students
        ]

        selected_student_id = st.selectbox(
            "Select Student",
            student_ids,
            format_func=lambda sid: next(
                s["Name"] + " (" + sid + ")"
                for s in st.session_state.students
                if s["Student ID"] == sid
            )
        )

        student = next(
            s for s in st.session_state.students
            if s["Student ID"] == selected_student_id
        )

        st.write(
            f"**Student:** {student['Name']}"
        )

        st.write(
            f"**Course:** {student['Course']}"
        )

        st.write(
            "**Current Skills:** "
            + ", ".join(student["Skills"])
        )

        st.divider()

        # Career selection
        selected_career = st.selectbox(
            "Choose Your Desired Career",
            list(career_roles.keys())
        )

        if st.button(
            "Analyze Skills",
            use_container_width=True
        ):

            result = analyze_skills(
                student["Skills"],
                selected_career
            )

            st.session_state.analysis_result = result

            st.session_state.analysis_student_id = (
                selected_student_id
            )

            st.session_state.analysis_career = (
                selected_career
            )

        # Display results only for the current selection
        if (
            st.session_state.analysis_result is not None
            and st.session_state.analysis_student_id == selected_student_id
            and st.session_state.analysis_career == selected_career
        ):

            result = st.session_state.analysis_result

            st.divider()

            st.subheader("📊 Analysis Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Skill Match",
                f"{result['match_percentage']}%"
            )

            col2.metric(
                "Matched Skills",
                len(result["matched_skills"])
            )

            col3.metric(
                "Missing Skills",
                len(result["missing_skills"])
            )

            st.progress(
                result["match_percentage"] / 100
            )

            st.write(
                f"**Selected Career:** {result['selected_career']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.success("✅ Matched Skills")

                if result["matched_skills"]:

                    for skill in result["matched_skills"]:
                        st.write("✔️", skill)

                else:
                    st.write("No matching skills found.")

            with col2:

                st.error("❌ Missing Skills")

                if result["missing_skills"]:

                    for skill in result["missing_skills"]:
                        st.write("❌", skill)

                else:
                    st.write("No missing skills!")

            # Recommendations
            st.divider()

            st.subheader("💡 Skill Improvement Recommendations")

            if result["missing_skills"]:

                st.write(
                    "Focus on learning these skills "
                    "to improve your career readiness:"
                )

                for skill in result["missing_skills"]:
                    st.info(f"Learn {skill}")

            else:

                st.success(
                    "You have all the required skills "
                    "for this selected career!"
                )

    else:

        st.warning(
            "Please register a student first."
        )


# ==========================================
# VISUAL ANALYTICS DASHBOARD
# ==========================================

elif page == "Visual Analytics":

    st.header("📈 Visual Analytics Dashboard")

    if st.session_state.students:

        student_ids = [
            student["Student ID"]
            for student in st.session_state.students
        ]

        selected_id = st.selectbox(
            "Select Student for Analytics",
            student_ids,
            format_func=lambda sid: next(
                s["Name"] + " (" + sid + ")"
                for s in st.session_state.students
                if s["Student ID"] == sid
            ),
            key="analytics_student"
        )

        student = next(
            s for s in st.session_state.students
            if s["Student ID"] == selected_id
        )

        st.subheader(
            f"Analytics for {student['Name']}"
        )

        # Career comparison
        career_data = []

        for career in career_roles:

            result = analyze_skills(
                student["Skills"],
                career
            )

            career_data.append({
                "Career": career,
                "Match Percentage": result["match_percentage"]
            })

        career_df = pd.DataFrame(career_data)

        best_career = career_df.loc[
            career_df["Match Percentage"].idxmax()
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Student Skills",
            len(student["Skills"])
        )

        col2.metric(
            "Career Options",
            len(career_roles)
        )

        col3.metric(
            "Best Career Match",
            f"{best_career['Match Percentage']:.1f}%"
        )

        st.divider()

        # Career comparison chart
        st.subheader("📊 Career-wise Skill Match")

        fig_career = px.bar(
            career_df,
            x="Career",
            y="Match Percentage",
            color="Match Percentage",
            text="Match Percentage",
            title="Skill Match Across All Careers",
            range_y=[0, 100],
            color_continuous_scale="Blues"
        )

        fig_career.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig_career,
            use_container_width=True
        )

        # Select career for detailed analytics
        st.divider()

        st.subheader("🎯 Detailed Skill Analysis")

        analysis_career = st.selectbox(
            "Choose Career for Detailed Analysis",
            list(career_roles.keys()),
            key="visual_career"
        )

        result = analyze_skills(
            student["Skills"],
            analysis_career
        )

        matched_count = len(
            result["matched_skills"]
        )

        missing_count = len(
            result["missing_skills"]
        )

        # Pie chart
        pie_df = pd.DataFrame({
            "Skill Status": [
                "Matched Skills",
                "Missing Skills"
            ],
            "Count": [
                matched_count,
                missing_count
            ]
        })

        fig_pie = px.pie(
            pie_df,
            names="Skill Status",
            values="Count",
            title="Matched vs Missing Skills",
            color="Skill Status",
            color_discrete_map={
                "Matched Skills": "#22C55E",
                "Missing Skills": "#EF4444"
            },
            hole=0.45
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        # Skill comparison bar chart
        skill_df = pd.DataFrame({
            "Skill": (
                result["matched_skills"]
                + result["missing_skills"]
            ),
            "Status": (
                ["Matched"] * matched_count
                + ["Missing"] * missing_count
            )
        })

        fig_skills = px.bar(
            skill_df,
            x="Skill",
            color="Status",
            title="Individual Skill Gap Analysis",
            color_discrete_map={
                "Matched": "#22C55E",
                "Missing": "#EF4444"
            }
        )

        st.plotly_chart(
            fig_skills,
            use_container_width=True
        )

        # Improvement recommendations
        st.divider()

        st.subheader("💡 Recommended Skills to Learn")

        if result["missing_skills"]:

            for index, skill in enumerate(
                result["missing_skills"],
                start=1
            ):

                st.write(
                    f"{index}. **{skill}**"
                )

        else:

            st.success(
                "All required career skills are matched!"
            )

        # Download career analysis
        st.divider()

        st.subheader("📥 Download Analysis Report")

        report_df = pd.DataFrame({
            "Student Name": [student["Name"]] * len(
                result["matched_skills"]
                + result["missing_skills"]
            ),
            "Student ID": [student["Student ID"]] * len(
                result["matched_skills"]
                + result["missing_skills"]
            ),
            "Career": [analysis_career] * len(
                result["matched_skills"]
                + result["missing_skills"]
            ),
            "Skill": (
                result["matched_skills"]
                + result["missing_skills"]
            ),
            "Status": (
                ["Matched"] * matched_count
                + ["Missing"] * missing_count
            )
        })

        csv = report_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name=f"{student['Student ID']}_skill_analysis.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "Please register a student before viewing analytics."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "University Student Skill Gap Analyzer | "
    "Developed using Python and Streamlit"
)
