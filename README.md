# 🎣 Fishing Lure Identifier App

AI-powered fishing lure identification app with cloud sync, subscription management, and catch tracking.

---

## 🚀 Features

- **AI Lure Identification** - GPT-4o Vision API analyzes lure photos
- **Cloud Sync** - Supabase backend for multi-device access
- **Subscriptions** - RevenueCat integration (iOS & Android)
- **Freemium Model** - 10 free scans/month, unlimited with PRO
- **Catch Tracking** - Log catches with photos and details
- **Favorites** - Mark and filter favorite lures
- **Offline Support** - Works without internet (local storage fallback)

---

## 📱 Tech Stack

### Mobile App
- **React Native** (Expo)
- **Supabase** - Auth, database, storage
- **RevenueCat** - Subscription management
- **React Navigation** - Navigation

### Backend
- **Flask** - Python web server
- **OpenAI API** - GPT-4o-mini for lure analysis
- **Supabase** - PostgreSQL database

---

## 🛠️ Setup

### Prerequisites
- Node.js 16+
- Python 3.8+
- Supabase account
- OpenAI API key

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd "Fishing Lure"

# Install backend dependencies
pip install -r requirements.txt

# Install mobile app dependencies
cd FishingLureApp
npm install
```

### 2. Configure Environment

Create `.env` file in the root directory:

```env
# OpenAI
OPENAI_API_KEY=your-openai-key

# Flask
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

See `env_template.txt` for full configuration options.

### 3. Set Up Supabase Database

Run these SQL files in Supabase SQL Editor (in order):

```sql
1. supabase_schema.sql              -- Main tables
2. supabase_subscriptions_schema.sql -- Subscription tracking
3. supabase_security_patch.sql       -- Security fixes
4. supabase_add_favorites.sql        -- Favorites feature
```

### 4. Run Backend

```bash
python app.py
# Server runs on http://localhost:5000
```

### 5. Run Mobile App

```bash
cd FishingLureApp
npx expo start

# Press 'a' for Android, 'i' for iOS
```

---

## 💰 Subscription Setup (For App Store Launch)

### 1. Developer Accounts
- **Apple Developer**: $99/year - https://developer.apple.com/programs/
- **Google Play Console**: $25 one-time - https://play.google.com/console/signup

### 2. RevenueCat Setup (FREE)
1. Sign up at https://app.revenuecat.com/signup
2. Create project
3. Get API keys for iOS and Android
4. Update `FishingLureApp/src/services/subscriptionService.js`:

```javascript
const REVENUECAT_API_KEY_IOS = 'your-ios-key';
const REVENUECAT_API_KEY_ANDROID = 'your-android-key';
```

### 3. Create Subscription Products

**Product IDs (same for both stores):**
- `fishing_lure_pro_monthly` - $4.99/month
- `fishing_lure_pro_yearly` - $39.99/year
- `fishing_lure_pro_lifetime` - $49.99 one-time

**iOS:** Create in App Store Connect → In-App Purchases
**Android:** Create in Google Play Console → Monetization → Subscriptions

### 4. Configure RevenueCat
1. Dashboard → Entitlements → Create "pro"
2. Attach all 3 products to "pro" entitlement
3. Connect Apple App Store & Google Play Store

**Full guide:** See `FishingLureApp/SUBSCRIPTION_SETUP.md`

---

## 📊 Pricing Model

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 10 scans/month, basic features |
| **PRO Monthly** | $4.99/mo | Unlimited scans, catches, advanced features |
| **PRO Yearly** | $39.99/yr | Save 33%, all PRO features |
| **Lifetime** | $49.99 | One-time, all features forever |

**Cost per scan:** ~$0.001 (GPT-4o-mini)
**Profit margin:** ~90% on PRO subscriptions

---

## 🗂️ Project Structure

