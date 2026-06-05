from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime


def generate_simple_pdf(data, filename):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Student Dropout Risk Report", styles["Title"]))
    content.append(Spacer(1, 12))

    for key, value in data.items():
        content.append(
            Paragraph(f"{key}: {value}", styles["Normal"])
        )
        content.append(Spacer(1, 6))

    doc.build(content)


def generate_professional_pdf(data, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(
        Paragraph(
            "EduShield AI - Student Risk Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Generated on: {datetime.now()}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    # Table Data
    table_data = [["Field", "Value"]]

    for key, value in data.items():
        table_data.append([str(key), str(value)])

    table = Table(table_data)

    table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

        ])
    )

    content.append(table)

    doc.build(content)