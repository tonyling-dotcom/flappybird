@echo off
echo Starting Flappy Bird Web Server...
echo.
echo Visit http://localhost:5000 in your browser
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start the Flask app
python app.py

