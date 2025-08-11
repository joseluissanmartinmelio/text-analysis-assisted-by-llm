@echo off
echo ====================================
echo  BUILDING WITH VIRTUAL ENVIRONMENT
echo ====================================
echo.

REM Check that we are in the correct folder
if not exist launcher.py (
    echo ERROR: launcher.py not found
    echo Make sure you are in the correct folder
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check for icon file (optional)
set ICON_PARAM=
if exist "icon.ico" (
    echo Icon file found: icon.ico
    set ICON_PARAM=--icon icon.ico
) else (
    echo No icon file found. You can add an icon.ico file to include an icon.
)

echo Creating executable with PyInstaller...
echo.

REM Compile directly with all parameters
pyinstaller ^
    --name STALLM ^
    --onedir ^
    --console ^
    %ICON_PARAM% ^
    --add-data "templates;templates" ^
    --add-data "prompts;prompts" ^
    --add-data "src;src" ^
    --add-data "app.py;." ^
    --add-data "app_wrapper.py;." ^
    --hidden-import flask ^
    --hidden-import werkzeug ^
    --hidden-import werkzeug.routing ^
    --hidden-import werkzeug.exceptions ^
    --hidden-import jinja2 ^
    --hidden-import openai ^
    --hidden-import docx ^
    --hidden-import pypandoc ^
    --hidden-import PyMuPDF ^
    --hidden-import fitz ^
    --hidden-import black ^
    --hidden-import httpx ^
    --hidden-import certifi ^
    --hidden-import urllib.request ^
    --hidden-import socket ^
    --hidden-import threading ^
    --hidden-import subprocess ^
    --hidden-import webbrowser ^
    --hidden-import pathlib ^
    --clean ^
    --noconfirm ^
    launcher.py

echo.
if exist "dist\STALLM\STALLM.exe" (
    echo ====================================
    echo  COMPILATION SUCCESSFUL!
    echo ====================================
    echo.
    echo Executable at: dist\STALLM\STALLM.exe
    echo.
    echo You can test the application by running:
    echo dist\STALLM\STALLM.exe
    echo.
) else (
    echo ====================================
    echo  COMPILATION ERROR
    echo ====================================
    echo Check the messages above
)

pause
