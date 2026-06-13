import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os
from datetime import datetime

# LOAD MODEL & PREPROCESSOR

model = joblib.load("models/best_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")


def show_prediction():

    st.markdown(
        """
        <div class="page-heading">
            <h1>🎯 Student Dropout Risk Prediction</h1>
            <p class="page-subtitle">
                Enter student data to assess dropout risk, understand the key drivers, and receive tailored support recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    theme = st.session_state.get("theme", "Light")
    if theme == "Dark":
        font_color = "#e6eef8"
        border_color = "#334155"
    else:
        font_color = "#0f172a"
        border_color = "#e2e8f0"

    st.markdown("---")

    main_col, side_col = st.columns([3, 1])

    with side_col:
        st.markdown(
            """
            <div class="info-panel">
                <h4>Why this matters</h4>
                <p>
                    This model combines academic, attendance, lifestyle and support factors to highlight students who may need early intervention.
                </p>
                <ul>
                    <li>Clear risk percentage</li>
                    <li>Actionable recommendations</li>
                    <li>Professional report generation</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="result-card">
                <h4>Prediction tips</h4>
                <p>
                    Use accurate attendance and academic measures for the best prediction quality. Keep support details up to date.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with main_col:
        with st.form("prediction_form"):
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("## 👤 Student Profile")
            student_name = st.text_input("Student Name")
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input("Age", 15, 40, 20)
                gender = st.selectbox("Gender", ["Male", "Female"])
            with col2:
                department = st.selectbox(
                    "Department",
                    ["CS", "Engineering", "Business", "Arts"],
                )
                semester = st.selectbox(
                    "Semester",
                    ["Year 1", "Year 2", "Year 3", "Year 4"],
                )
            with col3:
                parental_education = st.selectbox(
                    "Parental Education",
                    ["High School", "Bachelor", "Master", "PhD"],
                )
                family_income = st.number_input(
                    "Family Income (Rupees)",
                    value=30000,
                    step=1000,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("## 📚 Academic Performance")
            col1, col2, col3 = st.columns(3)
            with col1:
                gpa = st.slider("GPA", 0.0, 4.0, 3.0, 0.1)
            with col2:
                semester_gpa = st.slider("Semester GPA", 0.0, 4.0, 3.0, 0.1)
            with col3:
                cgpa = st.slider("CGPA", 0.0, 4.0, 3.0, 0.1)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("## 🎯 Attendance & Study Habits")
            col1, col2, col3 = st.columns(3)
            with col1:
                attendance_rate = st.slider("Attendance Rate (%)", 0, 100, 75)
            with col2:
                study_hours = st.number_input("Study Hours / Day", value=3.0, step=0.5)
            with col3:
                assignment_delay = st.number_input("Assignment Delay Days", value=2, step=1)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("## 🧠 Lifestyle & Stress")
            col1, col2, col3 = st.columns(3)
            with col1:
                stress_index = st.slider("Stress Index", 0.0, 10.0, 5.0, 0.1)
            with col2:
                travel_time = st.number_input("Travel Time (minutes)", value=20, step=5)
            with col3:
                part_time_job = st.selectbox("Part Time Job", ["Yes", "No"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("## 🎓 Student Support")
            col1, col2 = st.columns(2)
            with col1:
                scholarship = st.selectbox("Scholarship", ["Yes", "No"])
            with col2:
                internet_access = st.selectbox("Internet Access", ["Yes", "No"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            st.markdown("### Quick Student Snapshot")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("GPA", gpa)
            col2.metric("Attendance %", attendance_rate)
            col3.metric("Stress Index", stress_index)
            col4.metric("Study Hours", study_hours)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            predict_clicked = st.form_submit_button("🚀 Analyze Student Risk")

    if predict_clicked:

        #FEATURE ENGINEERING
        student_pressure_index = (stress_index * assignment_delay) / (study_hours + 1)
        academic_risk_score = (100 - attendance_rate) + ((4 - gpa) * 10)
        income_stress_ratio = stress_index / (family_income + 1)
        gpa_consistency_score = abs(gpa - semester_gpa)
        attendance_efficiency = attendance_rate / (travel_time + 1)
        study_efficiency_score = gpa / (study_hours + 1)
        financial_risk_indicator = (1 / (family_income + 1)) * 100000
        academic_momentum = semester_gpa - cgpa
        attendance_risk_index = 100 - attendance_rate
        stress_burden_score = stress_index * (100 - attendance_rate)

        # Create Input DataFrame
        input_df = pd.DataFrame(
            {
                "Age": [age],
                "Gender": [gender],
                "Family_Income": [family_income],
                "Internet_Access": [internet_access],
                "Study_Hours_per_Day": [study_hours],
                "Attendance_Rate": [attendance_rate],
                "Assignment_Delay_Days": [assignment_delay],
                "Travel_Time_Minutes": [travel_time],
                "Part_Time_Job": [part_time_job],
                "Scholarship": [scholarship],
                "Stress_Index": [stress_index],
                "GPA": [gpa],
                "Semester_GPA": [semester_gpa],
                "CGPA": [cgpa],
                "Semester": [semester],
                "Department": [department],
                "Parental_Education": [parental_education],
                "Student_Pressure_Index": [student_pressure_index],
                "Academic_Risk_Score": [academic_risk_score],
                "Income_Stress_Ratio": [income_stress_ratio],
                "GPA_Consistency_Score": [gpa_consistency_score],
                "Attendance_Efficiency": [attendance_efficiency],
                "Study_Efficiency_Score": [study_efficiency_score],
                "Financial_Risk_Indicator": [financial_risk_indicator],
                "Academic_Momentum": [academic_momentum],
                "Attendance_Risk_Index": [attendance_risk_index],
                "Stress_Burden_Score": [stress_burden_score],
            }
        )

        try:

            processed_input = preprocessor.transform(input_df)

            probability = model.predict_proba(processed_input)[0][1]

            risk_percent = round(probability * 100, 2)

            if risk_percent < 30:
                risk_level = "Low"
            elif risk_percent < 70:
                risk_level = "Medium"
            else:
                risk_level = "High"

            # Streamlit Session State
            
            st.session_state["latest_prediction"] = {"Age": age, "Department": department, "GPA": gpa, "Attendance_Rate": attendance_rate, "Stress_Index": stress_index, "Risk_Percent": risk_percent, "Risk_Level": risk_level}

            st.session_state["report_data"] = {
                "Student_Name": student_name,

                "Age": age,
                "Gender": gender,
                "Department": department,
                "Semester": semester,

                "GPA": gpa,
                "CGPA": cgpa,

                "Attendance Rate": attendance_rate,
                "Stress Index": stress_index,

                "Risk Percent": risk_percent,
                "Risk Level": risk_level
            }
            
            # save prediction history

            username = st.session_state.get("user", "guest")
            history_data = pd.DataFrame({"Username": [username], "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Age": [age], "Department": [department], "GPA": [gpa], "Attendance_Rate": [attendance_rate], "Stress_index": [stress_index], "Risk_percent": [risk_percent], "Risk_level": [risk_level]})
            history_file = r"C:\Projects\EduShield_AI\data\predictions\predictions_history.csv"
            if not os.path.exists(history_file):
                history_data.to_csv(history_file, index=False)
            else:
                history_data.to_csv(history_file, mode="a", header=False, index=False)

            # Risk gauge
            
            fig = go.Figure(go.Indicator(mode="gauge+number", value=risk_percent, title={"text": "Student dropout Risk(%)"}, gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.4}, "steps": [{"range": [0, 30], "color": "lightgreen"}, {"range": [30, 70], "color": "gold"}, {"range": [70, 100], "color": "salmon"}]}))
            fig.update_layout(
                margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=font_color),
                title_font=dict(color=font_color),
            )
            try:
                fig['data'][0]['gauge']['threshold'] = {"line": {"color": border_color, "width": 4}, "thickness": 0.75, "value": risk_percent}
            except Exception:
                pass
            left,right = st.columns([2,1])
            with left:
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            with right:
                st.metric(
                    "Risk Score",
                    f"{risk_percent}%"
                )
                st.metric(
                    "Risk Level",
                    risk_level
                )

            if risk_percent < 30:

                st.success("🟢 LOW RISK")

            elif risk_percent < 70:

                st.warning("🟠 MEDIUM RISK")

            else:

                st.error("🔴 HIGH RISK")

            # recommendation
            
            st.markdown("---")
            st.subheader("💡 Recommended Actions")
            if risk_percent < 30:

                recommendation = """
                Continue regular monitoring.
                Encourage extracurricular participation.
                Maintain academic support.
                """
            
                st.success(recommendation)
            
            elif risk_percent < 70:
            
                recommendation = """
                Academic mentoring.
                Weekly attendance tracking.
                Faculty counselling.
                Assignment monitoring.
                """

                st.warning(recommendation)
            
            else:
            
                recommendation = """
                Immediate intervention required.
                Parent communication.
                Mental health counselling.
                Academic support program.
                Weekly performance review.
                """
            
                st.error(recommendation)
                
            st.session_state["report_data"]["Recommendations"] = recommendation
            st.session_state["report_data"]["SHAP Summary"] = \
                "reports/figures/shap_summary.png"

            st.session_state["report_data"]["SHAP Waterfall"] = \
                "reports/figures/shap_waterfall.png"
        except Exception as e:

            st.error(f"Prediction Error: {e}")

