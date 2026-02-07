# App Store Connect Setup – My Tackle Box

Use this to set up (or finish) your app in App Store Connect. Order matters: do **In-App Purchases** first so they’re ready before you submit a build.

---

## 1. In-App Purchases (subscriptions)

Product IDs **must** match RevenueCat: `monthly_pro`, `yearly_pro`, `lifetime_pro`.

1. In App Store Connect go to **My Apps** → **My Tackle Box** → **Features** → **In-App Purchases**.
2. Click **+** to add in-app purchases.

### Subscription group

- Create (or use existing) **Subscription Group**: e.g. **My Tackle Box Subscriptions**.

### Add three subscriptions

For each, **Reference Name** is for you; **Product ID** is what the app and RevenueCat use (must match exactly).

| Reference Name              | Product ID   | Type        |
|-----------------------------|-------------|-------------|
| Monthly Pro Subscription    | `monthly_pro`   | Auto-Renewable |
| Yearly Pro Subscription     | `yearly_pro`    | Auto-Renewable |
| Lifetime Pro Access         | `lifetime_pro`  | Non-Consumable* or Auto-Renewable (see below) |

\* For a true “lifetime” one-time purchase, use **Non-Consumable** if your app supports it; otherwise use a long auto-renewable (e.g. 1 year) and treat it as “lifetime” in the app.

For each subscription:

- **Subscription Duration**: Monthly → 1 month, Yearly → 1 year.
- **Price**: Choose your price (e.g. $9.99 monthly, $79.99 yearly, $99.99 lifetime).
- **Display Name** (what users see): e.g. “Monthly Pro”, “Yearly Pro”, “Lifetime Pro Access”.
- **Description**: Short line describing the plan.
- Submit for review with the app (or when ready).

---

## 2. App information (App Store tab)

**My Apps** → **My Tackle Box** → **App Store** (left) → select **English (U.S.)**.

| Field | Value |
|-------|--------|
| **Name** | My Tackle Box |
| **Subtitle** (30 chars) | AI Lure ID & Catch Tracker |
| **Promotional Text** (170 chars, optional) | The ultimate fishing companion! Identify any lure with AI, track your catches, and organize your tackle box. |
| **Keywords** (100 chars, comma-separated) | fishing,lure,bass,tackle,fish,identify,catalog,catch,angler,bait,tacklebox |
| **Support URL** | https://ericfernandes71.github.io/fishing-lure-classifier/ |
| **Marketing URL** | (optional) |
| **Privacy Policy URL** | https://ericfernandes71.github.io/fishing-lure-classifier/PRIVACY_POLICY.html |

**Description** (4000 chars): Use the full text from `APP_STORE_LISTING_SETUP_GUIDE.md` or `APP_STORE_ASSETS_MYTACKLEBOX.md` (the long description with features, free tier, PRO monthly/yearly/lifetime, support email, legal links).

---

## 3. Screenshots

- **iPhone 6.7"** (1290 x 2796 px): **Required** – at least 3–8 screenshots.
- **iPhone 6.5"** (1242 x 2688 px): Recommended.

Ideas: Home/scan, analysis result, tackle box, catch tracking, lure detail, subscription/paywall.

---

## 4. Version and build

- **Version**: e.g. 1.0.0 (must be higher than any previously submitted).
- **What’s New**: Short “What’s New in This Version” (e.g. initial release or your current changes).
- **Build**: After you upload a build (via EAS Submit or Xcode), choose that build here. You can’t submit until a build is selected.

---

## 5. Review information

- **Contact**: First name, last name, phone, email (e.g. mytackleboxapp@gmail.com).
- **Demo account**: If the app requires login, provide a test account and password for Apple.
- **Notes**: Anything that helps reviewers (e.g. “Subscription can be tested with Sandbox account”).

---

## 6. App Privacy

- Ensure **App Privacy** is filled (e.g. data types: Photos, User Content, Identifiers, Purchases) as required for your app.

---

## 7. Pricing and availability

- **Price**: **Free** (with in-app purchases).
- **Availability**: All countries (or your chosen territories).

---

## Quick checklist

- [ ] Subscription group created
- [ ] Three products added: `monthly_pro`, `yearly_pro`, `lifetime_pro` (names/prices set)
- [ ] App info filled: name, subtitle, description, keywords, Support URL, Privacy Policy URL
- [ ] Screenshots uploaded (at least for 6.7" iPhone)
- [ ] Version number and “What’s New” set
- [ ] Build selected (after you upload via EAS Submit)
- [ ] Review contact and demo account (if needed) set
- [ ] Pricing: Free; availability set

---

**More detail:**  
- Full description and copy: `APP_STORE_LISTING_SETUP_GUIDE.md`, `APP_STORE_ASSETS_MYTACKLEBOX.md`  
- Build and submit: `FishingLureApp/APPLE_STORE_LAUNCH_CHECKLIST.md`
