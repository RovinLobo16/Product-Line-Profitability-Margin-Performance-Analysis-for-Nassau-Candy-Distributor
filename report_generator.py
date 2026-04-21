from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(insights):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    for i in insights:
        content.append(Paragraph(i, styles["Normal"]))

    doc.build(content)

    return "report.pdf"
