import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
  ScrollView,
  Switch,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen() {
  const [apiKey, setApiKey] = useState('');
  const [isApiKeyVisible, setIsApiKeyVisible] = useState(false);
  const [autoSave, setAutoSave] = useState(true);
  const [notifications, setNotifications] = useState(true);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const encryptedApiKey = await AsyncStorage.getItem('openai_api_key');
      const savedAutoSave = await AsyncStorage.getItem('auto_save');
      const savedNotifications = await AsyncStorage.getItem('notifications');
      
      // Load API key directly
      if (encryptedApiKey) {
        setApiKey(encryptedApiKey);
      }
      
      if (savedAutoSave !== null) setAutoSave(JSON.parse(savedAutoSave));
      if (savedNotifications !== null) setNotifications(JSON.parse(savedNotifications));
    } catch (error) {
      if (__DEV__) {
        console.error('Error loading settings:', error);
      }
    }
  };

  const saveApiKey = async () => {
    const trimmedKey = apiKey.trim();
    
    // Enhanced validation
    if (!trimmedKey) {
      Alert.alert('Error', 'Please enter a valid API key');
      return;
    }
    
    // Validate API key format
    if (!trimmedKey.startsWith('sk-') || trimmedKey.length < 20) {
      Alert.alert('Invalid Format', 'OpenAI API keys should start with "sk-" and be at least 20 characters long');
      return;
    }

    try {
      // Store API key directly (for now, to fix the issue)
      await AsyncStorage.setItem('openai_api_key', trimmedKey);
      Alert.alert('Success', 'API key saved successfully!');
      
      // Clear the input field for security
      setApiKey('');
    } catch (error) {
      if (__DEV__) {
        console.error('Error saving API key:', error);
      }
      Alert.alert('Error', 'Failed to save API key');
    }
  };

  const clearApiKey = () => {
    Alert.alert(
      'Clear API Key',
      'Are you sure you want to clear your API key?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('openai_api_key');
              setApiKey('');
              Alert.alert('Success', 'API key cleared');
            } catch (error) {
              if (__DEV__) {
                console.error('Error clearing API key:', error);
              }
              Alert.alert('Error', 'Failed to clear API key');
            }
          },
        },
      ]
    );
  };

  const saveSetting = async (key, value) => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      if (__DEV__) {
        console.error(`Error saving ${key}:`, error);
      }
    }
  };

  const clearAllData = () => {
    Alert.alert(
      'Clear All Data',
      'This will delete all your analyzed lures and settings. This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear All',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.clear();
              setApiKey('');
              setAutoSave(true);
              setNotifications(true);
              Alert.alert('Success', 'All data cleared');
            } catch (error) {
              if (__DEV__) {
                console.error('Error clearing data:', error);
              }
              Alert.alert('Error', 'Failed to clear data');
            }
          },
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>⚙️ Settings</Text>
        <Text style={styles.subtitle}>Configure your app preferences</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🔑 API Configuration</Text>
        
        <View style={styles.inputContainer}>
          <Text style={styles.label}>OpenAI API Key</Text>
          <TextInput
            style={styles.input}
            value={apiKey}
            onChangeText={setApiKey}
            placeholder="Enter your OpenAI API key"
            secureTextEntry={!isApiKeyVisible}
            autoCapitalize="none"
            autoCorrect={false}
          />
          <TouchableOpacity
            style={styles.visibilityButton}
            onPress={() => setIsApiKeyVisible(!isApiKeyVisible)}
          >
            <Text style={styles.visibilityButtonText}>
              {isApiKeyVisible ? '🙈' : '👁️'}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.saveButton} onPress={saveApiKey}>
            <Text style={styles.saveButtonText}>💾 Save API Key</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.clearButton} onPress={clearApiKey}>
            <Text style={styles.clearButtonText}>🗑️ Clear</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.helpText}>
          Get your API key from{' '}
          <Text style={styles.link}>https://platform.openai.com/api-keys</Text>
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🎣 App Preferences</Text>
        
        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Auto-save to Tackle Box</Text>
          <Switch
            value={autoSave}
            onValueChange={(value) => {
              setAutoSave(value);
              saveSetting('auto_save', value);
            }}
            trackColor={{ false: '#767577', true: '#3498db' }}
            thumbColor={autoSave ? '#fff' : '#f4f3f4'}
          />
        </View>

        <View style={styles.settingRow}>
          <Text style={styles.settingLabel}>Notifications</Text>
          <Switch
            value={notifications}
            onValueChange={(value) => {
              setNotifications(value);
              saveSetting('notifications', value);
            }}
            trackColor={{ false: '#767577', true: '#3498db' }}
            thumbColor={notifications ? '#fff' : '#f4f3f4'}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>ℹ️ App Information</Text>
        
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Version</Text>
          <Text style={styles.infoValue}>1.0.0</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Text style={styles.infoLabel}>Developer</Text>
          <Text style={styles.infoValue}>Fishing Lure App</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>⚠️ Danger Zone</Text>
        
        <TouchableOpacity style={styles.dangerButton} onPress={clearAllData}>
          <Text style={styles.dangerButtonText}>🗑️ Clear All Data</Text>
        </TouchableOpacity>
        
        <Text style={styles.dangerText}>
          This will delete all your analyzed lures, settings, and API keys.
        </Text>
      </View>
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
  section: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 15,
  },
  inputContainer: {
    position: 'relative',
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f8f9fa',
    paddingRight: 50,
  },
  visibilityButton: {
    position: 'absolute',
    right: 10,
    top: 35,
    padding: 5,
  },
  visibilityButtonText: {
    fontSize: 20,
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 15,
  },
  saveButton: {
    backgroundColor: '#27ae60',
    padding: 12,
    borderRadius: 8,
    flex: 1,
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  clearButton: {
    backgroundColor: '#e74c3c',
    padding: 12,
    borderRadius: 8,
    flex: 1,
    alignItems: 'center',
  },
  clearButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  helpText: {
    fontSize: 14,
    color: '#7f8c8d',
    lineHeight: 20,
  },
  link: {
    color: '#3498db',
    textDecorationLine: 'underline',
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  settingLabel: {
    fontSize: 16,
    color: '#2c3e50',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  infoLabel: {
    fontSize: 16,
    color: '#2c3e50',
  },
  infoValue: {
    fontSize: 16,
    color: '#7f8c8d',
  },
  dangerButton: {
    backgroundColor: '#e74c3c',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 10,
  },
  dangerButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  dangerText: {
    fontSize: 14,
    color: '#e74c3c',
    textAlign: 'center',
    lineHeight: 20,
  },
});
