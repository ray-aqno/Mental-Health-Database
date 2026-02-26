# ngrok Setup Guide - Mental Health Database

## 🌐 What is ngrok?

ngrok creates a secure tunnel from the internet to your localhost, giving you a public URL that works from **any device, anywhere in the world**.

**Perfect for:**
- 📱 Testing on your phone
- 🏠 Remote access
- 👥 Sharing with others off-campus
- 🎓 Portfolio demos

---

## 🚀 Quick Setup (5 Minutes)

### **Step 1: Download ngrok**

1. Go to: https://ngrok.com/download
2. Click **"Sign up"** (free account)
3. Sign up with Google/GitHub/Email
4. Download **ngrok for Windows** (ZIP file)

### **Step 2: Extract ngrok**

1. Open the downloaded ZIP file
2. Extract `ngrok.exe` to: **`C:\ngrok\`**
3. You should now have: `C:\ngrok\ngrok.exe`

### **Step 3: Get Your Auth Token**

1. After signing up, ngrok shows you a dashboard
2. Look for **"Your Authtoken"** section
3. Copy the token (looks like: `2abc123def456...`)
4. **OR** go to: https://dashboard.ngrok.com/get-started/your-authtoken

### **Step 4: Authenticate ngrok**

Open **Command Prompt** and run:

```bash
cd C:\ngrok
ngrok config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with your actual token.

You should see:
```
Authtoken saved to configuration file: C:\Users\YOUR_NAME\.ngrok2\ngrok.yml
```

---

## ✅ **You're Done with Setup!**

Now you can use ngrok anytime. Here's how:

---

## 🎯 **How to Use ngrok**

### **Method 1: Use the Helper Script (Easiest)**

1. **Start your app** in Visual Studio (F5)
2. **Double-click** `start-ngrok.bat` in your project folder
3. You'll see output like this:

```
ngrok

Session Status                online
Account                       your.email@example.com
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://a1b2-3c4d-5e6f.ngrok-free.app -> http://localhost:58346

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

4. **Copy the Forwarding URL**: `https://a1b2-3c4d-5e6f.ngrok-free.app`
5. **Open that URL on any device** - phone, tablet, another computer!

### **Method 2: Manual Command**

Open Command Prompt:
```bash
cd C:\ngrok
ngrok http 58346
```

---

## 📱 **Testing on Your Phone**

Once ngrok is running:

1. Copy the ngrok URL (e.g., `https://a1b2-3c4d-5e6f.ngrok-free.app`)
2. Open your phone's browser (Safari, Chrome, etc.)
3. Paste the URL and go!
4. **That's it!** Works from anywhere with internet.

### **First Visit Warning:**

The first time you visit, you'll see:
```
ngrok - visit site

You are about to visit: https://a1b2-3c4d-5e6f.ngrok-free.app
which is provided by a ngrok user...
```

Just click **"Visit Site"** - this is normal for free tier.

---

## 🔥 **Pro Tips**

### **Keep ngrok Running**

- Don't close the ngrok Command Prompt window
- Your app must be running in Visual Studio
- Both must stay open for the URL to work

### **URL Changes Each Time**

Free tier gives you a **new random URL** each time you restart ngrok.

**Good news:** The URL stays the same as long as you keep ngrok running!

### **Share the URL**

Send the ngrok URL via:
- Text message
- Email
- Slack/Discord
- QR code generator websites

### **Monitor Traffic**

Open: http://localhost:4040 to see:
- Who's accessing your app
- Request/response data
- Useful for debugging!

---

## 📊 **Quick Reference**

| Task | Command/Action |
|------|----------------|
| **Start ngrok** | Double-click `start-ngrok.bat` |
| **Stop ngrok** | Press Ctrl+C in ngrok window |
| **View traffic** | http://localhost:4040 |
| **Get new URL** | Restart ngrok |

---

## 🐛 **Troubleshooting**

### **"command not found" or "ngrok is not recognized"**

**Solution:**
```bash
cd C:\ngrok
ngrok http 58346
```
Make sure you're in the `C:\ngrok` folder!

### **"failed to start tunnel"**

**Solution:**
1. Make sure your app is running (F5 in Visual Studio)
2. Check that port 58346 is being used
3. Try: `ngrok http http://localhost:58346`

### **"authentication failed"**

**Solution:**
Run the auth command again:
```bash
cd C:\ngrok
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### **URL doesn't work on phone**

**Solution:**
1. Make sure ngrok is still running
2. Make sure your app is still running in Visual Studio
3. Check you copied the full URL including `https://`
4. Try the HTTP version if HTTPS has issues

### **"Too many connections" (Free Tier Limit)**

**Solution:**
- Free tier: 40 connections per minute
- For testing, this is plenty
- If exceeded, wait a minute or upgrade to paid tier

---

## 💰 **Free vs Paid**

### **Free Tier (What You Have):**
- ✅ 1 tunnel at a time
- ✅ Random URL (changes on restart)
- ✅ 40 connections/minute
- ✅ Perfect for development & testing
- ✅ "Visit Site" warning for first-time visitors

### **Paid Tier ($8-20/month):**
- Custom domain (e.g., `myapp.ngrok.app`)
- Multiple tunnels
- No connection limits
- No "Visit Site" warning
- Better for production

**For your project:** Free tier is perfect! ✅

---

## 🎓 **Usage Examples**

### **Scenario 1: Test on Your Phone**
```bash
1. Start app in Visual Studio (F5)
2. Run: start-ngrok.bat
3. Copy URL: https://abc123.ngrok-free.app
4. Open on phone - Done!
```

### **Scenario 2: Demo to Professor**
```bash
1. Start app and ngrok
2. Email URL to professor
3. They can access from any device
4. Works during your presentation!
```

### **Scenario 3: Portfolio/Job Application**
```bash
1. Start app and ngrok
2. Add URL to resume/portfolio
3. Recruiters can test it live
4. Keep app running during job search!
```

---

## 🔒 **Security Notes**

### **What ngrok Can See:**
- ngrok can see requests going through the tunnel
- Use HTTPS URLs (they provide this automatically)
- Don't expose sensitive databases or APIs

### **Best Practices:**
- ✅ Only run ngrok when needed
- ✅ Don't share URLs publicly
- ✅ Stop ngrok when done testing
- ✅ Keep your authtoken private

### **For This Project:**
Your Mental Health Database is **read-only public information**, so ngrok is safe to use! ✅

---

## 📋 **Checklist**

Before asking for help, verify:

- [ ] ngrok.exe is in `C:\ngrok\`
- [ ] You ran the auth command with your token
- [ ] Your app is running in Visual Studio (F5)
- [ ] You're running ngrok from `C:\ngrok` folder
- [ ] You copied the full HTTPS URL

---

## 🎉 **You're Ready!**

**Next Steps:**
1. ✅ Download ngrok from https://ngrok.com/download
2. ✅ Extract to `C:\ngrok\`
3. ✅ Run auth command with your token
4. ✅ Use `start-ngrok.bat` anytime you need access!

**Need help?** Check the troubleshooting section above!

---

## 🔗 **Useful Links**

- ngrok Download: https://ngrok.com/download
- Your Authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
- ngrok Dashboard: https://dashboard.ngrok.com/
- ngrok Docs: https://ngrok.com/docs

---

**Happy Testing! 🚀📱**
