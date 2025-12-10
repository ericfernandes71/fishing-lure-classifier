# 🚀 Final Pre-Launch Checklist for MyTackleBox

## ✅ Already Completed

- [x] EAS Project configured
- [x] Legal documents (Privacy Policy, Terms of Service) hosted on GitHub Pages
- [x] Backend verified and running
- [x] Supabase security patches applied
- [x] RevenueCat integration complete (test mode)
- [x] UI improvements and polish
- [x] Subscription management features
- [x] App configuration (bundle ID, version, etc.)

---

## 🔴 Critical - Must Do Before Launch

### 1. **RevenueCat Production Keys** ⚠️ CRITICAL
- [ ] Get production API keys from RevenueCat dashboard
  - Go to: https://app.revenuecat.com/
  - Navigate to: Project Settings → API Keys
  - Copy **Production** keys (not test keys)
- [ ] Update `FishingLureApp/src/services/subscriptionService.js`:
  ```javascript
  const REVENUECAT_API_KEY_IOS = 'YOUR_PRODUCTION_IOS_KEY';
  const REVENUECAT_API_KEY_ANDROID = 'YOUR_PRODUCTION_ANDROID_KEY';
  ```
- [ ] Connect RevenueCat to App Store Connect (iOS)
- [ ] Connect RevenueCat to Google Play Console (Android)
- [ ] Create subscription products in App Store Connect
- [ ] Create subscription products in Google Play Console

### 2. **App Store Assets** 📸
- [ ] **Screenshots** (take on physical device):
  - iPhone 6.7": 1290 x 2796 px (4-8 screenshots)
  - iPhone 6.5": 1242 x 2688 px (4-8 screenshots)
  - Android Phone: 1080 x 1920 px (4-8 screenshots)
- [ ] **Feature Graphic** (Android only): 1024 x 500 px
- [ ] **App Icon**: Verify 1024x1024px (iOS) and 512x512px (Android)

### 3. **App Store Connect Setup** (iOS)
- [ ] Complete payments profile (if not done)
- [ ] Create app listing
- [ ] Fill out app information:
  - Name: "MyTackleBox"
  - Subtitle: "AI Lure ID & Catch Tracker"
  - Description: (use from APP_STORE_ASSETS_MYTACKLEBOX.md)
  - Keywords: fishing,lure,bass,tackle,fish,identify
  - Category: Sports
  - Age Rating: 4+
- [ ] Add Privacy Policy URL: https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
- [ ] Add Support URL: mytackleboxapp@gmail.com
- [ ] Upload screenshots
- [ ] Create subscription products (monthly, yearly, lifetime)
- [ ] Set pricing

### 4. **Google Play Console Setup** (Android)
- [ ] Complete payments profile (if not done)
- [ ] Create app listing
- [ ] Fill out store listing:
  - Name: "MyTackleBox"
  - Short description: (80 chars max)
  - Full description: (use from APP_STORE_ASSETS_MYTACKLEBOX.md)
  - Category: Sports
- [ ] Add Privacy Policy URL
- [ ] Upload screenshots
- [ ] Upload feature graphic (1024x500)
- [ ] Create subscription products (monthly, yearly, lifetime)
- [ ] Set pricing
- [ ] Complete content rating questionnaire

### 5. **Production Builds** 🏗️
- [ ] Build iOS production app:
  ```bash
  cd FishingLureApp
  eas build --platform ios --profile production
  ```
- [ ] Build Android production app:
  ```bash
  eas build --platform android --profile production
  ```
- [ ] Test production builds on physical devices
- [ ] Verify subscriptions work in production mode

### 6. **Final Testing** 🧪
- [ ] Test subscription purchase flow
- [ ] Test subscription cancellation
- [ ] Test all app features on production build
- [ ] Test on both iOS and Android
- [ ] Verify backend connectivity
- [ ] Verify Supabase sync
- [ ] Test offline functionality (if applicable)

---

## 🟡 Important - Should Do

### 7. **App Store Optimization**
- [ ] Write compelling app description
- [ ] Choose effective keywords
- [ ] Prepare promotional text (iOS)
- [ ] Consider app preview video (optional but recommended)

### 8. **Analytics & Monitoring**
- [ ] Set up crash reporting (if not already)
- [ ] Set up analytics tracking
- [ ] Monitor subscription metrics in RevenueCat
- [ ] Set up error alerting

### 9. **Support & Documentation**
- [ ] Prepare support email responses
- [ ] Document known issues (if any)
- [ ] Prepare FAQ
- [ ] Set up customer support process

---

## 🟢 Nice to Have

### 10. **Marketing Prep**
- [ ] Prepare social media posts
- [ ] Create app preview video
- [ ] Write press release (if applicable)
- [ ] Plan launch announcement

---

## 📋 Quick Reference

### Current Configuration:
- **App Name**: MyTackleBox
- **Bundle ID**: com.fishinglure.analyzer
- **Version**: 1.0.0
- **Build Number**: 1 (iOS) / 1 (Android)
- **Privacy Policy**: https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html
- **Support Email**: mytackleboxapp@gmail.com

### RevenueCat:
- **Current**: Using test keys ⚠️
- **Need**: Production keys from RevenueCat dashboard
- **Entitlement ID**: MyTackleBox Pro
- **Products**: monthly, yearly, lifetime

### Next Steps Priority:
1. **Get RevenueCat production keys** (CRITICAL - app won't work in production without this)
2. **Take screenshots** (Required for submission)
3. **Complete store listings** (Required for submission)
4. **Build production apps** (Required for submission)
5. **Test everything** (Critical before launch)

---

## ⚠️ Important Notes

1. **RevenueCat Test vs Production**: 
   - Test keys work in development but NOT in production
   - You MUST switch to production keys before submitting to stores
   - Test subscriptions won't work in production builds

2. **Subscription Products**:
   - Must be created in both App Store Connect AND Google Play Console
   - Product IDs must match exactly: `monthly`, `yearly`, `lifetime`
   - Connect RevenueCat to both stores for subscription management

3. **Build Process**:
   - Production builds take longer (30-60 minutes)
   - Test on physical devices before submitting
   - Keep test builds separate from production builds

4. **Submission Timeline**:
   - iOS: Usually 24-48 hours for review
   - Android: Usually 1-3 days for review
   - First submission may take longer

---

**Ready to launch?** Complete the 🔴 Critical items first, then proceed with submission!

