/**
 * Subscription Service - RevenueCat Integration
 * Handles all subscription logic for the Fishing Lure App
 */

import Purchases from 'react-native-purchases';
import { Platform, Linking } from 'react-native';
import { getCurrentUser } from './supabaseService';
import { supabase } from '../config/supabase';
import axios from 'axios';
import { BACKEND_URL } from './backendService'; // Use same backend URL

// ============================================================================
// CONFIGURATION
// ============================================================================

// RevenueCat API Keys
// Get these from: https://app.revenuecat.com/ → Project Settings → API Keys
// Test key for Expo Go (development)
const REVENUECAT_API_KEY_TEST = 'test_dUUNiOeOwXcEMWFAsvnVGrKkMvp';
// Production iOS key - Connected to App Store Connect (for production builds only)
const REVENUECAT_API_KEY_IOS_PRODUCTION = 'appl_pgNgDazBFRrUubpNYcmYQqCNvPh';
// Production Android key - Update when Google Play is set up
const REVENUECAT_API_KEY_ANDROID_PRODUCTION = 'test_dUUNiOeOwXcEMWFAsvnVGrKkMvp'; // Still using test key

// Determine which key to use based on environment
// In Expo Go, we must use test key. In production builds, use production keys.
const getApiKey = () => {
  // Check if we're in Expo Go (development environment)
  // Production keys don't work in Expo Go, so always use test key in development
  if (__DEV__) {
    return {
      ios: REVENUECAT_API_KEY_TEST,
      android: REVENUECAT_API_KEY_TEST,
    };
  }
  
  // In production builds, use production keys
  return {
    ios: REVENUECAT_API_KEY_IOS_PRODUCTION,
    android: REVENUECAT_API_KEY_ANDROID_PRODUCTION,
  };
};

// Product IDs (must match App Store Connect product identifiers exactly)
// Updated to match App Store Connect Product IDs
export const PRODUCT_IDS = {
  MONTHLY: 'monthly_pro',
  YEARLY: 'yearly_pro',
  LIFETIME: 'lifetime_pro',
};

// Entitlement ID (set in RevenueCat dashboard) - Must match RevenueCat identifier exactly!
const ENTITLEMENT_ID = 'MyTackleBox Pro'; // Updated to match RevenueCat dashboard

// Free tier limits
const FREE_TIER_LIMIT = 10; // scans per month

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize RevenueCat SDK
 * Call this when the app starts, after user authentication
 */
export const initializeSubscriptions = async (userId) => {
  try {
    const keys = getApiKey();
    const apiKey = Platform.OS === 'ios' 
      ? keys.ios 
      : keys.android;
    
    // Check if already configured to avoid re-initialization errors
    try {
      await Purchases.getCustomerInfo();
      if (__DEV__) {
        console.log('[Subscriptions] Already configured, skipping initialization');
      }
      return { success: true };
    } catch (notConfiguredError) {
      // Not configured yet, proceed with configuration
    }
    
    // Configure RevenueCat with user ID
    await Purchases.configure({ 
      apiKey, 
      appUserID: userId // Links purchases to your user
    });
    
    // Enable debug logs in development
    if (__DEV__) {
      Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG);
    }
    
    console.log('[Subscriptions] ✓ Initialized successfully');
    return { success: true };
  } catch (error) {
    console.error('[Subscriptions] ✗ Init error:', error);
    // Don't fail completely - subscription features will just use fallback
    return { success: false, error: error.message };
  }
};

// ============================================================================
// SUBSCRIPTION STATUS
// ============================================================================

/**
 * Refresh customer info from RevenueCat server
 * Forces a fresh fetch to get latest subscription data
 */
export const refreshCustomerInfo = async () => {
  try {
    // Restore purchases to force refresh from server
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo;
  } catch (error) {
    // If restore fails, try regular getCustomerInfo
    console.warn('[Subscriptions] Restore failed, using getCustomerInfo:', error);
    return await Purchases.getCustomerInfo();
  }
};

/**
 * Get current subscription status
 * Returns whether user has PRO access and details
 * Prioritizes recurring subscriptions (monthly/yearly) over lifetime when both exist
 */
