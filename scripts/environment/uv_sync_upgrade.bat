:: Batch script to synchronize all specified dependencies
@echo off

:: Checks for uv, synchronizes and activates the virtual environment
call uv_check_activate_venv.bat

echo Upgrading all specified dependencies
uv sync --upgrade
echo - done
echo.
