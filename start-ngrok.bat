@echo off
echo.
echo ============================================================
echo    Mental Health Database - ngrok Tunnel Starter
echo ============================================================
echo.
echo Make sure your application is running in Visual Studio first!
echo.
echo Starting ngrok tunnel on port 58346...
echo.
echo Once started, you'll see a URL like:
echo   https://abc123.ngrok-free.app
echo.
echo Share that URL to access from any device!
echo.
echo Press Ctrl+C to stop the tunnel
echo ============================================================
echo.

ngrok http 58346
