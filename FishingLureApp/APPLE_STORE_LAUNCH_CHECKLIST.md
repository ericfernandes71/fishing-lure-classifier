# Apple App Store Launch Checklist – MyTackleBox

Use this right before you submit (or resubmit) to the App Store.

---

## 1. RevenueCat (production)

- [ ] **Production API key** in `src/services/subscriptionService.js`  
  - `REVENUECAT_API_KEY_IOS_PRODUCTION` must be your **production** iOS key from RevenueCat (starts with `appl_`).  
  - Test key is only for dev; production builds use this.
- [ ] **RevenueCat** project is connected to **App Store Connect** (Shared Secret / App-Specific Shared Secret).
- [ ] **Products in RevenueCat** match App Store Connect:  
  - `fishing_lure_pro_monthly`, `fishing_lure_pro_yearly`, `fishing_lure_pro_lifetime` (or whatever you use).
- [ ] **Entitlement** in RevenueCat (e.g. "MyTackleBox Pro") is attached to those products.

---

## 2. App Store Connect

- [ ] **App** created and status is “Prepare for Submission” (or ready for new version).
- [ ] **In‑App Purchases** (subscriptions) created and approved:  
  - Monthly, Yearly, Lifetime (or your set).  
  - Product IDs match the app + RevenueCat.
- [ ] **Pricing** set for each subscription.
- [ ] **App information** filled: name, subtitle, description, keywords, category (e.g. Sports), age rating.
- [ ] **Privacy Policy URL** and **Support URL** (or support email) set.
- [ ] **Screenshots** uploaded for required device sizes (e.g. 6.7", 6.5" iPhones).
- [ ] **Version** and **Build** numbers correct for this submission.

---

## 3. Build & upload

- [ ] **EAS production iOS build** (store build):
  ```bash
  cd FishingLureApp
  eas build --platform ios --profile production-ios
  ```
- [ ] After build finishes, **submit to App Store**:
  ```bash
  eas submit --platform ios --latest
  ```
  (Or upload the `.ipa` from EAS in App Store Connect.)
- [ ] In App Store Connect, **select the new build** for the version you’re submitting.
- [ ] Complete **Export Compliance**, **Content Rights**, **Advertising Identifier**, etc., if prompted.

---

## 4. Final checks

- [ ] **Quota / subscriptions** tested on TestFlight (free user countdown, block at limit, PRO flow).
- [ ] **Backend** live and healthy (e.g. `https://fishing-lure-backend.onrender.com/health`).
- [ ] No **test-only** screens or debug menus in the build (or they’re hidden for production).
- [ ] **Sign in / sign up** and **paywall** work on a real device.

---

## 5. Submit

- [ ] In App Store Connect, click **Submit for Review**.
- [ ] Answer **questionnaire** (encryption, ads, etc.) if asked.

---

**Docs in this repo:**  
- `FINAL_PRE_LAUNCH_CHECKLIST.md` – full pre-launch list  
- `APP_STORE_LAUNCH_GUIDE.md` – detailed launch roadmap  
- `SUBSCRIPTION_SETUP_FOR_APP_STORES.md` – subscription/product setup
