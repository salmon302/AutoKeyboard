@echo off
echo AutoKeyboard Presser - Build Script
echo ==================================

REM Check if virtual environment exists
if not exist .venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "AutoKeyboard-Presser.exe" del "AutoKeyboard-Presser.exe"

REM Build the executable
echo Building executable with PyInstaller...
.venv\Scripts\pyinstaller.exe --clean autokeyboard.spec

REM Check if build was successful
if exist "dist\AutoKeyboard-Presser.exe" (
    echo.
    echo ✓ Build successful!
    echo.
    echo Moving executable to root directory...
    move "dist\AutoKeyboard-Presser.exe" "AutoKeyboard-Presser.exe"
    
    echo Cleaning up build files...
    rmdir /s /q build
    rmdir /s /q dist
    
    echo.
    echo ================================
    echo BUILD COMPLETE!
    echo ================================
    echo.
    echo Executable created: AutoKeyboard-Presser.exe
    echo File size: 
    for %%A in ("AutoKeyboard-Presser.exe") do echo %%~zA bytes
    echo.
    echo You can now distribute this single .exe file!
    echo.
) else (
    echo.
    echo ✗ Build failed!
    echo Check the error messages above.
    echo.
)

pause
