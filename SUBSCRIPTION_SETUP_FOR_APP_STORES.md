# 💰 Subscription Plans Setup for App Stores

## 📋 Subscription Products for MyTackleBox

### Your Subscription Tiers:

1. **Free Tier**
   - 3 lure scans per month
   - Basic features

2. **PRO Monthly** - $4.99/month
   - Unlimited scans
   - Full catch tracking
   - All premium features

3. **PRO Yearly** - $39.99/year
   - Save 33% vs monthly
   - All PRO features

4. **Lifetime** - $49.99 one-time
   - All features forever
   - No recurring charges

---

## 🍎 iOS App Store Connect Setup

### Step 1: Create App Listing (If Not Done)

1. Go to: https://appstoreconnect.apple.com
2. Click **"My Apps"** → **"+"** → **"New App"**
3. Fill in:
   - **Platform:** iOS
   - **Name:** MyTackleBox
   - **Primary Language:** English
   - **Bundle ID:** com.fishinglure.analyzer
   - **SKU:** mytacklebox-001
   - **User Access:** Full Access

### Step 2: Create Subscription Group

1. In your app → **Features** → **In-App Purchases**
2. Click **"+"** → **"Create Subscription Group"**
3. Name: **"PRO Access"**
4. Click **"Create"**

### Step 3: Create Monthly Subscription

1. In Subscription Group → Click **"+"** → **"Create Subscription"**

**Fill in:**
- **Reference Name:** MyTackleBox PRO Monthly
- **Product ID:** `fishing_lure_pro_monthly` (must match code!)
- **Subscription Duration:** 1 Month
- **Price:** $4.99 USD
- **Free Trial:** Optional (7 days recommended)
- **Subscription Display Name:** PRO Monthly

**Localization (English):**
- **Name:** MyTackleBox PRO Monthly
- **Description:** Unlimited lure identifications, full catch tracking, and all premium features. Auto-renews monthly.

**Review Information:**
- **Screenshot:** Optional (can add later)
- **Review Notes:** "Monthly subscription for unlimited lure scans and premium features"

Click **"Create"**

### Step 4: Create Yearly Subscription

1. In same Subscription Group → Click **"+"** → **"Create Subscription"**

**Fill in:**
- **Reference Name:** MyTackleBox PRO Yearly
- **Product ID:** `fishing_lure_pro_yearly` (must match code!)
- **Subscription Duration:** 1 Year
- **Price:** $39.99 USD
- **Free Trial:** Optional (7 days recommended)
- **Subscription Display Name:** PRO Yearly

**Localization (English):**
- **Name:** MyTackleBox PRO Yearly
- **Description:** Save 33%! Unlimited lure identifications, full catch tracking, and all premium features. Auto-renews yearly.

**Review Information:**
- **Review Notes:** "Annual subscription for unlimited lure scans and premium features. Best value!"

Click **"Create"**

### Step 5: Create Lifetime Purchase

1. In your app → **Features** → **In-App Purchases**
2. Click **"+"** → **"Create In-App Purchase"**
3. Select **"Non-Consumable"**

**Fill in:**
- **Reference Name:** MyTackleBox Lifetime
- **Product ID:** `fishing_lure_pro_lifetime` (must match code!)
- **Price:** $49.99 USD

**Localization (English):**
- **Name:** MyTackleBox Lifetime Access
- **Description:** One-time purchase for lifetime access to all premium features. No recurring charges.

**Review Information:**
- **Review Notes:** "Lifetime purchase for all premium features"

Click **"Create"**

### Step 6: Submit for Review

1. All three products need to be **"Ready to Submit"**
2. Click **"Submit for Review"** on each product
3. Apple will review (usually 24-48 hours)
4. Once approved, products are active!

---

## 🤖 Google Play Console Setup

### Step 1: Create App Listing (If Not Done)

1. Go to: https://play.google.com/console
2. Click **"Create app"**
3. Fill in:
   - **App name:** MyTackleBox
   - **Default language:** English (United States)
   - **App or game:** App
   - **Free or paid:** Free
   - **Declarations:** Check required boxes

### Step 2: Create Monthly Subscription

1. Go to **Monetize** → **Subscriptions** → **Create subscription**

**Fill in:**
- **Product ID:** `fishing_lure_pro_monthly` (must match code!)
- **Name:** MyTackleBox PRO (Monthly)
- **Description:** Unlimited lure identifications, full catch tracking, and all premium features. Auto-renews monthly.
- **Billing period:** 1 month
- **Price:** $4.99 USD
- **Free trial:** Optional (7 days)
- **Grace period:** 3 days (recommended)
- **Account hold:** Enabled (recommended)

Click **"Save"**

### Step 3: Create Yearly Subscription

1. **Monetize** → **Subscriptions** → **Create subscription**

