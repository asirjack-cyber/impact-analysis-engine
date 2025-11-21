@echo off
echo ---------------------------------------
echo   IMPACT ANALYSIS ENGINE - STARTUP
echo ---------------------------------------

REM Step 1: Check Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not installed!
    pause
    exit /b
)

REM Step 2: Create venv if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Step 3: Activate venv
call venv\Scripts\activate

REM Step 4: Install dependencies
echo Installing requirements...
pip install --quiet --disable-pip-version-check -r requirements.txt

REM Step 5: Check .env
IF NOT EXIST ".env" (
    echo ❌ .env missing! Add GROQ_API_KEY.
    pause
    exit /b
)

REM Step 6: Launch FastAPI server in background window
echo Starting Impact Analysis API server...
start "Impact API" cmd /k "venv\Scripts\activate & uvicorn main:app --reload"

REM Step 7: Wait for server to start
echo Waiting for server to become ready...
timeout /t 3 >nul

REM Step 8: Read sample_jira.txt and send request
echo Sending sample_jira.txt to API...
setlocal enabledelayedexpansion
set JIRA_TEXT=
for /f "tokens=* delims=" %%x in (sample_jira.txt) do (
    set JIRA_TEXT=!JIRA_TEXT! %%x
)

REM Step 9: POST request using curl
echo.
echo --- API RESPONSE ---
curl -X POST "http://127.0.0.1:8000/analyze" ^
     -H "Content-Type: application/json" ^
     -d "{ \"jira_text\": \"!JIRA_TEXT!\" }"
echo.
echo ---------------------
echo Swagger UI: http://127.0.0.1:8000/docs

pause
