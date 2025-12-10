# 🍎 Apple App Store Connect Setup Guide

## Step-by-Step Instructions for MyTackleBox

---

## Prerequisites

Before you start, make sure you have:
- ✅ Apple Developer Program membership ($99/year)
- ✅ Apple ID with access to App Store Connect
- ✅ RevenueCat account (already have this)

---

## Step 1: Access App Store Connect

1. Go to: https://appstoreconnect.apple.com/
2. Log in with your Apple ID (the one associated with your Developer Program)
3. You should see the App Store Connect dashboard

---

## Step 2: Create Your App

1. Click **My Apps** in the top navigation
2. Click the **+** button (top left) → **New App**
3. Fill out the form:
   - **Platform:** iOS
   - **Name:** My Tackle Box (with spaces - more readable)
   - **Primary Language:** English (U.S.)
   - **Bundle ID:** Select `com.fishinglure.analyzer` (or create it if needed)
   - **SKU:** `mytacklebox-001` (or any unique identifier you want)
   - **User Access:** Full Access (unless you have a team)
4. Click **Create**

---

## Step 3: Configure App Information

### 3.1 App Information Tab

1. In your app, go to **App Information** (left sidebar)
2. Fill out:
   - **Subtitle:** AI Lure ID & Catch Tracker (30 chars max)
   - **Category:** 
     - Primary: Sports
     - Secondary: Utilities (optional)
   - **Content Rights:** Check "I have the rights to use all content"
   - **Age Rating:** Click **Edit** → Complete questionnaire → Should result in **4+** (Everyone)

### 3.2 Pricing and Availability

1. Go to **Pricing and Availability**
2. Set:
   - **Price:** Free (with in-app purchases)
   - **Availability:** All countries (or select specific ones)

---

## Step 4: Create Subscription Products

### 4.1 Create Subscription Group

1. Go to **Features** → **In-App Purchases**
2. Click **+** → **Create Subscription Group**
3. Name it: "MyTackleBox Subscriptions" (or similar)
4. Click **Create**

### 4.2 Create Monthly Subscription

1. In the subscription group, click **+** → **Create Subscription**
2. Fill out:
   - **Reference Name:** Monthly Pro Subscription
   - **Product ID:** `monthly` ⚠️ **Must match exactly!**
   - **Subscription Duration:** 1 Month
   - **Price:** Set your price (e.g., $4.99)
   - **Display Name:** Monthly Pro
   - **Description:** Unlimited lure scans and premium features
3. Click **Create**
4. Add **Subscription Localizations:**
   - Click **Add Localization**
   - Language: English (U.S.)
   - Display Name: Monthly Pro
   - Description: Unlimited lure scans and premium features

### 4.3 Create Yearly Subscription

1. Click **+** → **Create Subscription**
2. Fill out:
   - **Reference Name:** Yearly Pro Subscription
   - **Product ID:** `yearly` ⚠️ **Must match exactly!**
   - **Subscription Duration:** 1 Year
   - **Price:** Set your price (e.g., $39.99)
   - **Display Name:** Yearly Pro
   - **Description:** Unlimited lure scans and premium features - Best Value
3. Click **Create**
4. Add localization (same as monthly)

### 4.4 Create Lifetime Purchase

1. Go back to **Features** → **In-App Purchases**
2. Click **+** → **Create In-App Purchase**
3. Select **Non-Consumable**
4. Fill out:
   - **Reference Name:** Lifetime Pro Access
   - **Product ID:** `lifetime` ⚠️ **Must match exactly!**
   - **Price:** Set your price (e.g., $99.99)
   - **Display Name:** Lifetime Pro
   - **Description:** One-time payment for lifetime access to all premium features
5. Click **Create**
6. Add localization

**⚠️ CRITICAL:** Product IDs must be exactly: `monthly`, `yearly`, `lifetime` (lowercase, no spaces)

---

## Step 5: Add App Privacy Information

1. Go to **App Privacy** (left sidebar)
2. Click **Get Started** or **Edit**
3. Answer the questions:
   - **Does your app collect data?** Yes
   - **What types of data?**
     - Photos or Videos (for lure analysis)
     - User Content (lure data, catch logs)
     - Purchase History (subscriptions)
   - **How is data used?**
     - App Functionality
     - Analytics (if you use analytics)
   - **Is data linked to user?** Yes (for account sync)
   - **Is data used for tracking?** No (unless you use ads)
4. Click **Save**

---

## Step 6: Add Store Listing Information

### 6.1 App Store Listing

