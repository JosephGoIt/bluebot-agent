@echo off
setlocal

echo ============================================
echo  Bluebot Agent - Source Setup
echo ============================================
echo.

:: Check Python 3.12+
python --version 2>nul | findstr /r "3\.1[2-9]\|3\.[2-9][0-9]" >nul
if errorlevel 1 (
    echo [ERROR] Python 3.12 or newer is required.
    echo Download from: https://www.python.org/downloads/
    pause & exit /b 1
)

:: Create virtualenv
echo [1/7] Creating virtual environment...
python -m venv venv
if errorlevel 1 ( echo [ERROR] Failed to create venv. & pause & exit /b 1 )

:: Activate
call venv\Scripts\activate.bat

:: Upgrade pip silently
echo [2/7] Upgrading pip...
python -m pip install --upgrade pip --quiet

:: Install requirements
echo [3/7] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 ( echo [ERROR] Dependency install failed. & pause & exit /b 1 )

:: Upgrade playwright and browser-use
echo [4/7] Upgrading playwright and browser-use...
pip install --upgrade playwright browser-use --quiet

:: Fix pydantic (force-reinstall to ensure compiled extensions match Python)
echo [5/7] Reinstalling pydantic (ensures C extensions match Python version)...
pip install --force-reinstall --no-cache-dir pydantic pydantic-core jiter --quiet

:: Install Playwright Chromium (fallback browser if Chrome not found)
echo [6/7] Installing Playwright Chromium (fallback browser)...
playwright install chromium --with-deps
if errorlevel 1 ( echo [WARN] Playwright Chromium install failed - ensure CHROME_PATH is set in config.txt )

:: Create config.txt if missing
if not exist config.txt (
    echo [7/7] Creating config.txt template...
    (
        echo # Bluebot Configuration File
        echo # Get your Gemini API key at: https://aistudio.google.com/apikey
        echo.
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
    ) > config.txt
    echo.
    echo ACTION REQUIRED: Open config.txt and add your Gemini API key.
) else (
    echo [7/7] config.txt already exists.
)

echo.
echo ============================================
echo  Setup complete! Run the app with:
echo    venv\Scripts\python.exe main.py
echo ============================================
echo.
pause
