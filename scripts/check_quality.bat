@echo off
echo AutoKeyboard - Code Quality Check
echo =================================

REM Check if virtual environment exists
if not exist .venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Checking code style with flake8...
echo ----------------------------------
flake8 src/ --max-line-length=88 --ignore=E203,W503

echo.
echo Checking code formatting with black...
echo -------------------------------------
black --check src/

echo.
echo Running type checking with mypy...
echo ---------------------------------
mypy src/ --ignore-missing-imports

echo.
echo Running unit tests...
echo --------------------
python -m unittest discover -s tests -p "test_*.py" -v

echo.
echo ================================
echo Code quality check complete!
echo ================================

pause
