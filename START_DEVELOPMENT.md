# 🎣 Fishing Lure App - Development Startup Guide

## ✅ What We Accomplished

### Security Improvements:
1. ✅ **API Key Protection**: OpenAI API key is now stored securely on the backend only
2. ✅ **No Client-Side Keys**: Mobile app no longer stores or requires API keys
3. ✅ **HTTPS Connection**: Using ngrok for secure HTTPS tunnel (iOS-compatible)
4. ✅ **Backend Connection Status**: Settings screen now shows real-time connection status

### Technical Fixes:
1. ✅ Fixed Windows Unicode/emoji encoding errors in Flask
2. ✅ Configured Flask to accept network connections (0.0.0.0)
3. ✅ Set up ngrok tunnel for HTTPS access
4. ✅ Added Windows Firewall rule for port 5000
5. ✅ Created `/health` endpoint for quick connection testing

---

## 🚀 How to Start Development

### **Every Time You Want to Develop:**

You need to run **3 things** (in 3 separate terminal windows):

#### **Terminal 1: Flask Backend**
```powershell
cd "c:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"
python app.py
```
✅ Should show: `[OK] OpenAI API key loaded from config.py`  
✅ Should show: `Running on http://10.0.0.245:5000`

---

#### **Terminal 2: ngrok Tunnel**
```powershell
cd "c:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure"
.\ngrok.exe http 5000
```
✅ Should show: `Forwarding https://something.ngrok-free.dev -> http://localhost:5000`

**Important:** The ngrok URL changes each time you restart! If you restart ngrok, you'll need to update the mobile app with the new URL.

---

#### **Terminal 3: Expo (Mobile App)**
```powershell
cd "c:\Users\hippi\OneDrive\Desktop\Code\Fishing Lure\FishingLureApp"
npx expo start
```
✅ Scan the QR code with Expo Go on your phone  
✅ App should load and connect to backend via ngrok

---

## 📝 **Current Configuration**

### Backend URL:
- **Current ngrok URL**: `https://corolitic-diane-unapprehending.ngrok-free.dev`
- **Location**: `FishingLureApp/src/services/backendService.js` (line 5)

### API Key:
- **Location**: `.env` file in project root (never commit this!)
- **Loaded by**: `config.py`
- **Used by**: `app.py` → `mobile_lure_classifier.py`

### Important Files:
- `app.py` - Flask backend server
- `mobile_lure_classifier.py` - Lure analysis logic
- `config.py` - Configuration (loads from .env)
- `.env` - Environment variables (contains API key)
- `FishingLureApp/src/services/backendService.js` - Mobile app backend connection

---

## 🔧 **If ngrok URL Changes**

When you restart ngrok, the URL will change. Here's how to update your mobile app:

### Option A: Manual Update
1. Get the new ngrok URL from the ngrok terminal
2. Open `FishingLureApp/src/services/backendService.js`
3. Update line 5:
   ```javascript
   const BACKEND_URL = __DEV__ 
     ? 'https://YOUR-NEW-NGROK-URL-HERE.ngrok-free.dev'
     : 'https://your-production-server.com';
   ```
4. Restart Expo: `npx expo start --clear`

### Option B: Quick Script (I can create one if needed)

---

## 🧪 **Testing Checklist**

### Backend Health Check:
- Open browser: `http://localhost:5000/health`
- Should see: `{"status":"ok","message":"Backend is running","timestamp":"..."}`

### ngrok Health Check:
- Open browser: `https://your-ngrok-url.ngrok-free.dev/health`
- Should see the same JSON response

### Mobile App Check:
- Open Expo Go app → Settings
- Backend Connection should show: **✅ Connected**
- Can take photos and analyze lures successfully

---

## 📱 **Using the App**

1. **Take a Photo**: Home screen → "📷 Take Photo with Camera"
2. **Analyze**: Photo is sent to backend via ngrok HTTPS tunnel
3. **Results**: Get lure type, confidence, target species, and fishing tips!
4. **Tackle Box**: View all previously analyzed lures
5. **Settings**: Check backend connection status

---

## ⚠️ **Important Notes**

### ngrok Free Tier Limitations:
- ✅ URL changes every time you restart ngrok
- ✅ Session expires after ~2 hours of inactivity
- ✅ Free tier includes HTTPS automatically
- ✅ Perfect for development and testing

### For Long-Term Development:
Consider ngrok paid plan ($8/month) for:
- Fixed domain name (no need to update app when restarting)
- Longer session times
- Custom domains

### For Production (App Store):
You'll eventually need to deploy to a real server:
- **Heroku** (easy, free tier available)
- **Railway** (modern, free tier)
- **Render** (simple deployment)
- **AWS/Google Cloud/Azure** (enterprise-grade)

All provide HTTPS automatically, which iOS requires.

---

## 🎯 **What's Next?**

Now that your mobile app is working, you can:

1. **Test all features** - Make sure everything works as expected
2. **Add more features** - Enhance the app with new functionality
3. **Consider Supabase** - Add cloud database for multi-user support
4. **Plan deployment** - When ready, deploy to production server
5. **Polish UI/UX** - Improve the user experience

---

## 🆘 **Troubleshooting**

### "Disconnected" in Settings:
- Check if Flask is running (`python app.py`)
- Check if ngrok is running (`.\ngrok.exe http 5000`)
- Verify ngrok URL in `backendService.js` matches the current tunnel URL

### ngrok Session Expired:
- Restart ngrok: `.\ngrok.exe http 5000`
- Update mobile app with new URL
- Restart Expo

### Analysis Not Working:
- Check Flask terminal for errors
- Verify OpenAI API key in `.env` file
- Check if you have OpenAI API credits

---

**Last Updated:** October 15, 2025  
**Status:** ✅ Fully Functional with ngrok HTTPS Tunnel  
**Current ngrok URL:** `https://corolitic-diane-unapprehending.ngrok-free.dev`

