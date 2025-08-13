@echo off
echo Creating distribution package...

REM Create distribution directory
if not exist dist_package mkdir dist_package

REM Copy executable and documentation
copy AutoKeyboard-Presser.exe dist_package\
copy USER_GUIDE.md dist_package\
copy README.md dist_package\

REM Create a simple launcher instruction
echo @echo off > dist_package\run.bat
echo AutoKeyboard-Presser.exe >> dist_package\run.bat

echo.
echo Distribution package created in 'dist_package' folder!
echo Contents:
dir dist_package

pause
