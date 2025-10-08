import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { analyzeLureWithBackend, testBackendConnection } from './backendService';
import { SecurityUtils, API_CONFIG, getCurrentConfig } from '../config/security';

const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

// Create rate limiter instance
const rateLimiter = SecurityUtils.createRateLimiter(API_CONFIG.RATE_LIMIT_MS);

export const analyzeLure = async (imageUri) => {
  try {
            // Validate input using security utils
            SecurityUtils.validateImageUri(imageUri);
            
            // Validate image size
            await SecurityUtils.validateImageSize(imageUri);
    
    // Check rate limiting
    rateLimiter();
    
    // First, try to use the backend server if available
    try {
      const backendResult = await analyzeLureWithBackend(imageUri);
      return backendResult;
    } catch (backendError) {
      if (__DEV__) {
        console.log('Backend not available, trying direct OpenAI API:', backendError.message);
      }
      
      // Fallback to direct OpenAI API
      const apiKey = await AsyncStorage.getItem('openai_api_key');
      
          // Validate API key using security utils
          const validatedApiKey = SecurityUtils.validateApiKey(apiKey);
          
          // Additional security: Check for suspicious patterns
          if (validatedApiKey.includes('test') || validatedApiKey.includes('demo')) {
            SecurityUtils.secureLog('warn', 'Potentially test API key detected');
          }

      // Convert image to base64
      const base64Image = await convertImageToBase64(imageUri);

      // Prepare the request payload
      const payload = {
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'text',
                text: `Analyze this fishing lure image and provide detailed information. Please respond with a JSON object containing:
                {
                  "lure_type": "specific type of lure (e.g., Spinnerbait, Crankbait, Jig, etc.)",
                  "confidence": "confidence percentage (0-100)",
                  "target_species": ["list of fish species this lure targets"],
                  "reasoning": "detailed explanation of why you identified it as this type",
                  "description": "detailed description of the lure's appearance and features",
                  "best_conditions": {
                    "water_clarity": ["clear", "murky", "stained"],
                    "water_temperature_f": "optimal temperature range",
                    "depth_ft": "optimal depth range",
                    "structure_cover": ["rocks", "weeds", "open water", "docks"]
                  },
                  "retrieve_styles": ["slow retrieve", "fast retrieve", "stop and go", "jigging"],
                  "recommended_colors": {
                    "clear_water": ["natural colors"],
                    "murky_water": ["bright colors"],
                    "stained_water": ["contrasting colors"]
                  },
                  "common_mistakes": ["list of common mistakes when using this lure"],
                  "notes": "additional fishing tips and advice"
                }`
              },
              {
                type: 'image_url',
                image_url: {
                  url: `data:image/jpeg;base64,${base64Image}`,
                  detail: 'high'
                }
              }
            ]
          }
        ],
        max_tokens: 1000,
        temperature: 0.3
      };

      // Make API request with timeout
      const response = await axios.post(OPENAI_API_URL, payload, {
        headers: {
          'Authorization': `Bearer ${validatedApiKey}`,
          'Content-Type': 'application/json',
        },
        timeout: API_CONFIG.REQUEST_TIMEOUT,
      });

            // Parse the response with security validation
            const content = response.data.choices[0].message.content;
            
            // Security: Sanitize response content
            const sanitizedContent = content.replace(/<script[^>]*>.*?<\/script>/gi, '')
                                           .replace(/javascript:/gi, '')
                                           .replace(/on\w+\s*=/gi, '');
            
            // Try to extract JSON from the response
            let analysisResult;
            try {
              // Look for JSON in the response
              const jsonMatch = sanitizedContent.match(/\{[\s\S]*\}/);
              if (jsonMatch) {
                analysisResult = JSON.parse(jsonMatch[0]);
                
                // Validate the analysis result structure
                if (!analysisResult.lure_type || typeof analysisResult.confidence !== 'number') {
                  throw new Error('Invalid analysis result structure');
                }
                
                // Sanitize string fields
                if (analysisResult.reasoning) {
                  analysisResult.reasoning = analysisResult.reasoning.substring(0, 1000); // Limit length
                }
              } else {
                throw new Error('No JSON found in response');
              }
            } catch (parseError) {
        // Fallback: create a basic result structure
        analysisResult = {
          lure_type: 'Unknown Lure',
          confidence: 50,
          target_species: ['Various'],
          reasoning: content,
          description: 'Unable to parse detailed analysis',
          best_conditions: {
            water_clarity: ['Any'],
            water_temperature_f: 'Any',
            depth_ft: 'Any',
            structure_cover: ['Any']
          },
          retrieve_styles: ['Standard retrieve'],
          recommended_colors: 'Natural colors',
          common_mistakes: ['None specified'],
          notes: content
        };
      }

      // Add metadata
      const result = {
        lure_type: analysisResult.lure_type || 'Unknown Lure',
        confidence: analysisResult.confidence || 50,
        analysis_method: 'ChatGPT Vision API (Direct)',
        analysis_date: new Date().toISOString(),
        chatgpt_analysis: {
          confidence: analysisResult.confidence || 50,
          target_species: analysisResult.target_species || ['Various'],
          reasoning: analysisResult.reasoning || 'No reasoning provided'
        },
        lure_details: {
          description: analysisResult.description || 'No description available',
          target_species: analysisResult.target_species || ['Various'],
          best_seasons: ['Year-round'],
          best_conditions: analysisResult.best_conditions || {
            water_clarity: ['Any'],
            water_temperature_f: 'Any',
            depth_ft: 'Any',
            structure_cover: ['Any']
          },
          retrieve_styles: analysisResult.retrieve_styles || ['Standard retrieve'],
          recommended_colors: analysisResult.recommended_colors || 'Natural colors',
          common_mistakes: analysisResult.common_mistakes || ['None specified'],
          notes: analysisResult.notes || 'No additional tips available'
        }
      };

      return result;
    }

  } catch (error) {
    // Use secure logging
    SecurityUtils.secureLog('error', 'Lure analysis error:', error);
    
    if (error.response) {
      // API error
      const status = error.response.status;
      const message = error.response.data?.error?.message || 'API request failed';
      
      if (status === 401) {
        throw new Error('Invalid API key. Please check your OpenAI API key in Settings.');
      } else if (status === 429) {
        throw new Error('Rate limit exceeded. Please try again later.');
      } else if (status === 400) {
        throw new Error('Invalid request. Please try with a different image.');
      } else {
        throw new Error(`API Error (${status}): ${message}`);
      }
    } else if (error.message.includes('API key')) {
      throw error;
    } else {
      throw new Error('Failed to analyze lure. Please check your internet connection and try again.');
    }
  }
};

const convertImageToBase64 = async (imageUri) => {
  try {
    // For React Native, we need to use a different approach
    const response = await fetch(imageUri);
    const blob = await response.blob();
    
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } catch (error) {
    SecurityUtils.secureLog('error', 'Error converting image to base64:', error);
    throw new Error('Failed to process image');
  }
};

export const estimateCost = async (imageUri) => {
  try {
    const base64Image = await convertImageToBase64(imageUri);
    const imageSizeKB = Math.round(base64Image.length * 0.75 / 1024); // Approximate
    
    // Estimate tokens (rough calculation)
    const estimatedTokens = Math.ceil(imageSizeKB / 4) + 1000; // Base tokens + image tokens
    
    // Cost estimation (GPT-4o-mini pricing)
    const costPerToken = 0.00015 / 1000; // $0.15 per 1M tokens
    const estimatedCost = estimatedTokens * costPerToken;
    
    return {
      image_size_kb: imageSizeKB,
      estimated_tokens: estimatedTokens,
      estimated_cost_usd: `$${estimatedCost.toFixed(4)}`,
      cost_efficiency: 'Optimized for mobile use'
    };
  } catch (error) {
    console.error('Cost estimation error:', error);
    throw new Error('Failed to estimate cost');
  }
};