1. Go to **App Store** tab (left sidebar)
2. Select **English (U.S.)** or your primary language
3. Fill out:
   - **Name:** MyTackleBox (already set)
   - **Subtitle:** AI Lure ID & Catch Tracker
   - **Promotional Text:** (Optional) The ultimate fishing companion! Identify any lure with AI.
   - **Description:** Copy from `APP_STORE_ASSETS_MYTACKLEBOX.md`
   - **Keywords:** `fishing,lure,bass,tackle,fish,identify,catalog,catch,angler,bait`
   - **Support URL:** https://ericfernandes71.github.io/fishing-lure-classifier/ (or your support page)
   - **Marketing URL:** (Optional)
   - **Privacy Policy URL:** https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html ⚠️ **Required!**

### 6.2 Screenshots

1. In the same **App Store** tab
2. Upload screenshots:
   - **iPhone 6.7" Display:** 1290 x 2796 px (required)
   - **iPhone 6.5" Display:** 1242 x 2688 px (optional but recommended)
   - You can use screenshots from your `screenshots/` folder
   - Need at least 4 screenshots, up to 10

### 6.3 App Preview (Optional)

- You can add a video preview later if you want

---

## Step 7: Create App Store Connect API Key (For RevenueCat)

This is needed to connect RevenueCat to App Store Connect.

### 7.1 Create API Key

1. Go to: https://appstoreconnect.apple.com/access/api
2. Click **Keys** tab
3. Click **+** to create a new key
4. Fill out:
   - **Name:** RevenueCat Integration (or any name)
   - **Access:** App Manager (or Admin if you're the owner)
5. Click **Generate**
6. **⚠️ IMPORTANT:** Download the `.p8` key file immediately (you can only download it once!)
7. Note the **Key ID** (shown on screen)
8. Note the **Issuer ID** (shown at top of page)

### 7.2 Save This Information

You'll need:
- **Key ID:** (e.g., `ABC123XYZ`)
- **Issuer ID:** (e.g., `12345678-1234-1234-1234-123456789012`)
- **Key File:** The `.p8` file you downloaded

**Keep these safe!** You'll need them for RevenueCat integration.

---

## Step 8: Connect RevenueCat to App Store Connect

1. Go to RevenueCat dashboard: https://app.revenuecat.com/
2. Go to **Integrations** → **App Store Connect**
3. Click **Connect** or **Add Integration**
4. Choose **App Store Connect API**
5. Enter:
   - **Key ID:** (from Step 7.2)
   - **Issuer ID:** (from Step 7.2)
   - **Private Key:** Upload the `.p8` file or paste its contents
6. Click **Connect**
7. Select your app: **MyTackleBox** (`com.fishinglure.analyzer`)
8. RevenueCat will sync your subscription products

---

## Step 9: Get Production API Keys from RevenueCat

After connecting to App Store Connect:

1. In RevenueCat dashboard, go to **Project Settings** → **API Keys**
2. You should now see production keys:
   - **iOS Production Key:** Starts with `appl_`
3. Copy the iOS production key

---

## Step 10: Update Your Code

Once you have the production iOS key, I'll help you update `subscriptionService.js`:

**Current:**
```javascript
const REVENUECAT_API_KEY_IOS = 'test_dUUNiOeOwXcEMWFAsvnVGrKkMvp';
```

**Will become:**
```javascript
const REVENUECAT_API_KEY_IOS = 'appl_YOUR_PRODUCTION_KEY_HERE';
```

---

## 📋 Quick Checklist

- [ ] Log into App Store Connect
- [ ] Create app: MyTackleBox
- [ ] Configure app information (subtitle, category, age rating)
- [ ] Create subscription group
- [ ] Create monthly subscription (Product ID: `monthly`)
- [ ] Create yearly subscription (Product ID: `yearly`)
- [ ] Create lifetime purchase (Product ID: `lifetime`)
- [ ] Complete App Privacy section
- [ ] Add store listing (description, keywords, privacy policy URL)
- [ ] Upload screenshots
- [ ] Create App Store Connect API key
- [ ] Connect RevenueCat to App Store Connect
- [ ] Get production iOS API key from RevenueCat
- [ ] Update code with production key

---

## ⚠️ Important Notes

1. **Product IDs:** Must be exactly `monthly`, `yearly`, `lifetime` (lowercase, no spaces)
2. **Privacy Policy:** Required - must be a public URL
3. **API Key File:** Download immediately - you can only download once!
4. **Subscription Status:** Products need to be in "Ready to Submit" status before they work
5. **Testing:** Use sandbox test accounts to test purchases before going live

---

## 🎯 What to Do Next

After completing these steps:
1. You'll have production iOS API key
2. RevenueCat will be connected to App Store Connect
3. Subscription products will be synced
4. Then we'll update your code with the production key

**Ready to start?** Let me know when you've completed each step or if you need help with any part! 🚀

