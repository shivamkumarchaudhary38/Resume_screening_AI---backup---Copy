from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------
# Font Registration
# ---------------------------------------

try:
    pdfmetrics.registerFont(
        TTFont("Arial", "arial.ttf")
    )
    FONT_NAME = "Arial"
except:
    FONT_NAME = "Helvetica"

# ---------------------------------------
# Styles
# ---------------------------------------

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.fontName = FONT_NAME
title_style.alignment = TA_CENTER
title_style.textColor = colors.darkblue
title_style.spaceAfter = 15

heading_style = styles["Heading2"]
heading_style.fontName = FONT_NAME
heading_style.textColor = colors.darkblue
heading_style.spaceBefore = 12
heading_style.spaceAfter = 10

normal_style = styles["BodyText"]
normal_style.fontName = FONT_NAME
normal_style.leading = 18
normal_style.spaceAfter = 8

table_text_style = styles["BodyText"]
table_text_style.fontName = FONT_NAME
table_text_style.leading = 15
table_text_style.wordWrap = "CJK"

footer_style = styles["Italic"]
footer_style.fontName = FONT_NAME
footer_style.alignment = TA_CENTER
footer_style.textColor = colors.grey

# ---------------------------------------
# Generate PDF Report
# ---------------------------------------

def generate_report(
    filename,
    score,
    skills,
    education,
    experience,
    review,
    match_score
):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    # ---------------------------------------
    # Title
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Offline AI Resume Analysis Report",
            title_style
        )
    )

    elements.append(Spacer(1, 20))
        # ---------------------------------------
    # ATS Information Table
    # ---------------------------------------

    skills_text = ", ".join(skills) if skills else "Not Found"
    education_text = ", ".join(education) if education else "Not Found"

    data = [

        [
            Paragraph("<b>Field</b>", table_text_style),
            Paragraph("<b>Value</b>", table_text_style)
        ],

        [
            Paragraph("ATS Score", table_text_style),
            Paragraph(f"{score}/100", table_text_style)
        ],

        [
            Paragraph("Job Match Score", table_text_style),
            Paragraph(f"{match_score}%", table_text_style)
        ],

        [
            Paragraph("Skills", table_text_style),
            Paragraph(skills_text, table_text_style)
        ],

        [
            Paragraph("Education", table_text_style),
            Paragraph(education_text, table_text_style)
        ],

        [
            Paragraph("Experience", table_text_style),
            Paragraph(str(experience), table_text_style)
        ]

    ]

    table = Table(
        data,
        colWidths=[160, 320]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0d6efd")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("BACKGROUND", (0,1), (0,-1), colors.HexColor("#eef4ff")),
            ("BACKGROUND", (1,1), (1,-1), colors.white),

            ("GRID", (0,0), (-1,-1), 0.7, colors.grey),

            ("FONTNAME", (0,0), (-1,-1), FONT_NAME),

            ("FONTSIZE", (0,0), (-1,-1), 10),

            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING", (0,0), (-1,-1), 10),

            ("VALIGN", (0,0), (-1,-1), "TOP"),

            ("ALIGN", (0,0), (-1,0), "CENTER"),
            ("ALIGN", (0,1), (0,-1), "CENTER"),
            ("ALIGN", (1,1), (1,-1), "LEFT")

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 20))
        # ---------------------------------------
    # AI Resume Review
    # ---------------------------------------

    elements.append(
        Paragraph(
            "AI Resume Review",
            heading_style
        )
    )

    elements.append(Spacer(1, 8))

    review_box = Table(
        [
            [
                Paragraph(
                    review.replace("\n", "<br/>"),
                    normal_style
                )
            ]
        ],
        colWidths=[480]
    )

    review_box.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8f9fa")),

            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#d6d6d6")),

            ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d6d6d6")),

            ("LEFTPADDING", (0,0), (-1,-1), 12),

            ("RIGHTPADDING", (0,0), (-1,-1), 12),

            ("TOPPADDING", (0,0), (-1,-1), 10),

            ("BOTTOMPADDING", (0,0), (-1,-1), 10),

            ("VALIGN", (0,0), (-1,-1), "TOP")

        ])

    )

    elements.append(review_box)

    elements.append(Spacer(1, 20))
        # ---------------------------------------
    # Overall Resume Result
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Overall Resume Result",
            heading_style
        )
    )

    elements.append(Spacer(1, 8))

    if score >= 80:
        result = "⭐⭐⭐⭐⭐ Excellent Resume"
        result_color = colors.green

    elif score >= 60:
        result = "⭐⭐⭐⭐ Good Resume"
        result_color = colors.darkgoldenrod

    elif score >= 40:
        result = "⭐⭐⭐ Average Resume"
        result_color = colors.orange

    else:
        result = "⭐⭐ Needs Improvement"
        result_color = colors.red

    result_style = styles["Heading2"]
    result_style.fontName = FONT_NAME
    result_style.textColor = result_color
    result_style.alignment = TA_CENTER

    result_box = Table(
        [
            [Paragraph(result, result_style)]
        ],
        colWidths=[480]
    )

    result_box.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8f9fa")),

            ("BOX", (0,0), (-1,-1), 1.2, result_color),

            ("TOPPADDING", (0,0), (-1,-1), 12),

            ("BOTTOMPADDING", (0,0), (-1,-1), 12),

            ("LEFTPADDING", (0,0), (-1,-1), 10),

            ("RIGHTPADDING", (0,0), (-1,-1), 10),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE")

        ])

    )

    elements.append(result_box)

    elements.append(Spacer(1, 20))
        # ---------------------------------------
    # Footer
    # ---------------------------------------

    elements.append(
        Paragraph(
            "Generated by Offline AI Resume Analyzer",
            footer_style
        )
    )

    elements.append(Spacer(1, 6))

    elements.append(
        Paragraph(
            "Powered by Python • Flask • ReportLab",
            footer_style
        )
    )

    elements.append(Spacer(1, 6))

    elements.append(
        Paragraph(
            "© 2026 AI Resume Analyzer | Final Year Project",
            footer_style
        )
    )

    elements.append(Spacer(1, 15))

    # ---------------------------------------
    # Build PDF
    # ---------------------------------------

    doc.build(elements)