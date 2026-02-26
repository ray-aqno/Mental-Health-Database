@echo off
echo.
echo ============================================================
echo    ngrok Setup Checker
echo ============================================================
echo.

REM Check if C:\ngrok folder exists
if exist "C:\ngrok\" (
    echo [OK] C:\ngrok folder exists
) else (
    echo [X] C:\ngrok folder NOT found
    echo     Create it with: mkdir C:\ngrok
)

echo.

REM Check if ngrok.exe exists
if exist "C:\ngrok\ngrok.exe" (
    echo [OK] ngrok.exe found
    echo.
    cd C:\ngrok
    ngrok version
) else (
    echo [X] ngrok.exe NOT found in C:\ngrok
    echo     Download from: https://ngrok.com/download
    echo     Extract ngrok.exe to: C:\ngrok\
)

echo.

REM Check if config exists (means authtoken was set)
if exist "%USERPROFILE%\.ngrok2\ngrok.yml" (
    echo [OK] ngrok is authenticated
) else (
    echo [X] ngrok NOT authenticated yet
    echo     Run: cd C:\ngrok
    echo          ngrok config add-authtoken YOUR_TOKEN
)

echo.
echo ============================================================

REM Check if app is running
echo.
echo Checking if your app is running on port 58346...
netstat -an | find "58346" > nul
if errorlevel 1 (
    echo [X] App is NOT running on port 58346
    echo     Start your app in Visual Studio (F5)
) else (
    echo [OK] App is running on port 58346
)

echo.
echo ============================================================
echo.

if exist "C:\ngrok\ngrok.exe" (
    if exist "%USERPROFILE%\.ngrok2\ngrok.yml" (
        echo You're ready to use ngrok!
        echo.
        echo Next steps:
        echo 1. Make sure your app is running in Visual Studio
        echo 2. Run: start-ngrok.bat
        echo 3. Copy the https URL and use it on any device
    ) else (
        echo Setup is incomplete. Please:
        echo 1. Get your authtoken from https://dashboard.ngrok.com
        echo 2. Run: cd C:\ngrok
        echo 3. Run: ngrok config add-authtoken YOUR_TOKEN
    )
) else (
    echo Setup is incomplete. Please:
    echo 1. Download ngrok from https://ngrok.com/download
    echo 2. Extract ngrok.exe to C:\ngrok\
)

echo.
echo ============================================================
echo.
pause
