@echo off

:: Checks for uv, synchronizes and activates the virtual environment
cd "%~dp0..\environment"
call .\uv_sync_dev.bat

echo Running black code checking
uv run black --target-version py310 .\pyv5 .\tests
