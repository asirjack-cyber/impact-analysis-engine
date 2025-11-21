# Impact Analysis Engine – AI-Powered Developer Mapping System

A lightweight, automated AI-driven impact analysis tool that takes a JIRA requirement/feature change and produces:

✔ Module impact report  
✔ Impacted features  
✔ Regression areas  
✔ Risk assessment  
✔ Suggested test cases  
✔ Code hotspots  
✔ Auto-generated PDF report  
✔ Optional PPT generation (for presentations)

Built using FastAPI, Groq LLM, and ReportLab.

## Features

### 1. AI-Driven Impact Analysis
- Takes natural language JIRA text
- Maps it to modules, features, dependencies
- Uses Groq LLM to identify upstream/downstream impacts

### 2. Developer Mapping Engine
- Each module contains:
  - Features
  - Descriptions
  - Code locations
  - Upstream/downstream impact rules
- Uses developer_mapping.json

### 3. Automatic PDF Report Generation
- Clean professional formatting
- Bold headings
- Risk level highlight
- Saved as:
  output/impact_report.pdf

### 4. Optional PowerPoint (PPTX) Generation
- Executive-level summary
- Architecture overview
- Impact matrix
- Test recommendations

### 5. FastAPI Microservice
- Exposes /analyze endpoint
- Accepts JIRA text via JSON

### 6. Windows + Linux Run Support
- Shell script (Linux/macOS)
- .bat Windows script

## Project Structure

impact-dev-mapping/
├── analyzer.py
├── groq_client.py
├── report_generator.py
├── report_pdf_generator.py
├── developer_mapping.json
├── main.py
├── sample_jira.txt
├── run_demo.sh
├── run_demo.bat
├── README.md
└── requirements.txt
└── .env (User Need to create and add GROQ_API_KEY)

##Environment Setup

Create a .env file in the project root with the following variables:

# .env
GROQ_API_KEY=your_groq_api_key_here

##Steps to follow:

1.Go to Groq Console → API Keys
2.Generate a new API key
3.Copy the key and place it in the .env file as shown above

## Installation & Setup

1. Clone the repository
git clone https://github.com/asirjack-cyber/impact-analysis-engine
cd impact-analysis-engine

2. Install dependencies
pip install -r requirements.txt

3. Create .env file
GROQ_API_KEY=your_api_key_here

## Running the Project

Windows:
run_demo.bat

Linux/Mac:
bash run_demo.sh

---

## API Usage

POST /analyze

Request:
{
  "jira_text": "Add new limit validation"
}

Response:
{
  "impact_report": {
    "status": "success",
    "report": {
      "pdf_file": "output/impact_report.pdf",
      "text": "### IMPACT ANALYSIS REPORT ..."
    }
  }
}


##PPT

ImpactAnalyzer.ppt


## Example PDF Output

Formatted sections include:
- Summary / Reasoning (bold)
- Modules Impacted (bold)
- Files / Regression Areas (bold)
- Risk Level (bold)
- Recommended Test Cases (bold)
- Code Hotspots (bold)

## Windows Batch Script (run_demo.bat)

@echo off
echo Running Impact Analysis Demo
type sample_jira.txt | curl -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d @sample_jira.txt
pause

## License

MIT License

## Contributions

Pull requests are welcome! Create issues for bugs or improvements.