export const getSubscriptionStatus = async (forceRefresh = false) => {
  try {
    // Check if RevenueCat is configured
    let customerInfo;
    if (forceRefresh) {
      customerInfo = await refreshCustomerInfo();
    } else {
      customerInfo = await Purchases.getCustomerInfo();
    }
    
    // Check if user has active PRO entitlement
    const isPro = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    
    // Get all purchased product identifiers to see what user has
    const allPurchasedProducts = customerInfo.allPurchasedProductIdentifiers || [];
    
    // Check active subscriptions (recurring subscriptions that are currently active)
    const activeSubscriptions = customerInfo.activeSubscriptions || {};
    
    if (__DEV__) {
      console.log('[Subscriptions] All purchased products:', allPurchasedProducts);
      console.log('[Subscriptions] Active subscriptions:', Object.keys(activeSubscriptions));
      console.log('[Subscriptions] Active entitlements:', Object.keys(customerInfo.entitlements.active));
    }
    
    // Check if user has an active recurring subscription (monthly or yearly)
    const hasActiveMonthly = activeSubscriptions[PRODUCT_IDS.MONTHLY] !== undefined;
    const hasActiveYearly = activeSubscriptions[PRODUCT_IDS.YEARLY] !== undefined;
    const hasLifetime = allPurchasedProducts.includes(PRODUCT_IDS.LIFETIME);
    
    // Get the entitlement object (RevenueCat returns one entitlement, might be lifetime)
    let entitlement = customerInfo.entitlements.active[ENTITLEMENT_ID];
    
    // If user has an active recurring subscription AND lifetime, prioritize the recurring one
    // This shows what they're currently paying for, not just what grants access
    if (entitlement && (hasActiveMonthly || hasActiveYearly)) {
      // Check if the active subscription is actually granting the entitlement
      // If monthly/yearly is active, use that product identifier even if entitlement shows lifetime
      if (hasActiveMonthly) {
        // Create a synthetic entitlement object for monthly
        const monthlySubscription = activeSubscriptions[PRODUCT_IDS.MONTHLY];
        entitlement = {
          productIdentifier: PRODUCT_IDS.MONTHLY,
          willRenew: true,
          expirationDate: monthlySubscription.expirationDate || null,
          periodType: 'MONTH',
        };
        if (__DEV__) {
          console.log('[Subscriptions] Overriding with active monthly subscription');
        }
      } else if (hasActiveYearly) {
        // Create a synthetic entitlement object for yearly
        const yearlySubscription = activeSubscriptions[PRODUCT_IDS.YEARLY];
        entitlement = {
          productIdentifier: PRODUCT_IDS.YEARLY,
          willRenew: true,
          expirationDate: yearlySubscription.expirationDate || null,
          periodType: 'YEAR',
        };
        if (__DEV__) {
          console.log('[Subscriptions] Overriding with active yearly subscription');
        }
      }
    }
    
    if (__DEV__) {
      console.log('[Subscriptions] Final entitlement:', {
        isPro,
        productIdentifier: entitlement?.productIdentifier,
        willRenew: entitlement?.willRenew,
        expirationDate: entitlement?.expirationDate,
        hasActiveMonthly,
        hasActiveYearly,
        hasLifetime,
      });
    }
    
    // Check if it's a lifetime purchase
    const isLifetime = entitlement?.willRenew === false && 
                       entitlement?.productIdentifier === PRODUCT_IDS.LIFETIME;
    
    return {
      isPro,
      isLifetime,
      expirationDate: entitlement?.expirationDate || null,
      productIdentifier: entitlement?.productIdentifier || null,
      willRenew: entitlement?.willRenew || false,
      periodType: entitlement?.periodType || null,
    };
  } catch (error) {
    // If RevenueCat not configured yet, check backend API instead
    console.warn('[Subscriptions] RevenueCat not configured, checking backend');
    
    try {
      const user = await getCurrentUser();
      if (!user) {
        return { isPro: false, isLifetime: false };
      }
      
      // Use backend API to check subscription status
      const response = await axios.get(`${BACKEND_URL}/api/verify-subscription`, {
        params: { user_id: user.id },
        timeout: 5000,
      });
      
      const subscription = response.data;
      
      return {
        isPro: subscription.is_pro || false,
        isLifetime: subscription.subscription_type === 'lifetime',
        productIdentifier: subscription.product_identifier,
        expirationDate: subscription.expires_at,
      };
    } catch (fallbackError) {
      console.warn('[Subscriptions] Backend check failed, assuming free tier');
      return { isPro: false, isLifetime: false };
    }
  }
};

/**
 * Check if user is PRO (simple boolean check)
 */
export const isUserPro = async () => {
  const status = await getSubscriptionStatus();
  return status.isPro;
};

