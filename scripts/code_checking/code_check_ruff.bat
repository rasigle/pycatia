@echo off

set source_folder=.\src

:: Checks for uv, synchronizes and activates the virtual environment
cd "%~dp0..\environment"
call .\uv_sync_dev.bat

:: Run ruff checker
echo Running ruff code checking
uv run ruff check
