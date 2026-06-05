import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import os
from datetime import datetime
# --------------------------------------------------
# LOAD MODEL & PREPROCESSOR
# --------------------------------------------------

model = joblib.load("models/best_model.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")


def show_prediction():
    from src.utils.pdf_generator import (
    generate_simple_pdf,
    generate_professional_pdf
)
    import os
    st.header("🎯 Student Dropout Risk Prediction")

    st.markdown("---")

    # ==================================================
    # USER INPUTS
    # ==================================================

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=40,
        value=20
    )

    family_income = st.number_input(
        "Family Income",
        min_value=0,
        value=30000
    )

    study_hours = st.number_input(
        "Study Hours Per Day",
        min_value=0.0,
        value=3.0
    )

    attendance_rate = st.slider(
        "Attendance Rate (%)",
        0,
        100,
        75
    )

    assignment_delay = st.number_input(
        "Assignment Delay Days",
        min_value=0,
        value=2
    )

    travel_time = st.number_input(
        "Travel Time (Minutes)",
        min_value=0,
        value=20
    )

    stress_index = st.slider(
        "Stress Index",
        0.0,
        10.0,
        5.0
    )

    gpa = st.slider(
        "GPA",
        0.0,
        4.0,
        3.0
    )

    semester_gpa = st.slider(
        "Semester GPA",
        0.0,
        4.0,
        3.0
    )

    cgpa = st.slider(
        "CGPA",
        0.0,
        4.0,
        3.0
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    internet_access = st.selectbox(
        "Internet Access",
        ["Yes", "No"]
    )

    part_time_job = st.selectbox(
        "Part Time Job",
        ["Yes", "No"]
    )

    scholarship = st.selectbox(
        "Scholarship",
        ["Yes", "No"]
    )

    semester = st.selectbox(
        "Semester",
        ["Year 1", "Year 2", "Year 3", "Year 4"]
    )

    department = st.selectbox(
        "Department",
        ["CS", "Engineering", "Business", "Arts"]
    )

    parental_education = st.selectbox(
        "Parental Education",
        ["High School", "Bachelor", "Master", "PhD"]
    )

    # ==================================================
    # PREDICTION BUTTON
    # ==================================================

    if st.button("Predict Risk"):

        # ----------------------------------------------
        # Feature Engineering
        # ----------------------------------------------

        student_pressure_index = (
            stress_index * assignment_delay
        ) / (study_hours + 1)

        academic_risk_score = (
            (100 - attendance_rate)
            + ((4 - gpa) * 10)
        )

        income_stress_ratio = (
            stress_index /
            (family_income + 1)
        )

        gpa_consistency_score = abs(
            gpa - semester_gpa
        )

        attendance_efficiency = (
            attendance_rate /
            (travel_time + 1)
        )

        study_efficiency_score = (
            gpa /
            (study_hours + 1)
        )

        financial_risk_indicator = (
            1 / (family_income + 1)
        ) * 100000

        academic_momentum = (
            semester_gpa - cgpa
        )

        attendance_risk_index = (
            100 - attendance_rate
        )

        stress_burden_score = (
            stress_index *
            (100 - attendance_rate)
        )

        # ----------------------------------------------
        # Create Input DataFrame
        # ----------------------------------------------

        input_df = pd.DataFrame({

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

            "Student_Pressure_Index":
                [student_pressure_index],

            "Academic_Risk_Score":
                [academic_risk_score],

            "Income_Stress_Ratio":
                [income_stress_ratio],

            "GPA_Consistency_Score":
                [gpa_consistency_score],

            "Attendance_Efficiency":
                [attendance_efficiency],

            "Study_Efficiency_Score":
                [study_efficiency_score],

            "Financial_Risk_Indicator":
                [financial_risk_indicator],

            "Academic_Momentum":
                [academic_momentum],

            "Attendance_Risk_Index":
                [attendance_risk_index],

            "Stress_Burden_Score":
                [stress_burden_score]
        })

        try:

            processed_input = preprocessor.transform(
                input_df
            )

            probability = model.predict_proba(
                processed_input
            )[0][1]

            risk_percent = round(
                probability * 100,
                2
            )
            
             
            if risk_percent<30:
                risk_level="Low"
            elif risk_percent<70:
                risk_level="Medium"
            else:
                risk_level="High"
                
            #Streamlit Session State
            st.session_state["latest_prediction"] = {
                "Age": age,
                "Department": department,
                "GPA": gpa,
                "Attendance_Rate": attendance_rate,
                "Stress_Index": stress_index,
                "Risk_Percent": risk_percent,
                "Risk_Level": risk_level
            }

            st.session_state["report_data"] = {
                "Age": age,
                "Department": department,
                "GPA": gpa,
                "Attendance Rate": attendance_rate,
                "Stress Index": stress_index,
                "Risk(%)": risk_percent
            }
            #save prediction history
           
            username = st.session_state.get(
                "user", "guest"
            )
            history_data=pd.DataFrame({
                "Username":[username],
                "Timestamp":[datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )],
                "Age":[age],
                "Department":[department],
                "GPA":[gpa],
                "Attendance_Rate":[attendance_rate],
                "Stress_index":[stress_index],
                "Risk_percent":[risk_percent],
                "Risk_level":[risk_level]
            })
            history_file=("C:\Projects\EduShield_AI\data\predictions\predictions_history.csv")
            if not os.path.exists(history_file):
                history_data.to_csv(history_file,index=False)
            else:
                history_data.to_csv(history_file, mode="a",header=False,index=False)
            
            #Risk gauge
            fig=go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=risk_percent,
                    title={"text":"Student dropout Risk(%)"},
                    gauge={"axis":{"range":[0,100]},
                           "bar":{"thickness":0.4},
                           "steps":[{"range":[0,30],"color":"lightgreen"},
                                    {"range":[30,70],"color":"gold"},
                                    {"range":[70,100],"color":"salmon"}]}
                    
                )
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )
            
            st.subheader(
                f"Dropout Risk: {risk_percent}%"
            )

            if risk_percent < 30:

                st.success(
                    "🟢 LOW RISK"
                )

            elif risk_percent < 70:

                st.warning(
                    "🟠 MEDIUM RISK"
                )

            else:

                st.error(
                    "🔴 HIGH RISK"
                )
            
            #recommendation    
            st.markdown("---")
            st.subheader(
                "💡 Recommended Actions"
            )
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
                
            #PDF Report generator
            st.markdown("---")
            st.subheader("📄 PDF Report Generator")
            report_data={
                "Age":age,"Department":department,"GPA":gpa,"Attendance Rate":attendance_rate,"Stress Index":stress_index,"Risk(%)":risk_percent
            }
            if st.button("Generate PDF Reports"):
                
                #create folder
                PDF_FOLDER = r"C:\Projects\EduShield_AI\reports\pdf_reports"
                st.write("PDF Folder:", PDF_FOLDER)
                st.write(
                    "Folder Exists:",
                    os.path.exists(PDF_FOLDER)
                )
                os.makedirs(PDF_FOLDER,exist_ok=True)
                
                #Timestamp
                timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
                
                #file paths
                simple_pdf_paths=os.path.join(PDF_FOLDER,f"simple_report_{timestamp}.pdf")
                professional_pdf_path=os.path.join(PDF_FOLDER,f"professional_report_{timestamp}.pdf")
                
                #generate pdfs
                try:
                    generate_simple_pdf(
                        report_data,
                        simple_pdf_paths
                    )
                
                    generate_professional_pdf(
                        report_data,
                        professional_pdf_path
                    )
                
                    st.success(
                        "PDF Reports Generated Successfully!"
                    )
                
                except Exception as pdf_error:
                
                    st.error(
                        f"PDF Generation Error: {pdf_error}"
                    )
                st.info(f"Saved in:\n{PDF_FOLDER}")
                
                #download buttons
                col1,col2=st.columns(2)
                with col1:
                    with open(simple_pdf_paths,"rb") as pdf_file:
                        st.download_button(
                            label="📄 Download Simple PDF",
                            data=pdf_file,file_name=os.path.basename(
                                simple_pdf_paths
                            ),
                            mime="application/pdf"
                        )
                with col2:
                        with open(professional_pdf_path,"rb") as pdf_file:
                            st.download_button(label="⭐ Download Professional PDF",data=pdf_file,file_name=os.path.basename(professional_pdf_path),
                                               mime="application/pdf"
                )
        except Exception as e:

            st.error(
                f"Prediction Error: {e}"
            )