@echo off
setlocal
title WT32-ETH01 Ad Blocker - Setup & Flasher
cd /d "%~dp0"

echo ====================================================================
echo   WT32-ETH01 HARDWARE AD BLOCKER - AUTOMATED SETUP WIZARD
echo ====================================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH!
    echo.
    echo Please install Python 3 from https://www.python.org/
    echo During installation, be sure to check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

python setup_wizard.py

echo.
echo Press any key to exit...
pause >nul

