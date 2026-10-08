@echo off

echo Mypy code checking
echo.

:: Checks for uv, synchronizes and activates the virtual environment
cd "%~dp0..\environment"
call .\uv_sync_dev.bat

echo Running mypy
uv run mypy .\json_spec .\tests
