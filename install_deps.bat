@echo off
cd /d "%~dp0"
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from python.org before running this.
    pause
    exit /b
)

echo.
echo Installing dependencies (pre-compiled binaries only)...
python -m pip install --upgrade pip
pip install --only-binary :all: -r requirements.txt

echo.
echo Setup complete! You can now run the bot using run_bot.bat.
pause
