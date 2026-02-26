# Cross-Device Access Guide

## How to Access Your Application from Other Devices

### Your Computer's IP Address
**Current IP: 10.24.169.207**

---

## Option 1: Same WiFi Network (Easiest)

### Setup Steps:

#### 1. Configure Firewall (One-Time Setup)
Right-click `allow-firewall.bat` and select **"Run as Administrator"**

This will allow incoming connections on ports:
- 58345 (HTTPS)
- 58346 (HTTP)
- 58347 (HTTPS - external)
- 58348 (HTTP - external)

#### 2. Start Your Application
Run the application from Visual Studio as normal (F5)

#### 3. Access from Other Devices
On your phone, tablet, or another computer connected to the **same WiFi network**, open a browser and go to:

**HTTP (Recommended for mobile):**
```
http://10.24.169.207:58348
```

**HTTPS (May show certificate warning):**
```
https://10.24.169.207:58347
```

> **Note:** For HTTPS, you'll see a security warning. Click "Advanced" → "Proceed" to continue.

---

## Option 2: Using ngrok (Works Anywhere - Even Different Networks)

### What is ngrok?
ngrok creates a secure tunnel to your localhost, giving you a public URL that works from anywhere.

### Setup Steps:

#### 1. Download ngrok
- Go to https://ngrok.com/download
- Create a free account
- Download ngrok for Windows

#### 2. Install and Authenticate
```bash
# Extract ngrok.exe to a folder
# Open Command Prompt in that folder
ngrok authtoken YOUR_AUTH_TOKEN
```

#### 3. Start Your Application
Run your app from Visual Studio (F5)

#### 4. Create Tunnel
Open a new Command Prompt and run:
```bash
ngrok http 58346
```

#### 5. Access Your App
ngrok will display a URL like:
```
https://abc123.ngrok.io
```

Share this URL with anyone - it works from **any device, anywhere in the world**!

---

## Option 3: Deploy to Azure/Cloud (Production)

For permanent access, consider deploying to:
- **Azure App Service** (Free tier available)
- **Heroku** (Free tier available)
- **AWS Elastic Beanstalk**

---

## Troubleshooting

### "Can't connect" from other device

1. **Check both devices are on same WiFi**
   - Both must be connected to the same network

2. **Verify Firewall Rules**
   - Re-run `allow-firewall.bat` as Administrator

3. **Check your IP hasn't changed**
   - Run `ipconfig` to verify your IP address
   - Update the URL if it changed

4. **Use HTTP instead of HTTPS**
   - Mobile browsers may block self-signed certificates
   - Use `http://10.24.169.207:58348` instead

### Certificate Warning on Mobile

This is normal for HTTPS with self-signed certificates. Options:
1. Click "Advanced" → "Proceed anyway"
2. Use HTTP instead (port 58348)

---

## Current Access URLs

### From This Computer (Localhost):
- https://localhost:58345
- http://localhost:58346

### From Other Devices (Same Network):
- http://10.24.169.207:58348
- https://10.24.169.207:58347

---

## Security Notes

⚠️ **Important:**
- These URLs only work while your computer is running the application
- Firewall rules allow incoming connections (remove if concerned)
- For production use, deploy to a proper hosting service
- Never expose sensitive data through ngrok without authentication

---

## Quick Reference

| Scenario | URL to Use |
|----------|-----------|
| Testing on your computer | http://localhost:58346 |
| Testing on your phone (same WiFi) | http://10.24.169.207:58348 |
| Testing from anywhere | Use ngrok |
| Production deployment | Deploy to Azure/Cloud |

---

## Next Steps

1. ✅ Run `allow-firewall.bat` as Administrator
2. ✅ Start your application (F5 in Visual Studio)
3. ✅ Test on another device: http://10.24.169.207:58348
4. 📱 Add to your phone's home screen for easy access
