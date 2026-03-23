@echo off
:: ─────────────────────────────────────────────
:: composer_install.bat
:: Usage  : composer_install.bat <package>
:: Example: composer_install.bat guzzlehttp/guzzle
::
:: Requires Composer: https://getcomposer.org
:: Installs package AND updates composer.json + composer.lock
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: composer_install.bat guzzlehttp/guzzle
    exit /b 1
)

echo Installing %* ...
cd /d "/mnt/user-data/outputs/repo/examples/php_project/backend"
composer require %*

if %errorlevel% neq 0 (
    echo Install failed! Is Composer installed?
    echo Download from: https://getcomposer.org
    exit /b 1
)

echo.
echo Done! composer.json and composer.lock updated.
