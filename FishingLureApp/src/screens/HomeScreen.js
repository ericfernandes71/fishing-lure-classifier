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
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { Camera } from 'expo-camera';
import { analyzeLure } from '../services/lureAnalysisService';
import { saveLureToTackleBox } from '../services/storageService';

export default function HomeScreen() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showCamera, setShowCamera] = useState(false);

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

    if (!result.canceled) {
      setSelectedImage(result.assets[0]);
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

    if (!result.canceled) {
      setSelectedImage(result.assets[0]);
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
      
      // Save to tackle box
      await saveLureToTackleBox({
        imageUri: selectedImage.uri,
        analysis: result,
        timestamp: new Date().toISOString(),
      });
      
      Alert.alert('Success', 'Lure analyzed and saved to tackle box!');
    } catch (error) {
      if (__DEV__) {
        console.error('Analysis error:', error);
      }
      Alert.alert('Error', 'Failed to analyze lure. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetSelection = () => {
    setSelectedImage(null);
    setAnalysisResult(null);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🎣 Mobile Lure Classifier</Text>
        <Text style={styles.subtitle}>AI-Powered Fishing Lure Identification</Text>
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
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: '#2c3e50',
    padding: 20,
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
});
