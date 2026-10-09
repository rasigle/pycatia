:: Build HTML documentation with Sphinx.
@echo off

set BUILD_FOLDER=docs\build\html

:: Checks for uv, synchronizes and activates the virtual environment
cd "%~dp0..\environment"
call .\uv_check_activate_venv.bat

echo Synchronizing docs dependencies
uv sync --extra docs
echo - done
echo.

echo Building documentation into %BUILD_FOLDER%
uv run sphinx-build -n -T -b html docs/source %BUILD_FOLDER%
if errorlevel 1 (
    echo Documentation build failed.
    exit /b 1
)
echo - done
echo.

echo Opening documentation
start %BUILD_FOLDER%\index.html
