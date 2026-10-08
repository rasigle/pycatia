:: Batch script to fully delete the virtual environment folder
@echo off

:: Go to root-folder of the repository
cd "%~dp0..\.."
set venv_folder=.\.venv

if not exist %venv_folder%\ (
    echo Virtual environment folder %venv_folder% does not exist
    exit
)

echo Found virtual environment in: %~dp0%venv_folder%
echo.

setlocal
set AREYOUSURE=N
set /P AREYOUSURE=Do you really want to delete all contents of the folder? (Y/[N])?
if /I "%AREYOUSURE%" NEQ "Y" goto end

echo Removing contents of virtual environment
echo.
@RD /S /Q %venv_folder%

if exist %venv_folder%\ (
    echo The virtual environment folder %venv_folder% couldn't be fully deleted.
    echo Make sure to remove the contents manually before trying to create a new virtual environment.
    exit
)

echo Done

:end
endlocal
