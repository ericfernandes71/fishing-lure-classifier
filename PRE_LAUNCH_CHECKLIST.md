# 🚀 Pre-Launch Checklist - App Store Submission

## ⚠️ CRITICAL - Must Complete Before Submission

### 1. **EAS Project ID Configuration** 🔴
- [ ] **Update `app.json`**: Replace `"your-project-id-here"` with your actual EAS project ID
  - Location: `FishingLureApp/app.json` line 69
  - Run: `eas build:configure` to generate project ID
  - **Status**: ❌ Currently has placeholder value

### 2. **Privacy Policy & Terms of Service** 🔴
- [ ] **Create Privacy Policy** (REQUIRED by both stores)
  - Must cover: Camera access, photo library access, data collection, OpenAI API usage, Supabase data storage
  - Host on public URL (GitHub Pages, your website, or Notion)
  - **Status**: ❌ Not found in codebase
  
- [ ] **Create Terms of Service** (Recommended)
  - User agreement, subscription terms, cancellation policy
  - Host on public URL
  - **Status**: ❌ Not found in codebase

### 3. **Console Logging Cleanup** 🟡
- [ ] **Review and remove non-essential console.log statements**
  - Many are already wrapped in `__DEV__` checks (good!)
  - Found 113 console.log/warn/error statements
  - **Critical ones to fix**:
    - `backendService.js` line 9: `console.log('[BackendService] Using backend URL:', BACKEND_URL);` - NOT wrapped in `__DEV__`
    - `backendService.js` lines 200, 204, 211-212: Test connection logs - NOT wrapped in `__DEV__`
    - `TackleBoxScreen.js` lines 49, 51, 58: Some logs NOT wrapped in `__DEV__`
  - **Status**: ⚠️ Mostly protected, but some need attention

### 4. **Backend URL Verification** 🟡
- [ ] **Verify production backend is stable**
  - Current: `https://fishing-lure-backend.onrender.com`
  - Test all endpoints work correctly
  - Ensure backend is deployed and accessible
  - **Status**: ✅ Configured, but verify it's working

### 5. **Supabase Security Patch** 🟡
- [ ] **Run security patch SQL** (if not already done)
  - File: `supabase_security_patch.sql`
  - Fixes function search_path vulnerabilities
  - **Status**: ⚠️ SQL file exists but may not be applied

---

## 📱 App Store Specific Requirements

### iOS App Store

#### Configuration
- [x] Bundle identifier: `com.fishinglure.analyzer` ✅
- [x] Version: `1.0.0` ✅
- [x] Build number: `1` ✅
- [x] iOS deployment target: `13.0` ✅
- [x] Camera permission description ✅
- [x] Photo library permission description ✅
- [ ] **EAS Project ID** - ⚠️ Needs update

#### Assets Required
- [ ] **App Icon**: 1024x1024px PNG (check if `assets/icon.png` meets requirements)
- [ ] **Screenshots** for required device sizes:
  - [ ] iPhone 6.7" (iPhone 14 Pro Max, iPhone 15 Plus, iPhone 15 Pro Max): 1290 x 2796 px
  - [ ] iPhone 6.5" (iPhone 11 Pro Max, iPhone XS Max): 1242 x 2688 px
  - [ ] iPhone 5.5" (iPhone 8 Plus): 1242 x 2208 px
  - [ ] iPad Pro 12.9": 2048 x 2732 px (if supporting iPad)

#### App Store Connect Setup
- [ ] App created in App Store Connect
- [ ] App name: "Fishing Lure Analyzer" (or your choice, max 30 chars)
- [ ] Subtitle (max 30 chars)
- [ ] Description (4000 chars max)
- [ ] Keywords (100 chars max): `fishing,lure,bass,tackle,fish,identify,catalog,catch,angler,bait`
- [ ] Category: Sports (primary), Utilities (secondary)
- [ ] Age rating: 4+ (Everyone)
- [ ] Privacy policy URL (REQUIRED)
- [ ] Support URL
- [ ] Marketing URL (optional)

### Google Play Store

#### Configuration
- [x] Package name: `com.fishinglure.analyzer` ✅
- [x] Version code: `1` ✅
- [x] Version name: `1.0.0` ✅
- [x] Permissions configured ✅

#### Assets Required
- [ ] **App Icon**: 512x512px (check `assets/adaptive-icon.png`)
- [ ] **Feature Graphic**: 1024 x 500 px (Android only)
- [ ] **Screenshots**:
  - [ ] Phone: 1080 x 1920 px minimum (4-8 screenshots)
  - [ ] Tablet: 1600 x 2560 px (optional)

#### Google Play Console Setup
- [ ] App created in Google Play Console
- [ ] Short description (80 chars max)
- [ ] Full description
- [ ] Privacy policy URL (REQUIRED)
- [ ] Content rating questionnaire completed
- [ ] Category: Sports

---

## 🔒 Security & Compliance

### Security Checklist
- [x] No hardcoded API keys in mobile app ✅
- [x] Supabase anon key is safe to include (public, rate-limited) ✅
- [x] Backend handles sensitive operations ✅
- [x] Input validation implemented ✅
- [x] Rate limiting implemented ✅
- [ ] **Supabase security patch applied** ⚠️
- [ ] **Privacy policy created and hosted** ❌

