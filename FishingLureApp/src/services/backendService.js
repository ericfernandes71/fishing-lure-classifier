import axios from 'axios';

// Configuration - Use environment variables for security
const BACKEND_URL = __DEV__ 
  ? 'http://localhost:5000'  // Development only
  : 'https://your-production-server.com'; // Production URL - UPDATE THIS!

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

    // Make request to Flask backend
    const apiResponse = await axios.post(`${BACKEND_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 second timeout
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
      const message = error.response.data?.error || 'Server error occurred';
      
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
      timeout: 10000,
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
      timeout: 10000,
    });
    
    return response.data.results || [];
  } catch (error) {
    if (__DEV__) {
      console.error('Error fetching tackle box:', error);
    }
    throw new Error('Failed to load tackle box from server.');
  }
};

export const deleteLureFromBackend = async (lureId) => {
  try {
    const response = await axios.delete(`${BACKEND_URL}/api/delete-lure/${lureId}`, {
      timeout: 10000,
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
    const response = await axios.get(`${BACKEND_URL}/`, {
      timeout: 5000,
    });
    return { connected: true, status: response.status };
  } catch (error) {
    return { 
      connected: false, 
      error: error.message,
      suggestion: 'Make sure your Flask server is running on the correct port and accessible from your device.'
    };
  }
};
