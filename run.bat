@echo off
title Rosenix AI OS Launcher
color 0B
echo =======================================================
echo          STARTING ROSENIX AI OS SYSTEM
echo =======================================================
echo.

cd /d "%~dp0"

IF EXIST "venv\Scripts\python.exe" (
    echo [Rosenix System] Using Virtual Environment Python...
    venv\Scripts\python.exe run.py
) ELSE (
    echo [Rosenix System] Using System Python...
    python run.py
)

pause