### Data Privacy
- [x] Camera permission properly requested ✅
- [x] Photo library permission properly requested ✅
- [x] Clear usage descriptions ✅
- [ ] Privacy policy explains data collection ❌
- [ ] Privacy policy explains third-party services (OpenAI, Supabase) ❌
- [ ] User rights documented (delete account, export data) ❌

---

## 🧪 Testing Checklist

### Functional Testing
- [ ] Test on physical iOS device (iPhone)
- [ ] Test on physical Android device
- [ ] Test camera functionality
- [ ] Test photo library selection
- [ ] Test AI analysis end-to-end
- [ ] Test tackle box save/load
- [ ] Test catch logging
- [ ] Test user authentication (signup/login/logout)
- [ ] Test subscription/paywall flow (if implemented)
- [ ] Test offline behavior
- [ ] Test error handling (network errors, API errors)

### Edge Cases
- [ ] Very large images (>10MB)
- [ ] Very small images
- [ ] Corrupted images
- [ ] No camera permission
- [ ] No photo library permission
- [ ] Network timeout
- [ ] Server error (500)
- [ ] Quota exceeded (403)
- [ ] Slow network connection

### Performance
- [ ] App launches quickly (< 3 seconds)
- [ ] Images load efficiently
- [ ] No memory leaks
- [ ] Battery usage is reasonable
- [ ] App doesn't crash during normal usage

---

## 💰 Monetization (If Applicable)

### Subscription Setup
- [ ] RevenueCat configured (if using)
- [ ] Subscription products created in App Store Connect
- [ ] Subscription products created in Google Play Console
- [ ] Test with sandbox accounts
- [ ] Subscription management in settings
- [ ] Free trial configured (if offering)

### Pricing
- [ ] Pricing determined
- [ ] Free tier limits set (3 scans/month mentioned in guide)
- [ ] Premium tier benefits defined

---

## 📊 Analytics & Monitoring

### Setup Before Launch
- [ ] Analytics configured (Google Analytics, Mixpanel, etc.)
- [ ] Crash reporting configured (Sentry, Bugsnag, etc.)
- [ ] Error logging configured
- [ ] Performance monitoring set up

### Post-Launch Monitoring
- [ ] Monitor crash reports daily
- [ ] Review user feedback/ratings
- [ ] Monitor API costs (OpenAI, Supabase)
- [ ] Track downloads and subscriptions
- [ ] Monitor backend performance

---

## 🎨 Store Listing Content

### App Description (Draft)
See `APP_STORE_LAUNCH_GUIDE.md` lines 212-276 for a complete description template.

### Screenshot Ideas
1. Login/Signup screen
2. Camera/scan a lure
3. Analysis results
4. Tackle box view
5. Catch tracking
6. Lure details

### Keywords (iOS - 100 chars max)
```
fishing,lure,bass,tackle,fish,identify,catalog,catch,angler,bait
```

---

## 🚨 Immediate Action Items

### Do These First:
1. **Update EAS Project ID** in `app.json`
2. **Create and host Privacy Policy** (REQUIRED)
3. **Fix console.log statements** not wrapped in `__DEV__`
4. **Verify backend is accessible** and stable
5. **Run Supabase security patch** if not already done

### Before Building:
1. Test on physical devices
2. Verify all features work end-to-end
3. Test error scenarios
4. Check app performance
5. Review all user-facing text for typos

### Before Submission:
1. Take screenshots for all required sizes
2. Write app description
3. Prepare keywords
4. Set up analytics/crash reporting
5. Test subscription flow (if applicable)

---

## 📝 Quick Reference

### Build Commands
```bash
# iOS
eas build --platform ios --profile production-ios
eas submit --platform ios

# Android
eas build --platform android --profile production
eas submit --platform android
```

### Key Files to Review
- `FishingLureApp/app.json` - App configuration
- `FishingLureApp/eas.json` - Build configuration
- `FishingLureApp/src/config/security.js` - Backend URL
- `FishingLureApp/src/config/supabase.js` - Supabase config
- `FishingLureApp/src/services/backendService.js` - Backend service

### Important URLs
- Backend: `https://fishing-lure-backend.onrender.com`
- Supabase: `https://wisqqrerjbfbdiorlxtn.supabase.co`
- Privacy Policy: ❌ **Need to create**
- Terms of Service: ❌ **Need to create**

---

## ✅ Final Pre-Submission Checklist

- [ ] All critical items above completed
- [ ] App tested on physical devices
- [ ] All screenshots taken
- [ ] App Store Connect listing prepared
- [ ] Google Play Console listing prepared
- [ ] Privacy policy live and accessible
- [ ] Terms of service live (if created)
- [ ] Analytics configured
- [ ] Crash reporting configured
- [ ] Support email ready
- [ ] Marketing materials prepared
- [ ] Final build tested one more time

---

**Status Summary:**
- 🔴 Critical: 3 items (EAS Project ID, Privacy Policy, Terms of Service)
- 🟡 Important: 3 items (Console logs, Backend verification, Supabase patch)
- ✅ Completed: Most configuration and security items

**Estimated Time to Complete:** 2-4 hours for critical items, 1-2 days for full preparation