// ============================================================================
// OFFERINGS & PACKAGES
// ============================================================================

/**
 * Get available subscription packages
 * Returns packages configured in RevenueCat dashboard
 */
export const getSubscriptionPackages = async () => {
  try {
    const offerings = await Purchases.getOfferings();
    
    if (offerings.current !== null && offerings.current.availablePackages.length > 0) {
      return {
        success: true,
        packages: offerings.current.availablePackages,
        current: offerings.current,
      };
    } else {
      console.warn('[Subscriptions] No offerings found');
      return {
        success: false,
        packages: [],
        error: 'No subscription packages available'
      };
    }
  } catch (error) {
    console.error('[Subscriptions] Get packages error:', error);
    return {
      success: false,
      packages: [],
      error: error.message
    };
  }
};

// ============================================================================
// PURCHASE FLOW
// ============================================================================

/**
 * Purchase a subscription package
 */
export const purchaseSubscription = async (packageToPurchase) => {
  try {
    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
    
    const isPro = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    
    if (isPro) {
      // Sync subscription status to Supabase
      await syncSubscriptionToSupabase(customerInfo);
      
      console.log('[Subscriptions] ✓ Purchase successful');
      return { 
        success: true, 
        isPro: true,
        productId: packageToPurchase.product.identifier
      };
    } else {
      return { 
        success: false, 
        error: 'Purchase did not grant PRO access' 
      };
    }
  } catch (error) {
    if (error.userCancelled) {
      console.log('[Subscriptions] User cancelled purchase');
      return { 
        success: false, 
        cancelled: true 
      };
    } else {
      console.error('[Subscriptions] Purchase error:', error);
      return { 
        success: false, 
        error: error.message 
      };
    }
  }
};

/**
 * Restore previous purchases
 * Important for users who reinstall the app or switch devices
 */
export const restorePurchases = async () => {
  try {
    const customerInfo = await Purchases.restorePurchases();
    const isPro = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    
    if (isPro) {
      await syncSubscriptionToSupabase(customerInfo);
      console.log('[Subscriptions] ✓ Purchases restored');
    }
    
    return { 
      success: true, 
      isPro,
      message: isPro ? 'PRO subscription restored!' : 'No purchases to restore'
    };
  } catch (error) {
    console.error('[Subscriptions] Restore error:', error);
    return { 
      success: false, 
      error: error.message 
    };
  }
};

// ============================================================================
// QUOTA MANAGEMENT (FREE TIER)
// ============================================================================

/**
 * Check if user can scan a lure
 * Respects PRO status and free tier quotas
 */
export const canUserScan = async () => {
  try {
    // Check PRO status first
    const status = await getSubscriptionStatus();
    
    // PRO users have unlimited scans
    if (status.isPro) {
      return { 
        canScan: true, 
        reason: 'pro',
        unlimited: true 
      };
    }
    
    // Free users: check monthly quota
    const quota = await getMonthlyQuota();
    
    if (quota.remaining > 0) {
      return { 
        canScan: true, 
        reason: 'free_quota',
        remaining: quota.remaining,
        used: quota.used,
        limit: quota.limit,
        resetDate: quota.resetDate
      };
    }
    
    // Quota exceeded
    return { 
      canScan: false, 
      reason: 'quota_exceeded',
      resetDate: quota.resetDate,
      used: quota.used,
      limit: quota.limit
    };
  } catch (error) {
    console.error('[Subscriptions] Can scan check error:', error);
    return { 
      canScan: false, 
      reason: 'error',
      error: error.message 
    };
  }
};

/**
 * Get monthly quota status for free users
 */
