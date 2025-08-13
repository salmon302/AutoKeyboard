# Run all unit tests
@echo off
echo AutoKeyboard - Running Tests
echo ===========================

REM Check if virtual environment exists
if not exist .venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Running unit tests...
python -m unittest discover -s tests -p "test_*.py" -v

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ All tests passed!
) else (
    echo.
    echo ✗ Some tests failed!
)

echo.
pause
