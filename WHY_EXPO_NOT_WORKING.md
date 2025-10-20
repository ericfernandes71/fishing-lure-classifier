# 🔍 Why Expo Isn't Working - Troubleshooting Guide

## 🎯 The Issue

Your mobile app (Expo) can't connect to ChatGPT API because:
1. Flask backend must be running on your computer
2. ngrok tunnel must expose Flask to the internet
3. Mobile app must have the correct ngrok URL

**All 3 must be running simultaneously!**

---

## 🔧 Step-by-Step Fix

### Step 1: Start Flask Backend ✅ (DONE)

**Terminal 1:**
```powershell
cd "C:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"
python app.py
```

**Expected Output:**
```
[OK] Supabase client initialized
[OK] OpenAI API key loaded successfully from config.py
 * Running on http://0.0.0.0:5000
```

**Status:** ✅ Running now!

---

### Step 2: Start ngrok Tunnel

**Terminal 2:**
```powershell
cd "C:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"
.\ngrok.exe http 5000
```

**Expected Output:**
```
Forwarding https://abc123.ngrok-free.app -> http://localhost:5000
```

**Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`)

---

### Step 3: Update Mobile App Config

**File:** `FishingLureApp/src/config/security.js`

```javascript
// Update this line with your ngrok URL:
export const BACKEND_URL = 'https://abc123.ngrok-free.app';
```

**Important:** 
- Don't include trailing slash
- Must start with `https://`
- Must be the exact ngrok URL from Terminal 2

---

### Step 4: Restart Expo

**Terminal 3:**
```powershell
cd "C:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure\FishingLureApp"
npx expo start --clear
```

**Scan QR code** on your phone with Expo Go app

---

## 🐛 Common Problems & Solutions

### Problem 1: "Network Error" in mobile app

**Causes:**
- Flask not running
- ngrok not running
- Wrong URL in `security.js`

**Solution:**
```powershell
# Check if Flask is running:
Test-NetConnection -ComputerName localhost -Port 5000
# Should show: TcpTestSucceeded : True

# Check if ngrok is running:
curl http://localhost:4040/api/tunnels
# Should show your ngrok tunnel info
```

---

### Problem 2: "API key not configured" error

**Cause:** OpenAI API key not loaded

**Solution:**
```powershell
# Test API key:
cd "C:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"
python -c "import config; print('Key exists:', bool(config.OPENAI_API_KEY))"
```

If it says `False`:
1. Check `.env` file exists
2. Verify `OPENAI_API_KEY=sk-proj-...` is set
3. Restart Flask (`python app.py`)

---

### Problem 3: ngrok URL changes

**Cause:** ngrok free tier generates new URLs each time

**Solution Every Time You Restart:**
1. Copy new ngrok URL from Terminal 2
2. Update `src/config/security.js`
3. Restart Expo with `--clear` flag

**Better Solution:**
- Deploy to production (see `DEPLOYMENT_GUIDE.md`)
- Get permanent URL: `https://your-app.onrender.com`

---

### Problem 4: "403 Forbidden" or "401 Unauthorized"

**Cause:** No user authentication token

**Solution:**
```javascript
// Make sure you're logged in
const { user } = useAuth();
if (!user) {
  // Show login screen
}
```

---

### Problem 5: Expo app crashes on camera

**Cause:** Camera permissions not granted

**Solution:**
- In Expo Go: Settings → Expo Go → Allow camera
- Or reinstall Expo Go app

---

## 🧪 Testing Checklist

Before testing in Expo, verify each service:

### 1. Test Flask Locally
```powershell
curl http://localhost:5000/health
```
**Expected:** `{"status":"ok","message":"Backend is running"}`

### 2. Test Through ngrok
```powershell
curl https://your-ngrok-url.ngrok-free.app/health
```
**Expected:** Same as above

### 3. Test in Browser
Open: `https://your-ngrok-url.ngrok-free.app`
**Expected:** See the web interface

### 4. Test in Mobile App
1. Open Expo Go
2. Scan QR code
3. Go to Settings tab
4. Tap "🔄 Test Connection"
**Expected:** "✅ Connected to backend"

---

## 🚫 Why This Won't Work in Production

**Current Development Flow:**
```
1. Start Flask on your laptop
2. Start ngrok to expose Flask
3. Update mobile app with ngrok URL
4. Restart Expo
5. Test on phone

Problems:
- Your laptop must be on 24/7
- ngrok URL changes every restart
- Free tier has limits (40 connections/min)
- Not scalable for real users
```

**Production Flow (What You Need):**
```
1. Deploy Flask to Render.com (one-time setup)
2. Get permanent URL: https://your-app.onrender.com
3. Update mobile app once with permanent URL
4. Build and submit to App Store
5. Users can use app anytime

Benefits:
- Always available
- Permanent URL
- No laptop needed
- Unlimited users
- Professional setup
```

---

## 📱 Current Status

### ✅ What's Working:
- Flask backend running
- OpenAI API key configured
- Supabase connected
- Code is production-ready

### ⚠️ What's Blocking Expo:
- Need to start ngrok (Terminal 2)
- Need to update security.js with ngrok URL
- Need to restart Expo with --clear

### 🎯 Quick Fix (Next 5 Minutes):
1. **Terminal 2:** `.\ngrok.exe http 5000`
2. **Copy URL:** `https://abc123.ngrok-free.app`
3. **Edit:** `FishingLureApp/src/config/security.js`
   ```javascript
   export const BACKEND_URL = 'https://abc123.ngrok-free.app';
   ```
4. **Terminal 3:** `npx expo start --clear`
5. **Test:** Take photo of lure

---

## 🎓 Understanding the Architecture

### Development (Now):
```
Your Phone (Expo Go)
  ↓
Internet
  ↓
ngrok tunnel (https://abc123.ngrok-free.app)
  ↓
Your Laptop
  ↓
Flask Backend (localhost:5000)
  ↓
OpenAI API + Supabase
```

**Dependencies:**
- Your laptop must be on
- Flask must be running
- ngrok must be running
- All 3 connected

---

### Production (Goal):
```
User's Phone (Your App)
  ↓
Internet
  ↓
Cloud Server (https://your-app.onrender.com)
  ↓
OpenAI API + Supabase
```

**Benefits:**
- No laptop needed
- Always available
- Permanent URL
- Scalable
- App Store ready

---

## 🆘 Still Not Working?

### Debug Command:
```powershell
# Run this to check everything:
cd "C:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"

# Check Flask
Test-NetConnection -ComputerName localhost -Port 5000

# Check ngrok
curl http://localhost:4040/api/tunnels

# Check API key
python -c "import config; print('API Key:', 'LOADED' if config.OPENAI_API_KEY else 'MISSING')"

# Check Supabase
python -c "from supabase_client import supabase_service; print('Supabase:', 'CONNECTED' if supabase_service.is_enabled() else 'NOT CONFIGURED')"
```

---

## 🎯 Next Steps

### For Testing Today:
1. Start ngrok
2. Update security.js
3. Test in Expo

### For Production Soon:
1. **FIRST:** Rotate OpenAI API key (exposed in chat!)
2. Deploy to Render.com (see `DEPLOYMENT_GUIDE.md`)
3. Update mobile app with production URL
4. Build for App Store
5. Launch! 🚀

---

**Need help? Check these files:**
- `DEPLOYMENT_GUIDE.md` - How to deploy to production
- `SECURITY_CHECKLIST.md` - Security best practices
- `START_DEVELOPMENT.md` - Development setup guide

**The code is ready - it just needs to be deployed properly!** 🎣

