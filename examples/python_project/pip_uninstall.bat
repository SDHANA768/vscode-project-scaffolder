@echo off
:: ─────────────────────────────────────────────
:: pip_uninstall.bat
:: Usage  : pip_uninstall.bat <package>
:: Example: pip_uninstall.bat requests
::
:: Removes from venv AND updates requirements.txt
:: ─────────────────────────────────────────────

set VENV_PIP=/mnt/user-data/outputs/repo/examples/python_project/backend/venv/Scripts/pip.exe
set REQ=/mnt/user-data/outputs/repo/examples/python_project/backend/requirements.txt

if "%1"=="" (
    echo No package specified!
    echo Usage: pip_uninstall.bat requests
    exit /b 1
)

echo Uninstalling %* ...
"%VENV_PIP%" uninstall %* -y

if %errorlevel% neq 0 (
    echo Uninstall failed!
    exit /b 1
)

echo.
echo Updating requirements.txt ...
"%VENV_PIP%" freeze > "%REQ%"

echo.
echo Done! requirements.txt updated.
