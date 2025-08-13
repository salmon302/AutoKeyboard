@echo off
echo AutoKeyboard Presser - Python Source Launcher
echo ============================================
echo.
echo This launcher runs AutoKeyboard from Python source code.
echo Recommended for users experiencing antivirus false positives.
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo Running from Python source...
python run_from_source.py

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error.
    pause
)
