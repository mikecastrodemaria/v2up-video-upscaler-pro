@echo off
REM Cleanup Script - Removes old virtual environment
REM Run this before reinstalling with a stable Python version

echo ========================================
echo Virtual Environment Cleanup
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo No virtual environment found.
    echo Nothing to clean up.
    echo.
    pause
    exit /b 0
)

echo This will DELETE the existing virtual environment folder.
echo You will need to run install.bat again after cleanup.
echo.

choice /C YN /M "Continue with cleanup"
if errorlevel 2 (
    echo.
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Removing virtual environment...
rmdir /s /q venv

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to remove virtual environment
    echo Make sure it's not in use (close any active terminals)
    pause
    exit /b 1
)

echo.
echo ========================================
echo Cleanup completed successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Ensure you have a stable Python installed
echo   2. Run: check_python.bat (to verify)
echo   3. Run: install.bat (to create new venv)
echo.
echo See PYTHON_SETUP_FIX.md for detailed instructions
echo.
pause
