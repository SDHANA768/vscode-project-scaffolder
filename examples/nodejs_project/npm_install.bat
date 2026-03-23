@echo off
:: ─────────────────────────────────────────────
:: npm_install.bat
:: Usage  : npm_install.bat <package>
:: Example: npm_install.bat express
:: Example: npm_install.bat axios cors dotenv
::
:: Installs package AND auto-saves to package.json
:: Use --save-dev for dev dependencies:
::   npm_install.bat jest --save-dev
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: npm_install.bat express
    exit /b 1
)

echo Installing %* ...
cd /d "/mnt/user-data/outputs/repo/examples/nodejs_project/backend"
npm install %*

if %errorlevel% neq 0 (
    echo Install failed!
    exit /b 1
)

echo.
echo Done! package.json updated automatically by npm.
