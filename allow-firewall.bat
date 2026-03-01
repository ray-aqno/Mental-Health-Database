@echo off
echo Adding Windows Firewall rules for Mental Health Database...
echo.
echo You may need to run this as Administrator
echo.

netsh advfirewall firewall add rule name="Mental Health DB - Port 58345" dir=in action=allow protocol=TCP localport=58345
netsh advfirewall firewall add rule name="Mental Health DB - Port 58346" dir=in action=allow protocol=TCP localport=58346
netsh advfirewall firewall add rule name="Mental Health DB - Port 58347" dir=in action=allow protocol=TCP localport=58347
netsh advfirewall firewall add rule name="Mental Health DB - Port 58348" dir=in action=allow protocol=TCP localport=58348

echo.
echo Firewall rules added successfully!
echo.
pause
