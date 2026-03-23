@echo off
:: ─────────────────────────────────────────────
:: npm_uninstall.bat
:: Usage  : npm_uninstall.bat <package>
:: Example: npm_uninstall.bat cors
::
:: Removes package AND updates package.json
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: npm_uninstall.bat cors
    exit /b 1
)

echo Uninstalling %* ...
cd /d "/mnt/user-data/outputs/repo/examples/nodejs_project/backend"
npm uninstall %*

if %errorlevel% neq 0 (
    echo Uninstall failed!
    exit /b 1
)

echo.
echo Done! package.json updated automatically by npm.