export const getMonthlyQuota = async () => {
  try {
    const user = await getCurrentUser();
    if (!user) {
      console.warn('[Subscriptions] No user authenticated');
      return { 
        used: 0, 
        remaining: FREE_TIER_LIMIT, 
        limit: FREE_TIER_LIMIT,
        resetDate: new Date().toISOString()
      };
    }
    
    // Use backend API to check quota (more reliable than direct Supabase query)
    try {
      const response = await axios.get(`${BACKEND_URL}/api/check-scan-quota`, {
        params: { user_id: user.id },
        timeout: 5000,
      });
      
      const quota = response.data;
      
      if (quota.is_pro || quota.unlimited) {
        // PRO user
        return {
          used: 0,
          remaining: 999,
          limit: 999,
          resetDate: null,
          isPro: true,
        };
      }
      
      // Free user - calculate remaining from used and limit
      const now = new Date();
      const resetDate = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      
      const used = quota.used || 0;
      const limit = quota.limit || FREE_TIER_LIMIT;
      const remaining = Math.max(0, limit - used); // Calculate remaining properly
      
      console.log(`[Subscriptions] Quota from backend: ${used}/${limit} used, ${remaining} remaining`);
      
      return {
        used,
        remaining,
        limit,
        resetDate: quota.reset_date || resetDate.toISOString(),
      };
    } catch (backendError) {
      console.warn('[Subscriptions] Backend quota check failed, returning defaults:', backendError.message);
      // Return safe defaults if backend is unreachable
      return {
        used: 0,
        remaining: FREE_TIER_LIMIT,
        limit: FREE_TIER_LIMIT,
        resetDate: new Date().toISOString()
      };
    }
  } catch (error) {
    console.error('[Subscriptions] Quota check error:', error);
    // Return safe defaults on error
    return { 
      used: 0, 
      remaining: FREE_TIER_LIMIT, 
      limit: FREE_TIER_LIMIT,
      resetDate: new Date().toISOString()
    };
  }
};

/**
 * Get quota status for display in UI
 */
export const getQuotaStatus = async () => {
  try {
    const status = await getSubscriptionStatus();
    
    if (status.isPro) {
      return {
        isPro: true,
        unlimited: true,
        message: '∞ Unlimited scans',
        emoji: '🎣'
      };
    }
    
    const quota = await getMonthlyQuota();
    
    // Debug logging
    console.log('[Subscriptions] getQuotaStatus - quota data:', quota);
    
    const resetDate = new Date(quota.resetDate);
    const daysUntilReset = Math.ceil((resetDate - new Date()) / (1000 * 60 * 60 * 24));
    
    return {
      isPro: false,
      unlimited: false,
      used: quota.used,
      remaining: quota.remaining,
      limit: quota.limit,
      resetDate: quota.resetDate,
      daysUntilReset,
      message: `${quota.remaining} scan${quota.remaining !== 1 ? 's' : ''} remaining`,
      subtitle: `Resets in ${daysUntilReset} day${daysUntilReset !== 1 ? 's' : ''}`,
      emoji: quota.remaining > 5 ? '✅' : quota.remaining > 0 ? '⚠️' : '🚫'
    };
  } catch (error) {
    console.error('[Subscriptions] getQuotaStatus error:', error);
    // Return safe error state
    return {
      isPro: false,
      unlimited: false,
      used: 0,
      remaining: 0,
      limit: FREE_TIER_LIMIT,
      message: '⚠️ Could not load quota',
      subtitle: 'Please check your connection',
      emoji: '⚠️'
    };
  }
};

// ============================================================================
// SUPABASE SYNC
// ============================================================================

/**
 * Sync subscription status to Supabase
 * This allows backend to validate subscription status
 */
const syncSubscriptionToSupabase = async (customerInfo) => {
  try {
    const isPro = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    const entitlement = customerInfo.entitlements.active[ENTITLEMENT_ID];
    
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
      console.warn('[Subscriptions] No user found, skipping Supabase sync');
      return;
    }
    
    // Determine subscription type
    let subscriptionType = null;
    if (entitlement) {
      const productId = entitlement.productIdentifier;
      if (productId === PRODUCT_IDS.MONTHLY) {
        subscriptionType = 'monthly';
      } else if (productId === PRODUCT_IDS.YEARLY) {
        subscriptionType = 'yearly';
      } else if (productId === PRODUCT_IDS.LIFETIME) {
        subscriptionType = 'lifetime';
      }
    }
    
    // Upsert subscription status
    const { error } = await supabase
      .from('user_subscriptions')
      .upsert({
        user_id: user.id,
        is_pro: isPro,
        subscription_type: subscriptionType,
        product_identifier: entitlement?.productIdentifier || null,
        expires_at: entitlement?.expirationDate || null,
        will_renew: entitlement?.willRenew || false,
        updated_at: new Date().toISOString(),
      }, {
        onConflict: 'user_id'
      });
    
    if (error) throw error;
    
    console.log('[Subscriptions] ✓ Synced to Supabase');
  } catch (error) {
    console.error('[Subscriptions] Sync to Supabase error:', error);
    // Don't throw - subscription still works even if sync fails
  }
};

/**
 * Manually sync subscription status
 * Useful for debugging or forcing a refresh
 */
