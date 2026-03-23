@echo off
:: ─────────────────────────────────────────────
:: go_get.bat
:: Usage  : go_get.bat <package>
:: Example: go_get.bat github.com/gin-gonic/gin
::
:: Installs package AND updates go.mod + go.sum
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: go_get.bat github.com/gin-gonic/gin
    exit /b 1
)

echo Installing %* ...
cd /d "/mnt/user-data/outputs/repo/examples/go_project/backend"
go get %*

if %errorlevel% neq 0 (
    echo Install failed!
    exit /b 1
)

echo.
echo Tidying go.mod ...
go mod tidy

echo.
echo Done! go.mod and go.sum updated.
