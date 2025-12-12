@echo off
REM Video Upscaler Pro - Installation Script for Windows
REM This script sets up the Python virtual environment and installs dependencies

echo ========================================
echo Video Upscaler Pro - Installation
echo ========================================
echo.

REM Try to use Python 3.11 first (best compatibility), then 3.12, then system python
py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3.11, using it for best compatibility
    set PYTHON_CMD=py -3.11
) else (
    py -3.12 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Found Python 3.12, using it
        set PYTHON_CMD=py -3.12
    ) else (
        echo Python 3.11/3.12 not found, checking system python...
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ERROR: Python is not installed or not in PATH
            echo Please install Python 3.11 or 3.12 from https://www.python.org/
            echo Make sure to check "Add Python to PATH" during installation
            pause
            exit /b 1
        )
        set PYTHON_CMD=python
    )
)

echo [1/5] Checking Python version...
%PYTHON_CMD% --version

REM Check Python version is 3.10+
for /f "tokens=2 delims= " %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i

REM Check for beta, RC, or alpha versions
echo %PYTHON_VERSION% | findstr /C:"b" /C:"rc" /C:"a" >nul
if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo ERROR: BETA/RC/ALPHA Python detected ^(%PYTHON_VERSION%^)
    echo ============================================================
    echo.
    echo You are using an unstable Python release.
    echo This causes DLL load errors with packages like orjson.
    echo.
    echo REQUIRED: Install a STABLE release of Python:
    echo   - Python 3.11.x: https://www.python.org/downloads/release/python-3119/
    echo   - Python 3.12.x: https://www.python.org/downloads/release/python-3127/
    echo.
    echo IMPORTANT STEPS:
    echo   1. Download "Windows installer (64-bit)" for a stable version
    echo   2. During install, check "Add Python to PATH"
    echo   3. After installing, run: check_python.bat
    echo   4. Then run this installer again
    echo.
    echo ============================================================
    echo.
    pause
    exit /b 1
)
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

REM Warn about Python 3.13+ compatibility
if %MAJOR% EQU 3 if %MINOR% GEQ 13 (
    echo.
    echo ============================================================
    echo WARNING: Python 3.13+ detected ^(%PYTHON_VERSION%^)
    echo ============================================================
    echo.
    echo Python 3.13 has compatibility issues with some AI packages.
    echo.
    echo RECOMMENDED: Use Python 3.10, 3.11, or 3.12 for best results
    echo.
    echo You can continue, but AI model installation may fail.
    echo We will install core dependencies only.
    echo.
    echo Download Python 3.12: https://www.python.org/downloads/
    echo.
    echo ============================================================
    echo.
    choice /C YN /M "Continue anyway"
    if errorlevel 2 exit /b 1
    echo.
)

echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

%PYTHON_CMD% -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [4/6] Upgrading pip...
python -m pip install --upgrade pip

echo [5/6] Installing PyTorch with CUDA 12.6 support (RTX 5090, 4090, 4080, etc.)...
echo This may take several minutes (downloading ~2.5 GB)...
echo Supports: RTX 50-series, RTX 40-series, RTX 30-series, and older NVIDIA GPUs
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

echo [6/7] Installing other dependencies...
echo This may take several minutes...
pip install gradio opencv-python psutil tqdm pyyaml scikit-image imageio-ffmpeg moviepy decorator basicsr realesrgan orjson pillow numpy

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [7/7] Applying compatibility patches...
python fix_basicsr_torchvision.py
if %errorlevel% neq 0 (
    echo WARNING: Could not apply basicsr patch automatically
    echo You may need to run it manually later
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
