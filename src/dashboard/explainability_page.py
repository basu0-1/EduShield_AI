import streamlit as st
from PIL import Image
import pandas as pd

def show_explainability():

    st.header("🔍 Explainable AI Dashboard")
    
    # TOP RISK DRIVERS
    st.subheader("🚨 Top Risk Drivers")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.error(
            "📉 Attendance Risk Index"
        )

    with col2:
        st.warning(
            "😓 Stress Burden Score"
        )

    with col3:
        st.info(
            "🎓 Academic Risk Score"
        )

    st.markdown("---")

    # CHECK PREDICTION EXISTS
    if "latest_prediction" not in st.session_state:

        st.warning(
            "Please generate a prediction first."
        )

        return

    data = st.session_state["latest_prediction"]

    # KPI CARDS
    st.subheader("📊 Current Prediction Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk %",
            f"{data['Risk_Percent']}%"
        )

    with col2:
        st.metric(
            "Attendance %",
            data["Attendance_Rate"]
        )

    with col3:
        st.metric(
            "GPA",
            data["GPA"]
        )

    st.markdown("---")

    # SHAP SUMMARY
    st.subheader("📊 SHAP Summary Plot")

    try:

        summary_img = Image.open(
            "reports/figures/shap_summary.png"
        )

        st.image(
            summary_img,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Unable to load summary plot: {e}"
        )

    st.markdown("---")

    # FEATURE IMPORTANCE + FEATURE TABLE
    # FEATURE IMPORTANCE
    st.subheader("📈 Feature Importance")    

    try:    

        bar_img = Image.open(
            "reports/figures/shap_bar.png"
        )    

        st.image(
            bar_img,
            use_container_width=True
        )    

    except Exception as e:    

        st.error(
            f"Unable to load feature importance plot: {e}"
        )
    
    st.markdown("---")
    
    # WATERFALL PLOT
    st.subheader("🌊 SHAP Waterfall Plot")

    try:

        waterfall_img = Image.open(
            "reports/figures/shap_waterfall.png"
        )

        st.image(
            waterfall_img,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Unable to load waterfall plot: {e}"
        )

    st.markdown("---")
    
    # FEATURE REFERENCE TABLE    
    with st.expander(
        "🔢 Click to View Feature Number Mapping",
        expanded=True
    ):
    
        feature_df = pd.DataFrame({
    
            "Feature No": [
                f"Feature {i}"
                for i in range(20)
            ],
    
            "Feature Name": [
    
                "Student_ID",
                "Age",
                "Gender",
                "Family_Income",
                "Internet_Access",
                "Study_Hours_per_Day",
                "Attendance_Rate",
                "Assignment_Delay_Days",
                "Travel_Time_Minutes",
                "Part_Time_Job",
                "Scholarship",
                "Stress_Index",
                "GPA",
                "Semester_GPA",
                "CGPA",
                "Semester",
                "Department",
                "Parental_Education",
                "Dropout",
                "Student_Pressure_Index"
            ]
        })
    
        st.dataframe(
            feature_df,
            use_container_width=True
        )
    
    st.markdown("---")

    # AI INTERPRETATION
    st.subheader("🧠 AI Interpretation")

    if data["Risk_Percent"] < 30:

        st.success(
            """
            The model predicts LOW dropout risk.

            Main positive indicators:

            • Strong attendance

            • Stable academic performance

            • Manageable stress levels

            • Consistent engagement
            """
        )

    elif data["Risk_Percent"] < 70:

        st.warning(
            """
            The model predicts MEDIUM dropout risk.

            Key contributing factors:

            • Attendance fluctuations

            • Academic inconsistencies

            • Moderate stress burden

            • Need for closer monitoring
            """
        )

    else:

        st.error(
            """
            The model predicts HIGH dropout risk.

            Main risk contributors:

            • Poor attendance

            • High stress levels

            • Weak academic momentum

            • Increased dropout probability
            """
        )

    st.markdown("---")
    
    # RECOMMENDATIONS
    st.subheader("💡 Recommended Actions")

    if data["Risk_Percent"] < 30:

        st.success(
            """
            ✓ Continue regular monitoring

            ✓ Encourage extracurricular participation

            ✓ Maintain academic support
            """
        )

    elif data["Risk_Percent"] < 70:

        st.warning(
            """
            ✓ Academic mentoring

            ✓ Weekly attendance tracking

            ✓ Faculty counselling

            ✓ Assignment monitoring
            """
        )

    else:

        st.error(
            """
            ✓ Immediate intervention required

            ✓ Parent communication

            ✓ Mental health counselling

            ✓ Academic support program

            ✓ Weekly performance review
            """
        )

    st.markdown("---")

    # EXPLAINABILITY NOTE
    st.info(
        """
        SHAP (SHapley Additive exPlanations) explains
        how each feature contributes to the model's
        prediction. Positive values increase dropout
        risk, while negative values reduce risk.
        """
    )
