# groq_client.py
"""
Robust Groq client with JSON-repair wrapper.
Ensures valid JSON output from llama-3.3-70b-versatile.
"""

import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# Load .env from same folder
current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY missing in .env file")

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"


def _extract_json(text: str) -> str:
    """Extract first JSON object from text."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or start >= end:
        raise ValueError("No JSON block found in model output")
    return text[start:end + 1]


async def analyze_with_groq(jira_text: str, mapping: dict) -> dict:
    """Call Groq and return valid JSON dict."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert impact analysis engine.\n"
                        "Return ONLY valid JSON. Do NOT include markdown or text outside JSON.\n"
                        f"Developer mapping:\n{json.dumps(mapping)}\n"
                        "Required output shape:\n"
                        '{ "impacted_features": {}, "impact_reasoning": "", "risk_level": "Low|Medium|High", '
                        '"regression_areas": [], "recommended_testcases": [], "code_hotspots": [] }'
                    ),
                },
                {"role": "user", "content": f"Analyze this Jira: {jira_text}"}
            ],
            temperature=0.0,
            max_tokens=4096
        )

        # Try direct parsing
        raw_text = response.choices[0].message.content
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            # Extract JSON from any extra text
            cleaned = _extract_json(raw_text)
            return json.loads(cleaned)

    except Exception as e:
        return {"status": "error", "error": str(e)}
