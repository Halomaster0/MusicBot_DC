@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo    Music Bot Dependency Installer
echo ==========================================
echo.

:: 1. Check for Python
echo [1/3] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python not found!
        echo Please install Python from https://www.python.org/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b
    ) else (
        set PY_CMD=py
    )
) else (
    set PY_CMD=python
)
echo Found: %PY_CMD%

:: 2. Create Virtual Environment
echo [2/3] Setting up virtual environment (.venv)...
if not exist .venv (
    %PY_CMD% -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b
    )
    echo Created .venv folder successfully.
) else (
    echo .venv already exists, skipping creation.
)

:: 3. Install Dependencies
echo [3/3] Installing dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install --only-binary :all: -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed.
    pause
    exit /b
)

echo.
echo ==========================================
echo    INSTALLATION SUCCESSFUL!
echo ==========================================
echo You can now run the bot using run_bot.bat
echo or Start_MusicBot_Hidden.vbs
echo ==========================================
pause
