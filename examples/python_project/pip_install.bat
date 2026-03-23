@echo off
:: ─────────────────────────────────────────────
:: pip_install.bat
:: Usage  : pip_install.bat <package>
:: Example: pip_install.bat requests
:: Example: pip_install.bat numpy pandas flask
::
:: Installs into venv AND auto-updates requirements.txt
:: ─────────────────────────────────────────────

set VENV_PIP=%~dp0backend\venv\Scripts\pip.exe
set REQ=%~dp0backend\requirements.txt

if "%1"=="" (
    echo No package specified!
    echo Usage: pip_install.bat requests
    exit /b 1
)

echo Installing %* ...
"%VENV_PIP%" install %*

if %errorlevel% neq 0 (
    echo Install failed!
    exit /b 1
)

echo.
echo Updating requirements.txt ...
"%VENV_PIP%" freeze > "%REQ%"

echo.
echo Done! requirements.txt updated.