**Fill in:**
- **Product ID:** `fishing_lure_pro_yearly` (must match code!)
- **Name:** MyTackleBox PRO (Yearly)
- **Description:** Save 33%! Unlimited lure identifications, full catch tracking, and all premium features. Auto-renews yearly.
- **Billing period:** 1 year
- **Price:** $39.99 USD
- **Free trial:** Optional (7 days)
- **Grace period:** 3 days
- **Account hold:** Enabled

Click **"Save"**

### Step 4: Create Lifetime Purchase

1. Go to **Monetize** → **Products** → **In-app products**
2. Click **"Create product"**

**Fill in:**
- **Product ID:** `fishing_lure_pro_lifetime` (must match code!)
- **Name:** MyTackleBox Lifetime Access
- **Description:** One-time purchase for lifetime access to all premium features. No recurring charges.
- **Price:** $49.99 USD
- **Status:** Active

Click **"Save"**

### Step 5: Activate Products

- Subscriptions activate immediately after creation
- Lifetime product activates when you set status to "Active"
- No review needed (unlike iOS)

---

## ✅ Product ID Checklist

Make sure these match exactly in:
- ✅ Your code (`subscriptionService.js`)
- ✅ App Store Connect
- ✅ Google Play Console
- ✅ RevenueCat (when you set it up)

**Product IDs:**
- Monthly: `fishing_lure_pro_monthly`
- Yearly: `fishing_lure_pro_yearly`
- Lifetime: `fishing_lure_pro_lifetime`

---

## 📝 Subscription Details for App Store Listings

### Update Your App Store Description

Make sure your descriptions mention subscriptions. They're already in `APP_STORE_ASSETS_MYTACKLEBOX.md`:

```
💰 SUBSCRIPTION OPTIONS

FREE TIER:
• 3 lure identifications per month
• Basic tackle box features
• Limited catch tracking

PRO MONTHLY - $4.99/month:
• Unlimited lure identifications
• Full catch tracking with photos
• Advanced tackle box features
• Priority support
• All premium features

PRO YEARLY - $39.99/year:
• Save 33% vs monthly
• All PRO features
• Best value for serious anglers

LIFETIME - $49.99:
• One-time payment
• All features forever
• No recurring charges
```

---

## 🔗 RevenueCat Setup (Later)

After creating products in stores, you'll connect RevenueCat:

1. **Create RevenueCat account** (free): https://app.revenuecat.com/signup
2. **Create project:** "MyTackleBox"
3. **Connect App Store Connect:**
   - Upload API key
   - Select your app
4. **Connect Google Play:**
   - Upload service account JSON
   - Select your app
5. **Create Entitlement:**
   - Name: "pro"
   - Attach all 3 products
6. **Get API Keys:**
   - Copy iOS key (starts with `appl_`)
   - Copy Android key (starts with `goog_`)
7. **Update code:**
   - Replace placeholders in `subscriptionService.js`

---

## ⚠️ Important Notes

### Product IDs Must Match:
- Code: `fishing_lure_pro_monthly`
- App Store Connect: `fishing_lure_pro_monthly`
- Google Play: `fishing_lure_pro_monthly`
- RevenueCat: `fishing_lure_pro_monthly`

**They must be EXACTLY the same!**

### Pricing:
- Set prices in each store
- Prices can vary by country (stores handle conversion)
- You can change prices later (with notice to users)

### Free Trial (Optional):
- 7-day free trial is recommended
- Increases conversion rates
- Can be added later

---

## 📋 Pre-Submission Checklist

### App Store Connect:
- [ ] App listing created
- [ ] Subscription group created
- [ ] Monthly subscription created and submitted
- [ ] Yearly subscription created and submitted
- [ ] Lifetime purchase created and submitted
- [ ] All products approved by Apple

### Google Play Console:
- [ ] App listing created
- [ ] Monthly subscription created and active
- [ ] Yearly subscription created and active
- [ ] Lifetime product created and active

### Code:
- [ ] Product IDs match store products
- [ ] RevenueCat keys configured (when ready)
- [ ] Subscription service working
- [ ] Paywall screen implemented

### Legal:
- [ ] Terms of Service mentions subscriptions ✅ (already done)
- [ ] Privacy Policy mentions subscriptions ✅ (already done)
- [ ] Auto-renewal terms disclosed ✅ (in Terms of Service)

---

## 🎯 Timeline

**Before Building Apps:**
- Create app listings in both stores
- Create subscription products
- Wait for Apple approval (24-48 hours)

**After Products Approved:**
- Build production apps
- Connect RevenueCat
- Test subscriptions
- Submit apps for review

---

## 💡 Pro Tips

1. **Create products BEFORE building** - Makes testing easier
2. **Use same Product IDs** - Critical for RevenueCat
3. **Add free trial** - Increases conversions
4. **Test in sandbox** - Before going live
5. **Monitor RevenueCat** - Track subscriptions

---

**Ready to set up subscriptions?** Start with App Store Connect, then Google Play Console! 🚀

