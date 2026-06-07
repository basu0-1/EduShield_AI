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
    from src.utils.pdf_generator import generate_simple_pdf, generate_professional_pdf
    import os

    st.header("🎯 Student Dropout Risk Prediction")

    st.markdown("---")

    # USER INPUTS
    
    #Row 1 — Student Profile
    st.markdown("## 👤 Student Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age",15,40,20)
        gender = st.selectbox("Gender",["Male","Female"])    
    with col2:
        department = st.selectbox(
            "Department",
            ["CS","Engineering","Business","Arts"]
        )
        semester = st.selectbox(
            "Semester",
            ["Year 1","Year 2","Year 3","Year 4"]
        )
    with col3:
        parental_education = st.selectbox(
            "Parental Education",
            ["High School","Bachelor","Master","PhD"]
        )
        family_income = st.number_input(
            "Family Income",
            value=30000
        )
    #Row 2 — Academic Performance   
    st.markdown("## 📚 Academic Performance")
    col1,col2,col3 = st.columns(3)
    with col1:
        gpa = st.slider("GPA",0.0,4.0,3.0)
    with col2:
        semester_gpa = st.slider(
            "Semester GPA",
            0.0,4.0,3.0
        )
    with col3:
        cgpa = st.slider(
            "CGPA",
            0.0,4.0,3.0
        )
    #Row 3 — Attendance & Study
    st.markdown("## 🎯 Attendance & Study Habits")
    col1,col2,col3 = st.columns(3)    
    with col1:
        attendance_rate = st.slider(
            "Attendance Rate",
            0,100,75
        )    
    with col2:
        study_hours = st.number_input(
            "Study Hours/Day",
            value=3.0
        )    
    with col3:
        assignment_delay = st.number_input(
            "Assignment Delay Days",
            value=2
        )
    #Row 4 — Lifestyle & Stress
    st.markdown("## 🧠 Lifestyle & Stress")
    col1,col2,col3 = st.columns(3)    
    with col1:
        stress_index = st.slider(
            "Stress Index",
            0.0,10.0,5.0
        )    
    with col2:
        travel_time = st.number_input(
            "Travel Time",
            value=20
        )    
    with col3:
        part_time_job = st.selectbox(
            "Part Time Job",
            ["Yes","No"]
        )    
    #Row 5 — Support Factors
    st.markdown("## 🎓 Student Support")
    col1,col2,col3 = st.columns(3)
    with col1:
        scholarship = st.selectbox(
            "Scholarship",
            ["Yes","No"]
        )
    with col2:
        internet_access = st.selectbox(
            "Internet Access",
            ["Yes","No"]
        )
    
    
    #Summary Cards
    st.markdown("### Quick Student Snapshot")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric("GPA", gpa)
    with col2:
        st.metric(
            "Attendance %",
            attendance_rate
        )
    with col3:
        st.metric(
            "Stress Index",
            stress_index
        )
    with col4:
        st.metric(
            "Study Hours",
            study_hours
        )
    
    # PREDICTION BUTTON
    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button(
        "🚀 Analyze Student Risk",
        use_container_width=True
    )
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

            st.session_state["report_data"] = {"Age": age, "Department": department, "GPA": gpa, "Attendance Rate": attendance_rate, "Stress Index": stress_index, "Risk(%)": risk_percent}
            st.session_state["prediction_done"] = True
            
            # save prediction history

            username = st.session_state.get("user", "guest")
            history_data = pd.DataFrame({"Username": [username], "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Age": [age], "Department": [department], "GPA": [gpa], "Attendance_Rate": [attendance_rate], "Stress_index": [stress_index], "Risk_percent": [risk_percent], "Risk_level": [risk_level]})
            history_file = "C:\Projects\EduShield_AI\data\predictions\predictions_history.csv"
            if not os.path.exists(history_file):
                history_data.to_csv(history_file, index=False)
            else:
                history_data.to_csv(history_file, mode="a", header=False, index=False)

            # Risk gauge
            
            fig = go.Figure(go.Indicator(mode="gauge+number", value=risk_percent, title={"text": "Student dropout Risk(%)"}, gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.4}, "steps": [{"range": [0, 30], "color": "lightgreen"}, {"range": [30, 70], "color": "gold"}, {"range": [70, 100], "color": "salmon"}]}))
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
                st.success(
                    """
                    ✓ Student performing well
                    ✓ Continue regular monitoring
                    ✓ Encourage participation in activities
                    """
                )
            elif risk_percent < 70:
                st.warning(
                    """
                    ✓ Academic mentoring
                    ✓ Monitor attendance weekly
                    ✓ Faculty counselling
                    ✓ Track assignment submissions
                    """
                )
            else:
                st.error(
                    """
                    ✓ Immediate intervention required
                    ✓ Parent communication
                    ✓ Academic support program
                    ✓ Mental health counselling
                    ✓ Weekly progress monitoring
                    """
                )
            # ====================================
            # PDF REPORT SECTION
            # ====================================
            
            if st.session_state.get("prediction_done", False):
            
                st.markdown("---")
                st.subheader("📄 PDF Report Generator")
            
                if st.button("Generate PDF Reports"):
                    st.success("Button Clicked")
                    
                    report_data = st.session_state["report_data"]
            
                    PDF_FOLDER = r"C:\Projects\EduShield_AI\reports\pdf_reports"
            
                    os.makedirs(PDF_FOLDER, exist_ok=True)
            
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
                    simple_pdf_path = os.path.join(
                        PDF_FOLDER,
                        f"simple_report_{timestamp}.pdf"
                    )
            
                    professional_pdf_path = os.path.join(
                        PDF_FOLDER,
                        f"professional_report_{timestamp}.pdf"
                    )
            
                    try:
            
                        generate_simple_pdf(
                            report_data,
                            simple_pdf_path
                        )
            
                        generate_professional_pdf(
                            report_data,
                            professional_pdf_path
                        )
            
                        st.markdown(
                        f"""
                        <div class="recommendation-card">
                        <h4>Recommended Actions</h4>
                        
                        <ul>
                        <li>Academic Mentoring</li>
                        <li>Attendance Monitoring</li>
                        <li>Faculty Counselling</li>
                        <li>Assignment Tracking</li>
                        </ul>
                        
                        </div>
                        """,
                        unsafe_allow_html=True
                        )
            
                        with open(simple_pdf_path, "rb") as pdf:
            
                            st.download_button(
                                "📄 Download Simple PDF",
                                pdf,
                                file_name=os.path.basename(
                                    simple_pdf_path
                                ),
                                mime="application/pdf"
                            )
            
                        with open(
                            professional_pdf_path,
                            "rb"
                        ) as pdf:
            
                            st.download_button(
                                "⭐ Download Professional PDF",
                                pdf,
                                file_name=os.path.basename(
                                    professional_pdf_path
                                ),
                                mime="application/pdf"
                            )
            
                    except Exception as e:
            
                        st.error(
                            f"PDF Generation Error: {e}"
                        )
        except Exception as e:

            st.error(f"Prediction Error: {e}")

