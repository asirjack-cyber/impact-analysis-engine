# main.py

from fastapi import FastAPI
from analyzer import ImpactAnalyzer
from report_generator import save_report_pdf

app = FastAPI(title="Impact Analysis Engine")

analyzer = ImpactAnalyzer()

@app.post("/analyze")
async def analyze_requirement(data: dict):
    jira_text = data.get("jira_text", "")

    # Run impact analysis
    result = await analyzer.analyze(jira_text)

    # If analysis successful → generate PDF
    if result["status"] == "success":
        text_report = result["report"].get("text")
        if text_report:
            pdf_created = save_report_pdf(text_report, "impact_report.pdf")
            if pdf_created:
                print("PDF generated: impact_report.pdf")
            else:
                print("PDF creation failed.")
        else:
            print("No report text available — cannot generate PDF.")

    return {
        "impact_report": result
    }
