@echo off
echo ====================================
echo  DIRECT COMPILATION
echo ====================================
echo.

REM Check that we are in the correct folder
if not exist launcher.py (
    echo ERROR: launcher.py not found
    echo Make sure you are in the windows-build-package folder
    pause
    exit /b 1
)

echo Creating executable...
echo.

REM Compile directly with all parameters
pyinstaller ^
    --name TextAnalysisLLM ^
    --onedir ^
    --console ^
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
    --clean ^
    --noconfirm ^
    launcher.py

echo.
if exist "dist\TextAnalysisLLM\TextAnalysisLLM.exe" (
    echo ====================================
    echo  COMPILATION SUCCESSFUL!
    echo ====================================
    echo.
    echo Executable at: dist\TextAnalysisLLM\TextAnalysisLLM.exe
    echo.
    echo You can test the application by running:
    echo dist\TextAnalysisLLM\TextAnalysisLLM.exe
    echo.
) else (
    echo ====================================
    echo  COMPILATION ERROR
    echo ====================================
    echo Check the messages above
)

pause