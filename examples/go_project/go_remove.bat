@echo off
:: ─────────────────────────────────────────────
:: go_remove.bat
:: Usage  : go_remove.bat <package>
:: Example: go_remove.bat github.com/gin-gonic/gin
::
:: Removes package AND updates go.mod + go.sum
:: Uses "go get package@none" (official Go removal method)
:: ─────────────────────────────────────────────

if "%1"=="" (
    echo No package specified!
    echo Usage: go_remove.bat github.com/gin-gonic/gin
    exit /b 1
)

echo Removing %1 ...
cd /d "/mnt/user-data/outputs/repo/examples/go_project/backend"
go get %1@none

if %errorlevel% neq 0 (
    echo Remove failed!
    exit /b 1
)

echo.
echo Tidying go.mod ...
go mod tidy

echo.
echo Done! go.mod and go.sum updated.