```
Fishing Lure/
├── FishingLureApp/              # React Native mobile app
│   ├── src/
│   │   ├── screens/             # App screens
│   │   ├── services/            # API services
│   │   │   ├── subscriptionService.js   # RevenueCat
│   │   │   ├── supabaseService.js       # Database
│   │   │   └── storageService.js        # Local storage
│   │   └── contexts/            # React contexts
│   └── package.json
│
├── app.py                       # Flask backend
├── mobile_lure_classifier.py    # AI classification
├── supabase_client.py           # Supabase integration
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
│
├── supabase_*.sql               # Database schemas
└── templates/                   # HTML templates (web UI)
```

---

## 🔐 Security

- ✅ Row Level Security (RLS) enabled on all Supabase tables
- ✅ API keys stored in environment variables (never in code)
- ✅ Service role key used server-side only
- ✅ SQL injection protection (parameterized queries)
- ✅ Rate limiting on API endpoints
- ✅ Monthly budget caps for API costs

**Security patches applied:**
- Function search_path security
- Storage bucket policies
- View security_invoker settings

---

## 🧪 Testing

### Test Subscriptions

**iOS (Sandbox):**
1. Create sandbox tester in App Store Connect
2. Sign out of App Store on device
3. Run app and make test purchase
4. Sign in with sandbox account (no real charge)

**Android (Internal Testing):**
1. Add test accounts in Google Play Console
2. Upload internal test build
3. Install and test purchases

### Test Backend

```bash
# Run backend tests
python test_production.py

# Test Supabase connection
python test_supabase_connection.py
```

---

## 📱 Build & Deploy

### Mobile App (Expo EAS)

```bash
cd FishingLureApp

# Build for iOS
eas build --platform ios --profile production

# Build for Android
eas build --platform android --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

### Backend (Railway/Render)

**Environment Variables to Set:**
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `FLASK_HOST=0.0.0.0`
- `FLASK_PORT=5000`

---

## 🐛 Troubleshooting

### "Supabase credentials not found"
- Create `.env` file from `env_template.txt`
- Add your Supabase URL and keys

### "Failed to save to Supabase"
- Run all SQL schema files in Supabase SQL Editor
- Check Supabase service_role key is correct

### "No packages found" (RevenueCat)
- Verify subscription products created in App Store/Play Console
- Check products are attached to "pro" entitlement in RevenueCat
- Ensure products are "Ready to Submit" status

### App won't build
```bash
# Clear cache and rebuild
cd FishingLureApp
rm -rf node_modules
npm install
npx expo start -c
```

---

## 📊 Analytics & Monitoring

### Track via Supabase
```sql
-- Get subscription stats
SELECT * FROM subscription_stats;

-- Most scanned lure types
SELECT lure_type, COUNT(*) as scans
FROM lure_analyses
GROUP BY lure_type
ORDER BY scans DESC;

-- PRO conversion rate
SELECT 
  COUNT(*) FILTER (WHERE is_pro) * 100.0 / COUNT(*) as conversion_rate
FROM user_subscriptions;
```

### RevenueCat Dashboard
- Revenue charts
- Subscriber count
- Churn rate
- Trial conversions

---

## 🚀 Launch Checklist

- [ ] Developer accounts created (Apple + Google)
- [ ] RevenueCat configured
- [ ] Subscription products created
- [ ] Supabase database set up
- [ ] Backend deployed
- [ ] Mobile app built
- [ ] Test purchases verified
- [ ] Privacy policy created
- [ ] App Store screenshots ready
- [ ] Submit for review

---

## 💡 Tips

- **Start with Android** - Cheaper ($25 vs $99), faster approval
- **Use sandbox testing** - Test purchases thoroughly before launch
- **Monitor costs** - Set budget caps in `config.py`
- **Check logs** - Supabase Dashboard → Logs for errors
- **A/B test pricing** - Try different price points

---

## 📞 Support & Resources

- **RevenueCat Docs**: https://docs.revenuecat.com
- **Supabase Docs**: https://supabase.com/docs
- **Expo Docs**: https://docs.expo.dev
- **OpenAI API**: https://platform.openai.com/docs

---

## 📄 License

[Your License Here]

---

## 🤝 Contributing

[Your contribution guidelines]

---

**Built with ❤️ for fishermen everywhere** 🎣


