from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import os

from datetime import datetime

def generate_professional_pdf(data, output_path):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    content = []
    
    # ==================================
    # HEADER
    # ==================================

    title = Paragraph(
        "EduShield AI - Student Dropout Report",
        styles["Title"]
    )
    
    content.append(title)
    content.append(Spacer(1, 20))
    content.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1,15)
    )
    # ==================================
    # STUDENT DETAILS
    # ==================================

    content.append(
        Paragraph(
            "<b>Student Information</b>",
            styles["Heading2"]
        )
    )
    
    content.append(
        Paragraph(
            f"Student Name: {data.get('Student_Name', '')}",
            styles["BodyText"]
        )
    )
    
    content.append(
        Paragraph(
            f"Age: {data.get('Age','')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Department: {data.get('Department','')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"GPA: {data.get('GPA','')}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Attendance Rate: {data.get('Attendance_Rate','')}%",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 15))

    # ==================================
    # PREDICTION
    # ==================================

    content.append(
        Paragraph(
            "<b>Prediction Result</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Percentage: {data.get('Risk_Percent','')}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {data.get('Risk_Level','')}",
            styles["BodyText"]
        )
    )
    
    content.append(
        Paragraph(
            "<font color='red'><b>AI Risk Assessment Completed</b></font>",
            styles["BodyText"]
        )
    )
    content.append(Spacer(1, 20))

    # ==================================
    # RECOMMENDATIONS
    # ==================================

    content.append(
        Paragraph(
            "<b>Recommendations</b>",
            styles["Heading2"]
        )
    )

    if data["Risk_Level"] == "Low":

        recommendation = """
        • Continue regular monitoring<br/>
        • Encourage extracurricular participation<br/>
        • Maintain academic support
        """

    elif data["Risk_Level"] == "Medium":

        recommendation = """
        • Academic mentoring<br/>
        • Weekly attendance tracking<br/>
        • Faculty counselling<br/>
        • Assignment monitoring
        """

    else:

        recommendation = """
        • Immediate intervention required<br/>
        • Parent communication<br/>
        • Mental health counselling<br/>
        • Academic support program<br/>
        • Weekly performance review
        """

    content.append(
        Paragraph(
            recommendation,
            styles["BodyText"]
        )
    )

    content.append(PageBreak())

    # ==================================
    # SHAP SUMMARY
    # ==================================

    content.append(
        Paragraph(
            "SHAP Summary Plot",
            styles["Heading1"]
        )
    )

    summary_path = "reports/figures/shap_summary.png"

    if os.path.exists(summary_path):

        content.append(
            Image(
                summary_path,
                width=450,
                height=250
            )
        )

    content.append(PageBreak())

    # ==================================
    # SHAP BAR
    # ==================================

    content.append(
        Paragraph(
            "SHAP Feature Importance",
            styles["Heading1"]
        )
    )

    bar_path = "reports/figures/shap_bar.png"

    if os.path.exists(bar_path):

        content.append(
            Image(
                bar_path,
                width=450,
                height=250
            )
        )

    content.append(PageBreak())

    # ==================================
    # SHAP WATERFALL
    # ==================================

    content.append(
        Paragraph(
            "SHAP Waterfall Plot",
            styles["Heading1"]
        )
    )

    waterfall_path = "reports/figures/shap_waterfall.png"

    if os.path.exists(waterfall_path):

        content.append(
            Image(
                waterfall_path,
                width=450,
                height=250
            )
        )
    
    content.append(PageBreak())

    content.append(
        Paragraph(
            "EduShield AI",
            styles["Title"]
        )
    )
    
    content.append(
        Paragraph(
            "Student Dropout Prediction & Early Warning System",
            styles["BodyText"]
        )
    )
    
    content.append(
        Paragraph(
            "Predict • Explain • Prevent",
            styles["Heading2"]
        )
    )
    doc.build(content)
