/**
 * Subscription Service - RevenueCat Integration
 * Handles all subscription logic for the Fishing Lure App
 */

import Purchases from 'react-native-purchases';
import { Platform } from 'react-native';
import { supabase } from './supabaseService';

// ============================================================================
// CONFIGURATION
// ============================================================================

// RevenueCat API Keys
// Get these from: https://app.revenuecat.com/
const REVENUECAT_API_KEY_IOS = 'appl_YOUR_IOS_KEY_HERE';
const REVENUECAT_API_KEY_ANDROID = 'goog_YOUR_ANDROID_KEY_HERE';

// Product IDs (must match App Store Connect / Google Play Console)
export const PRODUCT_IDS = {
  MONTHLY: 'fishing_lure_pro_monthly',
  YEARLY: 'fishing_lure_pro_yearly',
  LIFETIME: 'fishing_lure_lifetime',
};

// Entitlement ID (set in RevenueCat dashboard)
const ENTITLEMENT_ID = 'pro';

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
    const apiKey = Platform.OS === 'ios' 
      ? REVENUECAT_API_KEY_IOS 
      : REVENUECAT_API_KEY_ANDROID;
    
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
    return { success: false, error: error.message };
  }
};

// ============================================================================
// SUBSCRIPTION STATUS
// ============================================================================

/**
 * Get current subscription status
 * Returns whether user has PRO access and details
 */
export const getSubscriptionStatus = async () => {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    
    // Check if user has active PRO entitlement
    const isPro = customerInfo.entitlements.active[ENTITLEMENT_ID] !== undefined;
    const entitlement = customerInfo.entitlements.active[ENTITLEMENT_ID];
    
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
    console.error('[Subscriptions] Get status error:', error);
    return { 
      isPro: false, 
      isLifetime: false,
      error: error.message 
    };
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
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) throw new Error('Not authenticated');
    
    // Calculate start of current month
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    
    // Get scans this month from Supabase
    const { data, error } = await supabase
      .from('lure_analyses')
      .select('id')
      .eq('user_id', user.id)
      .gte('created_at', startOfMonth.toISOString());
    
    if (error) throw error;
    
    const used = data?.length || 0;
    const remaining = Math.max(0, FREE_TIER_LIMIT - used);
    
    // Calculate reset date (first day of next month)
    const resetDate = new Date(now.getFullYear(), now.getMonth() + 1, 1);
    
    return { 
      used, 
      remaining, 
      limit: FREE_TIER_LIMIT, 
      resetDate: resetDate.toISOString()
    };
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
    const customerInfo = await Purchases.getCustomerInfo();
    await syncSubscriptionToSupabase(customerInfo);
    return { success: true };
  } catch (error) {
    console.error('[Subscriptions] Manual sync error:', error);
    return { success: false, error: error.message };
  }
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get subscription info for display
 */
export const getSubscriptionInfo = async () => {
  const status = await getSubscriptionStatus();
  
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
      badge: '⭐ Lifetime',
    };
  }
  
  if (productId === PRODUCT_IDS.YEARLY) {
    return {
      isPro: true,
      title: 'PRO (Yearly)',
      description: 'Billed annually',
      expiresAt: status.expirationDate,
      willRenew: status.willRenew,
      badge: '💎 PRO',
    };
  }
  
  if (productId === PRODUCT_IDS.MONTHLY) {
    return {
      isPro: true,
      title: 'PRO (Monthly)',
      description: 'Billed monthly',
      expiresAt: status.expirationDate,
      willRenew: status.willRenew,
      badge: '💎 PRO',
    };
  }
  
  return {
    isPro: true,
    title: 'PRO',
    description: 'Active subscription',
    badge: '💎 PRO',
  };
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