export const syncSubscription = async () => {
  try {
    // Check if RevenueCat is configured before trying to use it
    try {
      await Purchases.getCustomerInfo();
    } catch (notConfiguredError) {
      if (__DEV__) {
        console.warn('[Subscriptions] RevenueCat not configured yet, skipping sync');
      }
      return { success: false, error: 'RevenueCat not configured' };
    }
    
    const customerInfo = await Purchases.getCustomerInfo();
    await syncSubscriptionToSupabase(customerInfo);
    return { success: true };
  } catch (error) {
    if (__DEV__) {
      console.error('[Subscriptions] Manual sync error:', error);
    }
    return { success: false, error: error.message };
  }
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get subscription info for display
 */
export const getSubscriptionInfo = async (forceRefresh = false) => {
  const status = await getSubscriptionStatus(forceRefresh);
  
  if (!status.isPro) {
    return {
      isPro: false,
      title: 'Free Plan',
      description: '10 scans per month',
    };
  }
  
  const productId = status.productIdentifier;
  
  if (productId === PRODUCT_IDS.LIFETIME) {
    return {
      isPro: true,
      title: 'Lifetime PRO',
      description: 'Unlimited access forever',
      badge: 'Lifetime',
    };
  }
  
  if (productId === PRODUCT_IDS.YEARLY) {
    return {
      isPro: true,
      title: 'PRO (Yearly)',
      description: 'Billed annually',
      expiresAt: status.expirationDate,
      willRenew: status.willRenew,
      badge: 'PRO',
    };
  }
  
  if (productId === PRODUCT_IDS.MONTHLY) {
    return {
      isPro: true,
      title: 'PRO (Monthly)',
      description: 'Billed monthly',
      expiresAt: status.expirationDate,
      willRenew: status.willRenew,
      badge: 'PRO',
    };
  }
  
  return {
    isPro: true,
    title: 'PRO',
    description: 'Active subscription',
    badge: 'PRO',
  };
};

/**
 * Open subscription management in App Store/Play Store
 * This allows users to cancel or manage their subscriptions
 */
export const openSubscriptionManagement = async () => {
  try {
    if (Platform.OS === 'ios') {
      // iOS: Open App Store subscription management
      const url = 'https://apps.apple.com/account/subscriptions';
      const canOpen = await Linking.canOpenURL(url);
      if (canOpen) {
        await Linking.openURL(url);
        return { success: true };
      } else {
        return { success: false, error: 'Cannot open App Store' };
      }
    } else if (Platform.OS === 'android') {
      // Android: Open Play Store subscription management
      const url = 'https://play.google.com/store/account/subscriptions';
      const canOpen = await Linking.canOpenURL(url);
      if (canOpen) {
        await Linking.openURL(url);
        return { success: true };
      } else {
        // Try opening Play Store app directly
        const playStoreUrl = 'market://details?id=com.google.android.gms';
        try {
          await Linking.openURL(playStoreUrl);
          return { success: true };
        } catch {
          return { success: false, error: 'Cannot open Play Store' };
        }
      }
    }
    return { success: false, error: 'Platform not supported' };
  } catch (error) {
    console.error('[Subscriptions] Error opening subscription management:', error);
    return { success: false, error: error.message };
  }
};

/**
 * Check if subscription is about to expire
 * Returns true if expiring in next 7 days
 */
export const isSubscriptionExpiringSoon = async () => {
  const status = await getSubscriptionStatus();
  
  if (!status.isPro || !status.expirationDate || status.isLifetime) {
    return false;
  }
  
  const expirationDate = new Date(status.expirationDate);
  const now = new Date();
  const daysUntilExpiration = Math.ceil((expirationDate - now) / (1000 * 60 * 60 * 24));
  
  return daysUntilExpiration <= 7 && daysUntilExpiration > 0;
};

// ============================================================================
// EXPORTS
// ============================================================================

export default {
  // Initialization
  initializeSubscriptions,
  
  // Status
  getSubscriptionStatus,
  isUserPro,
  getSubscriptionInfo,
  isSubscriptionExpiringSoon,
  
  // Packages
  getSubscriptionPackages,
  
  // Purchase
  purchaseSubscription,
  restorePurchases,
  
  // Quota
  canUserScan,
  getMonthlyQuota,
  getQuotaStatus,
  
  // Sync
  syncSubscription,
  
  // Constants
  PRODUCT_IDS,
  FREE_TIER_LIMIT,
};

