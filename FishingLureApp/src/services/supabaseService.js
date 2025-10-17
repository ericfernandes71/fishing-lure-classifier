/**
 * Supabase Service - Authentication and Data Management
 */

import { supabase } from '../config/supabase';

// ============================================================================
// AUTHENTICATION
// ============================================================================

/**
 * Sign up new user
 */
export const signUp = async (email, password, fullName) => {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
        },
      },
    });

    if (error) throw error;
    return { success: true, user: data.user };
  } catch (error) {
    console.error('[Supabase] Sign up error:', error);
    throw new Error(error.message || 'Failed to sign up');
  }
};

/**
 * Sign in user
 */
export const signIn = async (email, password) => {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw error;
    return { success: true, user: data.user, session: data.session };
  } catch (error) {
    console.error('[Supabase] Sign in error:', error);
    throw new Error(error.message || 'Failed to sign in');
  }
};

/**
 * Sign out user
 */
export const signOut = async () => {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('[Supabase] Sign out error:', error);
    throw new Error(error.message || 'Failed to sign out');
  }
};

/**
 * Get current user
 */
export const getCurrentUser = async () => {
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    return user;
  } catch (error) {
    console.error('[Supabase] Get user error:', error);
    return null;
  }
};

/**
 * Get current session
 */
export const getCurrentSession = async () => {
  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error) throw error;
    return session;
  } catch (error) {
    console.error('[Supabase] Get session error:', error);
    return null;
  }
};

/**
 * Reset password
 */
export const resetPassword = async (email) => {
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('[Supabase] Password reset error:', error);
    throw new Error(error.message || 'Failed to reset password');
  }
};

// ============================================================================
// USER PROFILE
// ============================================================================

/**
 * Get user profile
 */
export const getUserProfile = async (userId) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', userId)
      .single();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error('[Supabase] Get profile error:', error);
    return null;
  }
};

/**
 * Update user profile
 */
export const updateUserProfile = async (userId, updates) => {
  try {
    const { data, error } = await supabase
      .from('profiles')
      .update(updates)
      .eq('id', userId)
      .select()
      .single();

    if (error) throw error;
    return { success: true, profile: data };
  } catch (error) {
    console.error('[Supabase] Update profile error:', error);
    throw new Error(error.message || 'Failed to update profile');
  }
};

// ============================================================================
// LURE ANALYSES
// ============================================================================

/**
 * Save lure analysis to Supabase
 */
export const saveLureAnalysis = async (analysisData) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { data, error } = await supabase
      .from('lure_analyses')
      .insert([{
        user_id: user.id,
        lure_type: analysisData.lure_type,
        confidence: analysisData.confidence,
        image_url: analysisData.image_url,
        image_name: analysisData.image_name,
        image_path: analysisData.image_path,
        analysis_method: analysisData.analysis_method || 'ChatGPT Vision API',
        chatgpt_analysis: analysisData.chatgpt_analysis || {},
        lure_details: analysisData.lure_details || {},
        api_cost_usd: analysisData.api_cost_usd,
        tokens_used: analysisData.tokens_used,
      }])
      .select()
      .single();

    if (error) throw error;
    return { success: true, analysis: data };
  } catch (error) {
    console.error('[Supabase] Save analysis error:', error);
    throw new Error(error.message || 'Failed to save lure analysis');
  }
};

/**
 * Get all lure analyses for current user (Tackle Box)
 * Includes catch count for each lure
 */
export const getUserLureAnalyses = async () => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    // Get all lure analyses
    const { data: lures, error } = await supabase
      .from('lure_analyses')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (error) throw error;

    // Get catch counts for all lures
    if (lures && lures.length > 0) {
      // Query catches and group by lure_analysis_id
      const { data: catchCounts, error: catchError } = await supabase
        .from('catches')
        .select('lure_analysis_id')
        .eq('user_id', user.id);

      if (!catchError && catchCounts) {
        // Count catches per lure
        const countMap = {};
        catchCounts.forEach(c => {
          countMap[c.lure_analysis_id] = (countMap[c.lure_analysis_id] || 0) + 1;
        });

        // Add catchCount to each lure
        lures.forEach(lure => {
          lure.catchCount = countMap[lure.id] || 0;
        });
      }
    }

    return lures || [];
  } catch (error) {
    console.error('[Supabase] Get analyses error:', error);
    throw new Error(error.message || 'Failed to load tackle box');
  }
};

/**
 * Get single lure analysis by ID
 */
export const getLureAnalysisById = async (analysisId) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { data, error } = await supabase
      .from('lure_analyses')
      .select('*')
      .eq('id', analysisId)
      .eq('user_id', user.id)
      .single();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error('[Supabase] Get analysis error:', error);
    throw new Error(error.message || 'Failed to load lure details');
  }
};

/**
 * Delete lure analysis
 */
export const deleteLureAnalysis = async (analysisId) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { error } = await supabase
      .from('lure_analyses')
      .delete()
      .eq('id', analysisId)
      .eq('user_id', user.id);

    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('[Supabase] Delete analysis error:', error);
    throw new Error(error.message || 'Failed to delete lure');
  }
};

/**
 * Bulk delete lure analyses
 */
export const bulkDeleteLureAnalyses = async (analysisIds) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { error } = await supabase
      .from('lure_analyses')
      .delete()
      .in('id', analysisIds)
      .eq('user_id', user.id);

    if (error) throw error;
    return { success: true, deleted_count: analysisIds.length };
  } catch (error) {
    console.error('[Supabase] Bulk delete error:', error);
    throw new Error(error.message || 'Failed to delete lures');
  }
};

// ============================================================================
// STORAGE (Lure Images)
// ============================================================================

/**
 * Upload lure image to Supabase Storage
 */
