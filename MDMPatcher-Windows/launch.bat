@echo off
REM MDMPatcher Enhanced - Windows Edition Launcher
REM This script makes it easy to launch the application on Windows

echo ========================================
echo MDMPatcher Enhanced - Windows Edition
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo Python: OK
echo.

REM Check if dependencies are installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

echo Dependencies: OK
echo.

REM Launch the application
echo Launching MDMPatcher Enhanced...
echo.
python main.py

REM If application exits with error, pause to show error
if errorlevel 1 (
    echo.
    echo Application exited with error
    pause
)
