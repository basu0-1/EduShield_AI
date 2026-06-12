import streamlit as st
from PIL import Image
import pandas as pd
from pathlib import Path

def show_explainability():

    st.markdown(
        """
        <div class="page-heading">
            <h1>🔍 Explainable AI Dashboard</h1>
            <p class="page-subtitle">
                Explore the model insights behind each risk prediction with clear driver cards, SHAP visuals, and actionable recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "latest_prediction" not in st.session_state:
        st.warning("Please generate a prediction first.")
        return

    data = st.session_state["latest_prediction"]

    st.markdown("<div class='explain-row'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='explain-metrics'>
            <div class='metric-card'>
                <h4>Risk %</h4>
                <p>{risk}%</p>
            </div>
            <div class='metric-card'>
                <h4>Attendance Rate</h4>
                <p>{attendance}%</p>
            </div>
            <div class='metric-card'>
                <h4>GPA</h4>
                <p>{gpa}</p>
            </div>
            <div class='metric-card'>
                <h4>Stress Index</h4>
                <p>{stress}</p>
            </div>
        </div>
        """.format(
            risk=f"{data['Risk_Percent']}%",
            attendance=f"{data['Attendance_Rate']}%",
            gpa=f"{data['GPA']:.2f}",
            stress=f"{data['Stress_Index']:.1f}",
        ),
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='explain-row'>", unsafe_allow_html=True)

    for title, detail, color in [
        ("📉 Attendance Risk Index", "Attendance shortfalls are the strongest driver of dropout risk.", "#fecaca"),
        ("😓 Stress Burden Score", "High stress levels amplify the likelihood of a student dropping out.", "#fde68a"),
        ("🎓 Academic Risk Score", "Academic performance remains a leading indicator in the dropout model.", "#bbf7d0"),
    ]:
        st.markdown(
            f"""
            <div class='explain-small-card' style='background: {color};'>
                <h4>{title}</h4>
                <p>{detail}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<div class='explain-image-grid'>", unsafe_allow_html=True)

    image_items = [
        {
            "title": "📊 SHAP Summary",
            "path": Path("reports/figures/shap_summary.png"),
            "description": (
                "The SHAP summary is a compact visualization of how each feature contributes to the overall prediction. "
                "It shows the most influential attributes sorted by impact and indicates whether they push the student risk higher or lower. "
                "This view helps you quickly identify the strongest positive and negative drivers for this student."
            ),
        },
        {
            "title": "📈 Feature Importance",
            "path": Path("reports/figures/shap_bar.png"),
            "description": (
                "The feature importance chart ranks each variable by its overall effect on the model output. "
                "Higher bars mean stronger influence on the student’s dropout risk, regardless of direction. "
                "Use this plot to understand which metrics are most critical for intervention planning."
            ),
        }
    ]

    for item in image_items:
        st.markdown("<div class='explain-image-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{item['title']}</h3>", unsafe_allow_html=True)
        try:
            image = Image.open(item["path"]) 
            # use explicit pixel width instead of deprecated use_column_width
            st.image(image, width=1000)
            st.markdown(
                f"<div class='image-detail-box'>{item['description']}</div>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"Unable to load {item['title']}: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("🔢 Feature Number Mapping", expanded=True):
        feature_df = pd.DataFrame(
            {
                "Feature No": [f"Feature {i}" for i in range(20)],
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
                    "Student_Pressure_Index",
                ],
            }
        )
        st.dataframe(feature_df, use_container_width=True)

    st.markdown("---")

    st.markdown("<div class='explain-row'>", unsafe_allow_html=True)

    st.markdown("<div class='explain-reco-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🧠 AI Interpretation</h3>", unsafe_allow_html=True)
    if data["Risk_Percent"] < 30:
        st.success(
            "The model predicts LOW dropout risk. Positive indicators include strong attendance, stable academic performance, and healthy stress management."
        )
    elif data["Risk_Percent"] < 70:
        st.warning(
            "The model predicts MEDIUM dropout risk. Key contributors include attendance variation, academic inconsistency, and moderate stress."
        )
    else:
        st.error(
            "The model predicts HIGH dropout risk. Main contributors are poor attendance, high stress, and weak academic momentum."
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='explain-reco-card'>", unsafe_allow_html=True)
    st.markdown("<h3>💡 Recommended Actions</h3>", unsafe_allow_html=True)
    if data["Risk_Percent"] < 30:
        st.markdown(
            """
            ✓ Continue regular progress checks<br>
            ✓ Encourage participation in campus activities<br>
            ✓ Maintain academic support channels
            """,
            unsafe_allow_html=True,
        )
    elif data["Risk_Percent"] < 70:
        st.markdown(
            """
            ✓ Provide targeted mentoring<br>
            ✓ Track attendance weekly<br>
            ✓ Offer counselling and assignment guidance
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            ✓ Initiate urgent intervention<br>
            ✓ Engage parents and support services<br>
            ✓ Create a recovery plan with academic coaching
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        """
        SHAP (SHapley Additive exPlanations) explains
        how each feature contributes to the model's
        prediction. Positive values increase dropout
        risk, while negative values reduce risk.
        """
    )

    st.markdown("---")