export const uploadLureImage = async (imageUri, fileName) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    // Create file path with user ID folder
    const filePath = `${user.id}/${fileName}`;

    // Read file as base64 and convert to ArrayBuffer
    const base64Response = await fetch(imageUri);
    const base64Data = await base64Response.text();
    
    // If it's a data URI, extract the base64 part
    let base64String = base64Data;
    if (base64Data.startsWith('data:')) {
      base64String = base64Data.split(',')[1];
    } else {
      // Not base64, read as arrayBuffer instead
      const arrayBufferResponse = await fetch(imageUri);
      const arrayBuffer = await arrayBufferResponse.arrayBuffer();
      
      // Upload ArrayBuffer to Supabase Storage
      const { data, error } = await supabase.storage
        .from('lure-images')
        .upload(filePath, arrayBuffer, {
          contentType: 'image/jpeg',
          upsert: false,
        });

      if (error) throw error;

      // Get public URL
      const { data: urlData } = supabase.storage
        .from('lure-images')
        .getPublicUrl(filePath);

      return { success: true, path: data.path, url: urlData.publicUrl };
    }
    
    // Convert base64 to ArrayBuffer
    const binaryString = atob(base64String);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Upload to Supabase Storage
    const { data, error } = await supabase.storage
      .from('lure-images')
      .upload(filePath, bytes.buffer, {
        contentType: 'image/jpeg',
        upsert: false,
      });

    if (error) throw error;

    // Get public URL
    const { data: urlData } = supabase.storage
      .from('lure-images')
      .getPublicUrl(filePath);

    return { success: true, path: data.path, url: urlData.publicUrl };
  } catch (error) {
    console.error('[Supabase] Upload image error:', error);
    throw new Error(error.message || 'Failed to upload image');
  }
};

/**
 * Delete lure image from Storage
 */
export const deleteLureImage = async (imagePath) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { error } = await supabase.storage
      .from('lure-images')
      .remove([imagePath]);

    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('[Supabase] Delete image error:', error);
    throw new Error(error.message || 'Failed to delete image');
  }
};

// ============================================================================
// CATCHES (Catch Photos for Each Lure)
// ============================================================================

/**
 * Add a catch to a lure
 */
export const addCatchToLure = async (lureAnalysisId, catchData) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    // Upload catch image to storage
    let imageUrl = null;
    if (catchData.imageUri) {
      const catchFileName = `catch_${Date.now()}.jpg`;
      const uploadResult = await uploadLureImage(catchData.imageUri, catchFileName);
      imageUrl = uploadResult.url;
    }

    const { data, error } = await supabase
      .from('catches')
      .insert([{
        lure_analysis_id: lureAnalysisId,
        user_id: user.id,
        fish_species: catchData.fishSpecies,
        weight: catchData.weight,
        length: catchData.length,
        location: catchData.location,
        notes: catchData.notes,
        image_url: imageUrl,
      }])
      .select()
      .single();

    if (error) throw error;
    return { success: true, catch: data };
  } catch (error) {
    console.error('[Supabase] Add catch error:', error);
    throw new Error(error.message || 'Failed to add catch');
  }
};

/**
 * Get all catches for a lure
 */
export const getCatchesForLure = async (lureAnalysisId) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { data, error } = await supabase
      .from('catches')
      .select('*')
      .eq('lure_analysis_id', lureAnalysisId)
      .eq('user_id', user.id)
      .order('catch_date', { ascending: false });

    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error('[Supabase] Get catches error:', error);
    return [];
  }
};

/**
 * Delete a catch
 */
export const deleteCatch = async (catchId) => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { error } = await supabase
      .from('catches')
      .delete()
      .eq('id', catchId)
      .eq('user_id', user.id);

    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('[Supabase] Delete catch error:', error);
    throw new Error(error.message || 'Failed to delete catch');
  }
};

// ============================================================================
// STATISTICS
// ============================================================================

/**
 * Get user's tackle box statistics
 */
export const getTackleBoxStats = async () => {
  try {
    const user = await getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    // Get all analyses
    const analyses = await getUserLureAnalyses();

    // Calculate statistics
    const totalLures = analyses.length;
    const lureTypes = {};
    const targetSpecies = new Set();
    let totalConfidence = 0;

    analyses.forEach(analysis => {
      // Count by type
      lureTypes[analysis.lure_type] = (lureTypes[analysis.lure_type] || 0) + 1;
      
      // Collect target species
      if (analysis.chatgpt_analysis?.target_species) {
        analysis.chatgpt_analysis.target_species.forEach(species => {
          targetSpecies.add(species);
        });
      }
      
      // Sum confidence
      totalConfidence += analysis.confidence || 0;
    });

    const avgConfidence = totalLures > 0 ? Math.round(totalConfidence / totalLures) : 0;

    return {
      totalLures,
      lureTypes,
      targetSpecies: Array.from(targetSpecies),
      avgConfidence,
      mostCommonType: Object.keys(lureTypes).sort((a, b) => lureTypes[b] - lureTypes[a])[0] || 'None',
    };
  } catch (error) {
    console.error('[Supabase] Get stats error:', error);
    throw new Error(error.message || 'Failed to load statistics');
  }
};

export default {
  // Auth
  signUp,
  signIn,
  signOut,
  getCurrentUser,
  getCurrentSession,
  resetPassword,
  
  // Profile
  getUserProfile,
  updateUserProfile,
  
  // Lure Analyses
  saveLureAnalysis,
  getUserLureAnalyses,
  getLureAnalysisById,
  deleteLureAnalysis,
  bulkDeleteLureAnalyses,
  
  // Storage
  uploadLureImage,
  deleteLureImage,
  
  // Catches
  addCatchToLure,
  getCatchesForLure,
  deleteCatch,
  
  // Stats
  getTackleBoxStats,
};

