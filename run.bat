@echo off
echo AutoKeyboard Presser
echo ===================

REM Check if virtual environment exists
if not exist .venv (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if %errorlevel% neq 0 (
        echo Setup failed. Exiting.
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting AutoKeyboard Presser...
.venv\Scripts\python.exe main.py

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error.
    pause
)
