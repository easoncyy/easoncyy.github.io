@echo off
cd /d "%~dp0"
python -c "import tkinter, yaml" >nul 2>&1
if errorlevel 1 (
  echo Python, Tkinter or PyYAML is missing. Install requirements.txt first.
  pause
  exit /b 1
)
start "" pythonw "%~dp0scripts\manage-site.pyw"
