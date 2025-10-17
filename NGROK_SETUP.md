# Using ngrok to Access Your Backend

ngrok creates a secure tunnel to your local server, bypassing all firewall/network issues!

## Setup Steps:

1. **Download ngrok:**
   - Go to: https://ngrok.com/download
   - Download and extract ngrok.exe to your project folder

2. **Sign up (free):**
   - Go to: https://dashboard.ngrok.com/signup
   - Get your authtoken

3. **Configure ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

4. **Start ngrok tunnel:**
   ```bash
   ngrok http 5000
   ```

5. **You'll get a URL like:** `https://abc123.ngrok.io`

6. **Update your mobile app:**
   - Open `FishingLureApp/src/services/backendService.js`
   - Change `BACKEND_URL` to your ngrok URL:
   ```javascript
   const BACKEND_URL = 'https://abc123.ngrok.io'
   ```

7. **Restart Expo and it will work!** 🎉

## Pros:
- ✅ Works from anywhere (not just local network)
- ✅ No firewall configuration needed
- ✅ HTTPS secure connection
- ✅ Can share with others to test

## Cons:
- ⚠️ URL changes each time you restart ngrok (free plan)
- ⚠️ Requires internet connection

