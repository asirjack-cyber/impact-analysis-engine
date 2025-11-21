# analyzer.py

import json
from report_generator import generate_report
from groq_client import analyze_with_groq

class ImpactAnalyzer:

    def __init__(self, mapping_file="developer_mapping.json"):
        with open(mapping_file, "r") as f:
            full_map = json.load(f)
            self.modules = full_map["modules"]

    async def analyze(self, jira_text: str):

        # Call Groq AI with modules mapping
        ai_response = await analyze_with_groq(jira_text, self.modules)

        # Error from Groq
        if "error" in ai_response:
            return {
                "status": "error",
                "details": ai_response
            }

        # Convert Groq output into readable report
        final_report = generate_report(ai_response, self.modules)

        # If report is plain text returned by generator → wrap in dict
        if isinstance(final_report, str):
            final_report = {"text": final_report}

        return {
            "status": "success",
            "report": final_report
        }
