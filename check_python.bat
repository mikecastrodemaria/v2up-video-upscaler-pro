@echo off
REM Python Version Checker - Verifies stable Python installation
REM Checks for beta, RC, or other unstable versions

echo ========================================
echo Python Installation Checker
echo ========================================
echo.

REM Check available Python installations
echo Checking for Python installations...
echo.

REM Try Python 3.12
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [Found] Python 3.12:
    for /f "tokens=*" %%i in ('py -3.12 --version 2^>^&1') do set PY312_VERSION=%%i
    echo   %PY312_VERSION%
    echo   %PY312_VERSION% | findstr /C:"b" /C:"rc" /C:"a" >nul
    if %errorlevel% equ 0 (
        echo   [WARNING] This is a BETA/RC version - NOT RECOMMENDED!
        set PY312_STABLE=0
    ) else (
        echo   [OK] Stable release
        set PY312_STABLE=1
    )
    echo.
)

REM Try Python 3.11
py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [Found] Python 3.11:
    for /f "tokens=*" %%i in ('py -3.11 --version 2^>^&1') do set PY311_VERSION=%%i
    echo   %PY311_VERSION%
    echo   %PY311_VERSION% | findstr /C:"b" /C:"rc" /C:"a" >nul
    if %errorlevel% equ 0 (
        echo   [WARNING] This is a BETA/RC version - NOT RECOMMENDED!
        set PY311_STABLE=0
    ) else (
        echo   [OK] Stable release
        set PY311_STABLE=1
    )
    echo.
)

REM Try Python 3.10
py -3.10 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [Found] Python 3.10:
    for /f "tokens=*" %%i in ('py -3.10 --version 2^>^&1') do set PY310_VERSION=%%i
    echo   %PY310_VERSION%
    echo   %PY310_VERSION% | findstr /C:"b" /C:"rc" /C:"a" >nul
    if %errorlevel% equ 0 (
        echo   [WARNING] This is a BETA/RC version - NOT RECOMMENDED!
        set PY310_STABLE=0
    ) else (
        echo   [OK] Stable release
        set PY310_STABLE=1
    )
    echo.
)

REM Check system python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [Found] System Python:
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PY_VERSION=%%i
    echo   %PY_VERSION%
    echo   %PY_VERSION% | findstr /C:"b" /C:"rc" /C:"a" >nul
    if %errorlevel% equ 0 (
        echo   [WARNING] This is a BETA/RC version - NOT RECOMMENDED!
    ) else (
        echo   [OK] Stable release
    )
    echo.
)

echo ========================================
echo Recommendations:
echo ========================================
echo.

REM Provide recommendations
if "%PY312_STABLE%"=="1" (
    echo [RECOMMENDED] Use Python 3.12 stable
    echo   Run: py -3.12 -m venv venv
) else if "%PY311_STABLE%"=="1" (
    echo [RECOMMENDED] Use Python 3.11 stable
    echo   Run: py -3.11 -m venv venv
) else if "%PY310_STABLE%"=="1" (
    echo [RECOMMENDED] Use Python 3.10 stable
    echo   Run: py -3.10 -m venv venv
) else (
    echo [ACTION REQUIRED] No stable Python 3.10+ found
    echo.
    echo Please install a STABLE release of Python:
    echo   - Python 3.11.x: https://www.python.org/downloads/release/python-3119/
    echo   - Python 3.12.x: https://www.python.org/downloads/release/python-3127/
    echo.
    echo IMPORTANT:
    echo   1. Download the "Windows installer (64-bit)"
    echo   2. During installation, check "Add Python to PATH"
    echo   3. Avoid beta, RC, or alpha versions
    echo.
)

echo ========================================
echo.
pause
