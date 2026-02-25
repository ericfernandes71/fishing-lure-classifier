# Canada-only launch & testing with friends

Use this to limit the app to Canada, lock in pricing, and invite friends to test.

---

## 1. Make the app available only in Canada

**In App Store Connect:**

1. Go to **My Apps** → **My Tackle Box**.
2. Open the **Pricing and Availability** section (left sidebar or from the app’s version page).
3. Under **Availability**, click **Edit** (or “Manage availability”).
4. Choose **Select specific countries and regions** (not “Make this app available in all territories”).
5. **Deselect all**, then select only **Canada**. Save.

Your app will then be visible and downloadable only in Canada. You can add more countries later.

**Subscriptions:**  
Each in-app purchase (monthly, yearly, lifetime) also has its own **Availability**. In **Subscriptions** → each product → **Availability**, set the same: Canada only (or match the app).

---

## 2. Pricing (where to set it)

**Actual prices are set in App Store Connect**, not in the app code. The app shows whatever price the store returns.

- **App Store Connect** → **My Tackle Box** → **Subscriptions** (or **In-App Purchases**).
- Open each subscription: **Monthly Pro**, **Yearly Pro**, **Lifetime Pro**.
- Under **Subscription Prices** (or **Pricing**), add a price for **Canada** (e.g. CAD) and save.

**Reference (you can choose your own):**

| Plan     | Example (USD) | Example (CAD) |
|----------|----------------|----------------|
| Monthly  | $4.99/mo       | ~$6.99 CAD     |
| Yearly   | $39.99/yr      | ~$54.99 CAD    |
| Lifetime | $49.99 or $99.99 one-time | Your choice |

Your repo has different numbers in different places (e.g. $4.99 vs $9.99 monthly). Pick one set, set those prices in App Store Connect for Canada, and optionally update:

- **TERMS_OF_SERVICE.md** (and any other legal/marketing copy) so they match.
- **App Store description** in App Store Connect so the listed prices match.

The in-app paywall will show the prices from the store for the user’s region (e.g. CAD in Canada).

---

## 3. Testing with friends (TestFlight)

**Option A – Public link (easiest)**  
1. **App Store Connect** → **My Tackle Box** → **TestFlight** tab.  
2. With a build uploaded, open the build and enable **Public Link** (if you want a link anyone can use).  
3. Share that link with friends. They install **TestFlight** from the App Store, open the link, and install your app.  
4. They can use the app like a normal install (no Apple ID needed for the link, unless you restrict to a list).

**Option B – Internal / external testers**  
1. **TestFlight** → **Internal Testing** or **External Testing**.  
2. Add testers by **email** (Apple ID).  
3. They get an email invite; they accept in TestFlight and install the build.  

**Notes:**

- **Internal testers:** Up to 100, no review; instant. Good for close friends.  
- **External testers:** Up to 10,000; first build per version needs a quick Apple review. Good for broader friends list.  
- **Canada only:** TestFlight availability is separate from store availability. Your test build can be installed by testers in any country you invite; **store availability (Canada only)** only affects who can download the app once it’s **released** on the App Store.

So: invite friends as TestFlight testers (any country). When you release, only users in Canada will see and download the app.

---

## Quick checklist

- [ ] **Availability:** App + subscriptions set to **Canada only** in App Store Connect.
- [ ] **Pricing:** Canada (CAD) prices set for each subscription in App Store Connect; legal/description text updated if you want them to match.
- [ ] **TestFlight:** Build uploaded; friends invited via Public Link or by email (Internal/External testers).

After that you can test with friends and launch only in Canada.
