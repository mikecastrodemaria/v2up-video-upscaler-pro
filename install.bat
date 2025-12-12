@echo off
REM Video Upscaler Pro - Installation Script for Windows
REM This script sets up the Python virtual environment and installs dependencies

echo ========================================
echo Video Upscaler Pro - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

REM Check Python version is 3.10+
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo ERROR: Python 3.10 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 10 (
    echo ERROR: Python 3.10 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

echo [5/5] Installing dependencies...
echo This may take several minutes...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo To start the application, run:
echo   start.bat
echo.
echo Or manually:
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
pause
