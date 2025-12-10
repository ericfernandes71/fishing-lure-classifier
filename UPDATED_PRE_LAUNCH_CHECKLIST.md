# 🚀 Updated Pre-Launch Checklist - MyTackleBox

**Last Updated:** Based on current codebase state

---

## ✅ COMPLETED - Ready to Go!

### Technical Setup:
- ✅ EAS Project ID configured (`0d80e90f-7dd9-4210-b6b4-d1fb3e8cc6af`)
- ✅ App name updated to "MyTackleBox"
- ✅ Bundle ID: `com.fishinglure.analyzer`
- ✅ Version: 1.0.0
- ✅ Backend verified and running
- ✅ Supabase security patches applied
- ✅ Console logging wrapped in `__DEV__` checks
- ✅ Bug fixes completed (SettingsScreen)

### Legal Documents:
- ✅ Privacy Policy hosted: https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
- ✅ Terms of Service hosted: https://ericfernandes71.github.io/fishing-lure-classifier/TERMS_OF_SERVICE.html
- ✅ Support email: mytackleboxapp@gmail.com

### App Store Content:
- ✅ Descriptions written (in `APP_STORE_ASSETS_MYTACKLEBOX.md`)
- ✅ Keywords prepared
- ✅ Screenshots taken (can update with production builds later)

### RevenueCat Integration:
- ✅ RevenueCat integrated and working
- ✅ Test subscriptions working
- ⚠️ **Currently using TEST API keys** (needs production keys before launch)

---

## 🔴 CRITICAL - Must Complete Before Store Submission

### 1. **RevenueCat Production Setup** ⚠️ HIGHEST PRIORITY
**Status:** Currently using test keys - MUST switch to production before launch

**Steps:**
1. [ ] Log into RevenueCat dashboard: https://app.revenuecat.com/
2. [ ] Navigate to: Project Settings → API Keys
3. [ ] Copy **Production** API keys (separate for iOS and Android)
4. [ ] Update `FishingLureApp/src/services/subscriptionService.js`:
   ```javascript
   const REVENUECAT_API_KEY_IOS = 'YOUR_PRODUCTION_IOS_KEY_HERE';
   const REVENUECAT_API_KEY_ANDROID = 'YOUR_PRODUCTION_ANDROID_KEY_HERE';
   ```
5. [ ] Connect RevenueCat to App Store Connect (iOS)
   - In RevenueCat: Integrations → App Store Connect
   - Follow setup wizard
6. [ ] Connect RevenueCat to Google Play Console (Android)
   - In RevenueCat: Integrations → Google Play
   - Follow setup wizard

**Why Critical:** Test keys won't work in production builds. Subscriptions will fail.

---

### 2. **Developer Accounts** 💳
**Status:** Required before building production apps

**iOS:**
- [ ] Apple Developer Program ($99/year)
  - Sign up: https://developer.apple.com/programs/
  - Approval: 1-2 days typically
  - Required for: iOS builds, App Store submission

**Android:**
- [ ] Google Play Developer Account ($25 one-time)
  - Sign up: https://play.google.com/console/signup
  - Approval: Usually instant
  - Required for: Android submission

---

### 3. **App Store Connect Setup** (iOS) 📱
**Status:** Need to create listing and configure

**Steps:**
1. [ ] Log into App Store Connect: https://appstoreconnect.apple.com/
2. [ ] Create new app:
   - Name: "MyTackleBox"
   - Primary Language: English
   - Bundle ID: `com.fishinglure.analyzer`
   - SKU: `mytacklebox-001` (or your choice)
3. [ ] Fill out App Information:
   - Subtitle: "AI Lure ID & Catch Tracker"
   - Category: Sports (primary), Utilities (secondary)
   - Age Rating: 4+ (Everyone)
4. [ ] Add Privacy Policy URL:
   - https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
5. [ ] Add Support URL: mytackleboxapp@gmail.com
6. [ ] Upload screenshots (from `screenshots/` folder or retake on device)
7. [ ] Add app description (copy from `APP_STORE_ASSETS_MYTACKLEBOX.md`)
8. [ ] Add keywords: `fishing,lure,bass,tackle,fish,identify,catalog,catch,angler,bait`
9. [ ] Create subscription products:
   - Monthly subscription
   - Yearly subscription
   - Lifetime (one-time purchase)
   - Set pricing for each
10. [ ] Complete App Privacy section (required)
11. [ ] Complete payments profile (if not done)

---

### 4. **Google Play Console Setup** (Android) 🤖
**Status:** Need to create listing and configure

**Steps:**
1. [ ] Log into Google Play Console: https://play.google.com/console/
2. [ ] Create new app:
   - Name: "MyTackleBox"
   - Default Language: English (United States)
   - App or Game: App
   - Free or Paid: Free (with in-app purchases)
3. [ ] Complete Store Listing:
   - Short description (80 chars max): "AI-powered fishing lure identification and catch tracking app"
   - Full description (copy from `APP_STORE_ASSETS_MYTACKLEBOX.md`)
   - Category: Sports
   - Privacy Policy URL: https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
