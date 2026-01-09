@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
    echo Starting Music Bot using Virtual Environment...
    .venv\Scripts\python.exe src\main.py
) else (
    echo Starting Music Bot using System Python...
    python src\main.py
)
pause
