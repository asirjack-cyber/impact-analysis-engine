# report_generator.py

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(ai_json: dict, modules: dict):
    """Generate markdown report from Groq AI JSON output."""
    
    if "impacted_features" not in ai_json:
        return {"status": "error", "error": "AI returned invalid JSON", "raw_response": ai_json}
    
    report = []
    report.append("### IMPACT ANALYSIS REPORT\n")
    
    report.append(f"**Summary / Reasoning:**\n{ai_json.get('impact_reasoning','')}\n")
    
    # Modules impacted
    report.append("**Modules Impacted:**")
    for mod, features in ai_json.get("impacted_features", {}).items():
        name = modules.get(mod, {}).get("name", mod)
        report.append(f"- {mod} ({name}) → Features: {', '.join(features)}")
    
    # Files / regression areas
    report.append("\n**Files / Regression Areas Impacted:**")
    for file in ai_json.get("regression_areas", []):
        report.append(f"- {file}")
    
    # Risk level
    report.append(f"\n**Risk Level:** {ai_json.get('risk_level','')}\n")
    
    # Test cases
    report.append("**Recommended Test Cases:**")
    for t in ai_json.get("recommended_testcases", []):
        report.append(f"- {t}")
    
    # Code hotspots
    report.append("\n**Code Hotspots:**")
    for f in ai_json.get("code_hotspots", []):
        report.append(f"- {f}")
    
    return "\n".join(report)


# -------------------------------
# SAVE REPORT AS PDF
# -------------------------------

def save_report_pdf(text: str, filename: str = "impact_report.pdf"):
    """Save the impact analysis report as a PDF with bold title & bold section headers."""
    try:
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()

        # Styles
        title_style = styles["Heading1"]
        title_style.fontSize = 16
        title_style.leading = 20

        header_style = styles["Heading3"]
        header_style.fontSize = 12
        header_style.leading = 16

        normal_style = styles["Normal"]

        story = []
        lines = text.split("\n")

        # ---- MAIN TITLE ----
        if lines:
            story.append(Paragraph(f"<b>{lines[0]}</b>", title_style))
            story.append(Paragraph("", normal_style))
            lines = lines[1:]

        for line in lines:
            stripped = line.strip()

            # --- NEW FIX: detect headings like "**Risk Level:** Medium"
            if stripped.startswith("**") and "**" in stripped[2:]:
                # Extract the bold header part
                header_part = stripped.split("**")[1]  # inside **header:**
                rest = stripped.split("**", 2)[2].strip()  # content after header

                # Build bold header + normal content
                story.append(Paragraph(f"<b>{header_part}</b> {rest}", header_style))
                continue

            # Standard bullet items
            if stripped.startswith("- "):
                story.append(Paragraph(stripped, normal_style))
                continue

            # Normal line
            story.append(Paragraph(stripped, normal_style))

        doc.build(story)
        return True

    except Exception as e:
        print("Error generating PDF:", e)
        return False
