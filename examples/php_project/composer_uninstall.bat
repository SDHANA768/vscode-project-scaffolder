@echo off
:: ─────────────────────────────────────────────
:: composer_uninstall.bat
:: Usage  : composer_uninstall.bat <package>
:: Example: composer_uninstall.bat guzzlehttp/guzzle
::
:: Removes package AND updates composer.json + composer.lock
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: composer_uninstall.bat guzzlehttp/guzzle
    exit /b 1
)

echo Removing %* ...
cd /d "/mnt/user-data/outputs/repo/examples/php_project/backend"
composer remove %*

if %errorlevel% neq 0 (
    echo Uninstall failed!
    exit /b 1
)

echo.
echo Done! composer.json and composer.lock updated.
