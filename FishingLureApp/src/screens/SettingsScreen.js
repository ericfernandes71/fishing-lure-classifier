import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  Switch,
  ActivityIndicator,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { testBackendConnection } from '../services/backendService';
import { useAuth } from '../contexts/AuthContext';

export default function SettingsScreen() {
  const [autoSave, setAutoSave] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [backendStatus, setBackendStatus] = useState(null);
  const [isCheckingBackend, setIsCheckingBackend] = useState(false);
  const { user, signOut } = useAuth();

  useEffect(() => {
    loadSettings();
    // Check backend connection silently in background
    checkBackendConnection();
  }, []);

  const loadSettings = async () => {
    try {
      const savedAutoSave = await AsyncStorage.getItem('auto_save');
      const savedNotifications = await AsyncStorage.getItem('notifications');
      
      if (savedAutoSave !== null) setAutoSave(JSON.parse(savedAutoSave));
      if (savedNotifications !== null) setNotifications(JSON.parse(savedNotifications));
    } catch (error) {
      if (__DEV__) {
        console.error('Error loading settings:', error);
      }
    }
  };

  const checkBackendConnection = async () => {
    setIsCheckingBackend(true);
    try {
      console.log('[Settings] Testing backend connection...');
      const result = await testBackendConnection();
      console.log('[Settings] Backend test result:', result);
      setBackendStatus(result);
    } catch (error) {
      console.error('[Settings] Backend connection error:', error);
      setBackendStatus({ 
        connected: false, 
        error: 'Connection test failed: ' + error.message 
      });
    } finally {
      setIsCheckingBackend(false);
    }
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

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            try {
              await signOut();
            } catch (error) {
              Alert.alert('Error', 'Failed to logout');
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

      {/* User Profile Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>👤 Account</Text>
        
        <View style={styles.userInfo}>
          <View style={styles.userAvatar}>
            <Text style={styles.userAvatarText}>
              {user?.email?.charAt(0).toUpperCase() || '?'}
            </Text>
          </View>
          <View style={styles.userDetails}>
            <Text style={styles.userName}>{user?.user_metadata?.full_name || 'User'}</Text>
            <Text style={styles.userEmail}>{user?.email}</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutButtonText}>🚪 Logout</Text>
        </TouchableOpacity>
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
  statusContainer: {
    marginBottom: 15,
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderRadius: 8,
  },
  statusConnected: {
    backgroundColor: '#d4edda',
    borderColor: '#c3e6cb',
    borderWidth: 1,
  },
  statusDisconnected: {
    backgroundColor: '#f8d7da',
    borderColor: '#f5c6cb',
    borderWidth: 1,
  },
  statusIcon: {
    fontSize: 24,
    marginRight: 10,
  },
  statusText: {
    fontSize: 16,
    color: '#2c3e50',
  },
  errorText: {
    fontSize: 14,
    color: '#e74c3c',
    marginTop: 10,
    lineHeight: 20,
  },
  refreshButton: {
    backgroundColor: '#3498db',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 15,
  },
  refreshButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
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
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    marginBottom: 15,
  },
  userAvatar: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#3498db',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  userAvatarText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  userDetails: {
    flex: 1,
  },
  userName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  logoutButton: {
    backgroundColor: '#e74c3c',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
