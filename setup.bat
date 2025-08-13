@echo off
echo Installing AutoKeyboard Presser dependencies...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo Installation completed successfully!
    echo.
    echo To run the application:
    echo   python main.py
    echo.
) else (
    echo.
    echo Installation failed. Please check the error messages above.
    echo.
)

pause
