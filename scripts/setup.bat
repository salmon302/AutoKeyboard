@echo off
echo AutoKeyboard - Environment Setup
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ================================
    echo SETUP COMPLETE!
    echo ================================
    echo.
    echo Virtual environment created and dependencies installed.
    echo.
    echo To run the application:
    echo   .\run.bat
    echo   OR
    echo   .venv\Scripts\activate.bat
    echo   python main.py
    echo.
    echo To run tests:
    echo   .\run_tests.bat
    echo.
    echo To build executable:
    echo   .\build.bat
    echo.
) else (
    echo.
    echo Setup failed. Please check the error messages above.
    echo.
)

pause
