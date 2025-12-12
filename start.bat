@echo off
REM Video Upscaler Pro - Start Script for Windows

echo ========================================
echo Video Upscaler Pro
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if app.py exists
if not exist app.py (
    echo ERROR: app.py not found
    echo The application may not be properly installed
    pause
    exit /b 1
)

REM Start the application
echo Starting Video Upscaler Pro...
echo.
echo The application will open in your browser automatically.
echo To stop the application, press Ctrl+C in this window.
echo.
python app.py

REM If app exits, pause to show any error messages
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application exited with error code %errorlevel%
    pause
)
