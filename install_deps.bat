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

:: 2. Check for FFmpeg
echo [2/4] Checking for FFmpeg...
set FFMPEG_OK=0
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 set FFMPEG_OK=1
if exist ffmpeg.exe set FFMPEG_OK=1

if %FFMPEG_OK% equ 0 (
    echo.
    echo [!] FFmpeg not found on system.
    echo [!] It will be installed automatically via Pip in Step 4.
) else (
    echo Found FFmpeg.
)

:: 3. Create Virtual Environment
echo [3/4] Setting up virtual environment (.venv)...
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

:: 4. Install Dependencies
echo [4/4] Installing dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install --only-binary :all: -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed.
    pause
    exit /b
)

:: 4. Setup .env
if not exist .env (
    echo DISCORD_TOKEN=your_token_here>.env
    echo Created template .env file.
)

echo.
echo ==========================================
echo    INSTALLATION SUCCESSFUL!
echo ==========================================
echo IMPORTANT: Open ".env" and paste your token!
echo Then run the bot using run_bot.bat
echo ==========================================
pause
