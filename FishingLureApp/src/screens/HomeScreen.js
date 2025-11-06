import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Alert,
  ScrollView,
  ActivityIndicator,
  Modal,
  SafeAreaView,
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as ImageManipulator from 'expo-image-manipulator';
import { Camera } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { analyzeLure } from '../services/lureAnalysisService';
import { saveLureToTackleBox } from '../services/storageService';
import { saveLureAnalysis } from '../services/supabaseService';
import { getQuotaStatus } from '../services/subscriptionService';
import { useAuth } from '../contexts/AuthContext';

export default function HomeScreen() {
  const { user } = useAuth();
  const navigation = useNavigation();
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const [quotaStatus, setQuotaStatus] = useState(null);

  // Load quota status when screen is focused
  useFocusEffect(
    React.useCallback(() => {
      loadQuotaStatus();
    }, [user])
  );
  
  const loadQuotaStatus = async () => {
    if (user) {
      try {
        const status = await getQuotaStatus();
        setQuotaStatus(status);
      } catch (error) {
        console.error('Failed to load quota:', error);
      }
    }
  };
  
  const compressImage = async (imageUri) => {
    try {
      console.log('[HomeScreen] Compressing image...');
      const manipResult = await ImageManipulator.manipulateAsync(
        imageUri,
        [
          { resize: { width: 1200 } }, // Resize to max 1200px width (maintains aspect ratio)
        ],
        { 
          compress: 0.7,  // 70% quality (good balance of quality vs size)
          format: ImageManipulator.SaveFormat.JPEG 
        }
      );
      console.log('[HomeScreen] ✓ Image compressed');
      return manipResult.uri;
    } catch (error) {
      console.warn('[HomeScreen] Compression failed, using original:', error);
      return imageUri; // Return original if compression fails
    }
  };

  const requestPermissions = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Sorry, we need camera roll permissions to make this work!');
      return false;
    }
    return true;
  };

  const pickImage = async () => {
    const hasPermission = await requestPermissions();
    if (!hasPermission) return;

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      // Compress image before setting
      const compressedUri = await compressImage(result.assets[0].uri);
      setSelectedImage({ ...result.assets[0], uri: compressedUri });
      setAnalysisResult(null);
    }
  };

  const takePicture = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Sorry, we need camera permissions to make this work!');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      // Compress image before setting
      const compressedUri = await compressImage(result.assets[0].uri);
      setSelectedImage({ ...result.assets[0], uri: compressedUri });
      setAnalysisResult(null);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) {
      Alert.alert('No Image', 'Please select an image first');
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await analyzeLure(selectedImage.uri);
      setAnalysisResult(result);
      
      // Save to local tackle box (backwards compatibility)
      await saveLureToTackleBox({
        imageUri: selectedImage.uri,
        analysis: result,
        timestamp: new Date().toISOString(),
      });
      
      // Refresh quota status after successful scan
      if (user) {
        loadQuotaStatus(); // Update counter immediately
      }
      
      // Also save to Supabase if user is logged in
      if (user && result.supabase_id) {
        console.log('[HomeScreen] Analysis already saved to Supabase by backend');
        Alert.alert('Success', 'Lure analyzed and saved to your cloud tackle box! ☁️');
      } else if (user) {
        // Try to save to Supabase if backend didn't do it
        try {
          await saveLureAnalysis(result);
          console.log('[HomeScreen] Saved to Supabase from mobile app');
          Alert.alert('Success', 'Lure analyzed and saved to your cloud tackle box! ☁️');
        } catch (supabaseError) {
          console.log('[HomeScreen] Supabase save failed, using local only');
          Alert.alert('Success', 'Lure analyzed and saved locally!');
        }
      } else {
        Alert.alert('Success', 'Lure analyzed and saved to tackle box!');
      }
    } catch (error) {
      if (__DEV__) {
        console.error('Analysis error:', error);
      }
      
      // Check if it's a quota exceeded error
      if (error.code === 'QUOTA_EXCEEDED') {
        // Update quota to show 0 remaining
        if (user) {
          setQuotaStatus({
            isPro: false,
            unlimited: false,
            used: 10,
            remaining: 0,
            limit: 10,
            message: '🚫 0 scans remaining',
            subtitle: 'Upgrade to PRO for unlimited scans',
            emoji: '🚫'
          });
        }
        
        Alert.alert(
          '🎣 Free Scans Used Up!',
          "You've used all 10 free scans this month. Upgrade to PRO for unlimited scans!",
          [
            { text: 'Maybe Later', style: 'cancel' },
            { 
              text: 'Upgrade to PRO', 
              onPress: () => navigation.navigate('Paywall', {
                message: "You've used all 10 free scans this month!"
              })
            }
          ]
        );
      } else {
        Alert.alert('Error', error.message || 'Failed to analyze lure. Please try again.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetSelection = () => {
    setSelectedImage(null);
    setAnalysisResult(null);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container}>
        <View style={styles.header}>
        <Text style={styles.title}>🎣 Mobile Lure Classifier</Text>
        <Text style={styles.subtitle}>AI-Powered Fishing Lure Identification</Text>
        
        {/* Quota Display */}
        {user && quotaStatus && !quotaStatus.unlimited && (
          <View style={styles.quotaCard}>
            <Text style={styles.quotaText}>
              {quotaStatus.emoji} {quotaStatus.message}
            </Text>
            <Text style={styles.quotaSubtext}>{quotaStatus.subtitle}</Text>
            {quotaStatus.remaining <= 3 && quotaStatus.remaining > 0 && (
              <TouchableOpacity
                style={styles.miniUpgradeButton}
                onPress={() => navigation.navigate('Paywall')}
              >
                <Text style={styles.miniUpgradeText}>Upgrade to PRO →</Text>
              </TouchableOpacity>
            )}
          </View>
        )}
        
        {user && quotaStatus && quotaStatus.unlimited && (
          <View style={styles.proCard}>
            <Text style={styles.proText}>💎 PRO - Unlimited Scans</Text>
          </View>
        )}
      </View>

      <View style={styles.uploadSection}>
        {!selectedImage ? (
          <View style={styles.uploadButtons}>
            <TouchableOpacity style={styles.button} onPress={pickImage}>
              <Text style={styles.buttonText}>📸 Choose from Gallery</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.button} onPress={takePicture}>
              <Text style={styles.buttonText}>📷 Take Photo</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.imageContainer}>
            <Image source={{ uri: selectedImage.uri }} style={styles.image} />
            <View style={styles.imageActions}>
              <TouchableOpacity style={styles.actionButton} onPress={resetSelection}>
                <Text style={styles.actionButtonText}>🔄 Change Image</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={[styles.actionButton, styles.analyzeButton]} 
                onPress={analyzeImage}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <Text style={styles.analyzeButtonText}>🔍 Analyze Lure</Text>
                )}
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>

      {analysisResult && (
        <View style={styles.resultsSection}>
          <Text style={styles.resultsTitle}>Analysis Results</Text>
          
          <View style={styles.resultCard}>
            <Text style={styles.lureType}>{analysisResult.lure_type}</Text>
            <Text style={styles.confidence}>Confidence: {analysisResult.confidence}%</Text>
          </View>

          {analysisResult.chatgpt_analysis && (
            <View style={styles.detailsCard}>
              <Text style={styles.detailsTitle}>🧠 AI Analysis</Text>
              <Text style={styles.detailsText}>
                <Text style={styles.bold}>Target Species:</Text> {analysisResult.chatgpt_analysis.target_species?.join(', ') || 'Unknown'}
              </Text>
              <Text style={styles.detailsText}>
                <Text style={styles.bold}>Reasoning:</Text> {analysisResult.chatgpt_analysis.reasoning || 'No reasoning provided'}
              </Text>
            </View>
          )}

          {analysisResult.lure_details && (
            <View style={styles.detailsCard}>
              <Text style={styles.detailsTitle}>🎣 Fishing Tips</Text>
              <Text style={styles.detailsText}>
                <Text style={styles.bold}>Description:</Text> {analysisResult.lure_details.description || 'No description available'}
              </Text>
              <Text style={styles.detailsText}>
                <Text style={styles.bold}>Best Conditions:</Text> {analysisResult.lure_details.best_conditions?.water_clarity?.join(', ') || 'Any'}
              </Text>
              <Text style={styles.detailsText}>
                <Text style={styles.bold}>Retrieve Styles:</Text> {analysisResult.lure_details.retrieve_styles?.join(', ') || 'Standard retrieve'}
              </Text>
            </View>
          )}

          {/* Scan Next Lure Button */}
          <TouchableOpacity 
            style={styles.scanNextButton} 
            onPress={resetSelection}
          >
            <Ionicons name="camera" size={24} color="white" />
            <Text style={styles.scanNextButtonText}>📸 Scan Next Lure</Text>
          </TouchableOpacity>
        </View>
      )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#2c3e50',
  },
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#2c3e50',
    padding: 20,
    paddingTop: 10,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#bdc3c7',
  },
  quotaCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    padding: 12,
    borderRadius: 8,
    marginTop: 16,
    alignItems: 'center',
  },
  quotaText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  quotaSubtext: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: 12,
    marginTop: 4,
  },
  miniUpgradeButton: {
    backgroundColor: '#fff',
    padding: 8,
    paddingHorizontal: 16,
    borderRadius: 6,
    marginTop: 8,
  },
  miniUpgradeText: {
    color: '#2c3e50',
    fontSize: 12,
    fontWeight: 'bold',
  },
  proCard: {
    backgroundColor: 'rgba(255, 215, 0, 0.25)',
    padding: 10,
    borderRadius: 8,
    marginTop: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 215, 0, 0.4)',
    alignItems: 'center',
  },
  proText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  uploadSection: {
    padding: 20,
  },
  uploadButtons: {
    gap: 15,
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  imageContainer: {
    alignItems: 'center',
  },
  image: {
    width: 300,
    height: 300,
    borderRadius: 10,
    marginBottom: 20,
  },
  imageActions: {
    flexDirection: 'row',
    gap: 10,
  },
  actionButton: {
    backgroundColor: '#95a5a6',
    padding: 10,
    borderRadius: 8,
    flex: 1,
    alignItems: 'center',
  },
  actionButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  analyzeButton: {
    backgroundColor: '#27ae60',
  },
  analyzeButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  resultsSection: {
    padding: 20,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#2c3e50',
  },
  resultCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lureType: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 5,
  },
  confidence: {
    fontSize: 16,
    color: '#27ae60',
    fontWeight: 'bold',
  },
  detailsCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  detailsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
  },
  detailsText: {
    fontSize: 14,
    color: '#555',
    marginBottom: 8,
    lineHeight: 20,
  },
  bold: {
    fontWeight: 'bold',
  },
  scanNextButton: {
    backgroundColor: '#3498db',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  scanNextButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});