4. [ ] Upload screenshots:
   - Phone: 1080 x 1920 px (4-8 screenshots)
   - Feature Graphic: 1024 x 500 px (required)
5. [ ] Complete Content Rating questionnaire
6. [ ] Set up subscription products:
   - Monthly subscription
   - Yearly subscription
   - Lifetime (one-time purchase)
   - Set pricing for each
7. [ ] Complete payments profile (if not done)

---

### 5. **Production Builds** 🏗️
**Status:** Build after completing steps 1-2 above

**iOS Build:**
```bash
cd FishingLureApp
eas build --platform ios --profile production
```
- [ ] Build completes successfully
- [ ] Download and test on physical iPhone
- [ ] Verify subscriptions work (with production keys)
- [ ] Test all features

**Android Build:**
```bash
cd FishingLureApp
eas build --platform android --profile production
```
- [ ] Build completes successfully
- [ ] Download and test on physical Android device
- [ ] Verify subscriptions work (with production keys)
- [ ] Test all features

---

### 6. **Final Testing** 🧪
**Status:** Test production builds thoroughly

**Subscription Testing:**
- [ ] Test monthly subscription purchase
- [ ] Test yearly subscription purchase
- [ ] Test lifetime purchase
- [ ] Test subscription cancellation flow
- [ ] Test restore purchases
- [ ] Verify PRO features unlock correctly

**App Functionality:**
- [ ] Test lure analysis (camera and gallery)
- [ ] Test tackle box save/load
- [ ] Test catch logging
- [ ] Test user authentication
- [ ] Test offline behavior
- [ ] Test error handling (network errors, etc.)

**Platform Testing:**
- [ ] Test on iOS device
- [ ] Test on Android device
- [ ] Test on different screen sizes
- [ ] Test on slow network connection

---

## 🟡 IMPORTANT - Should Complete

### 7. **App Store Optimization**
- [ ] Review and optimize app description
- [ ] Ensure keywords are effective
- [ ] Consider app preview video (optional but recommended)
- [ ] Prepare promotional text (iOS)

### 8. **Analytics & Monitoring**
- [ ] Set up crash reporting (Sentry, Bugsnag, etc.)
- [ ] Set up analytics (optional but recommended)
- [ ] Monitor RevenueCat dashboard for subscription metrics

### 9. **Support Preparation**
- [ ] Prepare FAQ document
- [ ] Set up email templates for common support requests
- [ ] Document known issues (if any)

---

## 📋 Quick Reference

### Your URLs:
- **Privacy Policy:** https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
- **Terms of Service:** https://ericfernandes71.github.io/fishing-lure-classifier/TERMS_OF_SERVICE.html
- **Support Email:** mytackleboxapp@gmail.com
- **Backend:** https://fishing-lure-backend.onrender.com

### App Details:
- **Name:** MyTackleBox
- **Subtitle:** AI Lure ID & Catch Tracker
- **Bundle ID:** com.fishinglure.analyzer
- **Package Name:** com.fishinglure.analyzer
- **Version:** 1.0.0
- **Build Number:** 1 (iOS) / 1 (Android)

### RevenueCat:
- **Current Status:** ⚠️ Using TEST keys
- **Entitlement ID:** MyTackleBox Pro
- **Product IDs:** monthly, yearly, lifetime
- **Action Required:** Switch to production keys before launch

### Store Assets:
- **Descriptions:** See `APP_STORE_ASSETS_MYTACKLEBOX.md`
- **Screenshots:** In `screenshots/` folder (can update with production builds)

---

## ⚠️ Critical Notes

1. **RevenueCat Keys:**
   - ⚠️ You're currently using TEST keys
   - Production builds will FAIL if test keys are used
   - MUST switch to production keys before building for stores

2. **Subscription Products:**
   - Must be created in BOTH App Store Connect AND Google Play Console
   - Product IDs must match exactly: `monthly`, `yearly`, `lifetime`
   - RevenueCat must be connected to both stores

3. **Build Order:**
   - Get developer accounts first
   - Switch to production RevenueCat keys
   - Then build production apps
   - Test thoroughly before submitting

4. **Submission Timeline:**
   - iOS review: Usually 24-48 hours
   - Android review: Usually 1-3 days
   - First submission may take longer

---

## 🎯 Current Status Summary

**✅ Ready:**
- All code is ready
- Legal documents are live
- App store content is prepared
- Technical setup is complete

**⚠️ Need to Complete:**
1. Switch RevenueCat to production keys (CRITICAL)
2. Get developer accounts (if not already)
3. Create store listings
4. Build production apps
5. Test production builds
6. Submit to stores

---

## 🚀 Next Steps (In Order)

1. **Get RevenueCat production keys** ← START HERE
2. **Get developer accounts** (if needed)
3. **Create store listings** (App Store Connect + Google Play)
4. **Switch to production keys in code**
5. **Build production apps**
6. **Test production builds**
7. **Submit to stores**
8. **Launch!** 🎉

---

**You're very close!** The main blocker is switching to RevenueCat production keys. Once that's done and you have developer accounts, you can build and submit! 🚀

