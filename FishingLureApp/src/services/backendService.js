import axios from 'axios';
import { supabase } from '../config/supabase';
import { Platform } from 'react-native';

// Configuration - Use environment variables for security
// Using production backend (Render) - always available
export const BACKEND_URL = 'https://fishing-lure-backend.onrender.com';

console.log('[BackendService] Using backend URL:', BACKEND_URL);

// Helper to get current user ID
const getCurrentUserId = async () => {
  try {
    const { data: { user } } = await supabase.auth.getUser();
    return user?.id || null;
  } catch (error) {
    return null;
  }
};

// Input validation helper
const validateImageUri = (imageUri) => {
  if (!imageUri || typeof imageUri !== 'string') {
    throw new Error('Invalid image URI provided');
  }
  
  // Basic URI validation
  if (!imageUri.startsWith('file://') && !imageUri.startsWith('content://') && !imageUri.startsWith('data:')) {
    throw new Error('Invalid image URI format');
  }
  
  return true;
};

export const analyzeLureWithBackend = async (imageUri) => {
  try {
    // Validate input
    validateImageUri(imageUri);
    
    // Get current user ID
    const userId = await getCurrentUserId();
    
    // Create FormData for file upload
    const formData = new FormData();
    
    // Convert image URI to blob for upload
    const response = await fetch(imageUri);
    const blob = await response.blob();
    
    // Create file object
    const filename = `lure_${Date.now()}.jpg`;
    const file = {
      uri: imageUri,
      type: 'image/jpeg',
      name: filename,
    };
    
    formData.append('file', file);
    
    // Add user_id if available
    if (userId) {
      formData.append('user_id', userId);
    }

    // Make request to Flask backend
    const apiResponse = await axios.post(`${BACKEND_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...(userId && { 'X-User-ID': userId }), // Include user ID in headers
      },
      timeout: 120000, // 2 minute timeout (OpenAI can be slow sometimes)
    });

    return apiResponse.data;

  } catch (error) {
    // Only log errors in development mode
    if (__DEV__) {
      console.error('Backend analysis error:', error);
    }
    
    if (error.code === 'NETWORK_ERROR' || error.message.includes('Network Error')) {
      throw new Error('Cannot connect to server. Please make sure your Flask server is running and accessible.');
    } else if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      const message = data?.error || data?.message || 'Server error occurred';
      
      // Handle quota exceeded (403) - this should trigger paywall
      if (status === 403 && data?.error === 'quota_exceeded') {
        const quotaError = new Error(data.message);
        quotaError.code = 'QUOTA_EXCEEDED';
        quotaError.quota = data.quota;
        throw quotaError;
      }
      
      if (status === 500) {
        throw new Error('Server error. Please check your API configuration.');
      } else {
        throw new Error(`Server Error (${status}): ${message}`);
      }
    } else {
      throw new Error('Failed to analyze lure. Please check your connection and try again.');
    }
  }
};

export const estimateCostWithBackend = async (imageUri) => {
  try {
    const formData = new FormData();
    
    const response = await fetch(imageUri);
    const blob = await response.blob();
    
    const filename = `lure_${Date.now()}.jpg`;
    const file = {
      uri: imageUri,
      type: 'image/jpeg',
      name: filename,
    };
    
    formData.append('file', file);

    const apiResponse = await axios.post(`${BACKEND_URL}/estimate-cost`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 second timeout
    });

    return apiResponse.data;

  } catch (error) {
    if (__DEV__) {
      console.error('Cost estimation error:', error);
    }
    throw new Error('Failed to estimate cost. Please try again.');
  }
};

export const getTackleBoxFromBackend = async () => {
  try {
    const response = await axios.get(`${BACKEND_URL}/api/tackle-box`, {
      timeout: 30000, // 30 second timeout
    });
    
    return response.data.results || [];
  } catch (error) {
    if (__DEV__) {
      console.error('Error fetching tackle box:', error);
    }
    throw new Error('Failed to load tackle box from server.');
  }
};

export const getTackleBoxFromSupabase = async () => {
  try {
    // Get current user ID
    const userId = await getCurrentUserId();
    
    if (!userId) {
      throw new Error('User not authenticated');
    }
    
    const response = await axios.get(`${BACKEND_URL}/api/supabase/tackle-box`, {
      params: { user_id: userId },
      headers: {
        'X-User-ID': userId,
      },
      timeout: 30000,
    });
    
    return response.data.results || [];
  } catch (error) {
    if (__DEV__) {
      console.error('Error fetching Supabase tackle box:', error);
    }
    throw new Error('Failed to load tackle box from cloud.');
  }
};

export const deleteLureFromBackend = async (lureId) => {
  try {
    const response = await axios.delete(`${BACKEND_URL}/api/delete-lure/${lureId}`, {
      timeout: 30000, // 30 second timeout
    });
    
    return response.data;
  } catch (error) {
    if (__DEV__) {
      console.error('Error deleting lure:', error);
    }
    throw new Error('Failed to delete lure from server.');
  }
};

// Helper function to test backend connection
export const testBackendConnection = async () => {
  try {
    console.log('[BackendService] Testing connection to:', BACKEND_URL);
    const response = await axios.get(`${BACKEND_URL}/health`, {
      timeout: 10000, // 10 seconds should be enough for a simple JSON response
    });
    console.log('[BackendService] Connection successful! Response:', response.data);
    return { 
      connected: true, 
      status: response.status,
      message: response.data.message 
    };
  } catch (error) {
    console.error('[BackendService] Connection failed:', error.message);
    console.error('[BackendService] Error details:', error);
    return { 
      connected: false, 
      error: error.message,
      suggestion: 'Make sure your Flask server is running on the correct port and accessible from your device.',
      url: BACKEND_URL // Include URL in response for debugging
    };
  }
};
