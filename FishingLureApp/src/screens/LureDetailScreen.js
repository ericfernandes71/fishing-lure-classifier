import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
  Modal,
  TextInput,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { addCatchToLure as addCatchLocal, deleteCatchFromLure } from '../services/storageService';
import { addCatchToLure as addCatchSupabase, getCatchesForLure, deleteCatch } from '../services/supabaseService';
import { useAuth } from '../contexts/AuthContext';

export default function LureDetailScreen({ route, navigation }) {
  const { lure } = route.params;
  const { user } = useAuth();
  const [catches, setCatches] = useState(lure.catches || []);
  const [addCatchModalVisible, setAddCatchModalVisible] = useState(false);
  const [viewCatchModalVisible, setViewCatchModalVisible] = useState(false);
  const [selectedCatch, setSelectedCatch] = useState(null);
  const [catchPhoto, setCatchPhoto] = useState(null);
  const [catchDetails, setCatchDetails] = useState({
    fishSpecies: '',
    weight: '',
    length: '',
    location: '',
    notes: '',
  });

  // Helper to check if lure is from Supabase (has UUID format)
  const isSupabaseLure = () => {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    return lure.id && uuidRegex.test(lure.id);
  };

  // Load catches from Supabase if it's a Supabase lure
  useEffect(() => {
    const loadCatches = async () => {
      if (user && isSupabaseLure()) {
        try {
          const supabaseCatches = await getCatchesForLure(lure.id);
          // Convert Supabase format to match local format
          const formattedCatches = supabaseCatches.map(c => ({
            id: c.id,
            imageUri: c.image_url,
            timestamp: c.catch_date || c.created_at,
            fishSpecies: c.fish_species,
            weight: c.weight,
            length: c.length,
            location: c.location,
            notes: c.notes,
          }));
          setCatches(formattedCatches);
          console.log('[LureDetail] Loaded catches from Supabase:', formattedCatches.length);
        } catch (error) {
          console.error('[LureDetail] Error loading catches:', error);
        }
      }
    };
    loadCatches();
  }, [lure.id, user]);

  const pickCatchPhoto = async (useCamera = false) => {
    try {
      let result;
      
      if (useCamera) {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();
        if (status !== 'granted') {
          Alert.alert('Permission needed', 'Camera permission is required to take photos');
          return;
        }
        result = await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });
      } else {
        result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });
      }

      if (!result.canceled) {
        setCatchPhoto(result.assets[0]);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick photo');
    }
  };

  const saveCatch = async () => {
    if (!catchPhoto) {
      Alert.alert('No Photo', 'Please add a photo of your catch');
      return;
    }

    try {
      const catchData = {
        imageUri: catchPhoto.uri,
        timestamp: new Date().toISOString(),
        ...catchDetails,
      };

      let newCatch;

      // Use Supabase for Supabase lures, local storage for local lures
      if (user && isSupabaseLure()) {
        console.log('[LureDetail] Saving catch to Supabase for lure:', lure.id);
        const result = await addCatchSupabase(lure.id, catchData);
        // Convert to display format
        newCatch = {
          id: result.catch.id,
          imageUri: result.catch.image_url,
          timestamp: result.catch.catch_date || result.catch.created_at,
          fishSpecies: result.catch.fish_species,
          weight: result.catch.weight,
          length: result.catch.length,
          location: result.catch.location,
          notes: result.catch.notes,
        };
      } else {
        // Local storage
        const lureIdentifier = lure.id || lure.timestamp || Date.now().toString();
        console.log('[LureDetail] Saving catch locally for lure:', lureIdentifier);
        await addCatchLocal(lureIdentifier, catchData);
        newCatch = {
          id: Date.now().toString(),
          ...catchData,
        };
      }
      
      // Update local state
      setCatches([...catches, newCatch]);
      
      Alert.alert('Success', 'Catch added successfully!');
      setAddCatchModalVisible(false);
      setCatchPhoto(null);
      setCatchDetails({
        fishSpecies: '',
        weight: '',
        length: '',
        location: '',
        notes: '',
      });
    } catch (error) {
      console.error('[LureDetail] Save catch error:', error);
      Alert.alert('Error', `Failed to save catch: ${error.message}`);
    }
  };

  const handleDeleteCatch = async (catchId) => {
    Alert.alert(
      'Delete Catch',
      'Are you sure you want to delete this catch?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              // Use Supabase or local storage depending on lure type
              if (user && isSupabaseLure()) {
                await deleteCatch(catchId);
                console.log('[LureDetail] Deleted catch from Supabase:', catchId);
              } else {
                await deleteCatchFromLure(lure.id, catchId);
                console.log('[LureDetail] Deleted catch locally:', catchId);
              }
              
              // Update local state
              setCatches(catches.filter(c => c.id !== catchId));
              
              Alert.alert('Success', 'Catch deleted');
              setViewCatchModalVisible(false);
            } catch (error) {
              console.error('[LureDetail] Delete catch error:', error);
              Alert.alert('Error', `Failed to delete catch: ${error.message}`);
            }
          },
        },
      ]
    );
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Lure',
      'Are you sure you want to delete this lure from your tackle box?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: () => {
            // This will be handled by the parent screen
            navigation.goBack();
          },
        },
      ]
    );
  };

  const renderSection = (title, content, icon) => {
    if (!content) return null;
    
    return (
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name={icon} size={20} color="#2c3e50" />
          <Text style={styles.sectionTitle}>{title}</Text>
        </View>
        <Text style={styles.sectionContent}>{content}</Text>
      </View>
    );
  };

  const renderRecommendedColors = (colors) => {
    if (!colors) return null;
    
    let colorText = '';
    if (typeof colors === 'object') {
      // Handle object format like { clear_water: [...], murky_water: [...] }
      const colorEntries = Object.entries(colors);
      colorText = colorEntries.map(([condition, colorList]) => {
        const colors = Array.isArray(colorList) ? colorList.join(', ') : colorList;
        return `${condition.replace(/_/g, ' ').toUpperCase()}: ${colors}`;
      }).join('\n\n');
    } else if (Array.isArray(colors)) {
      // Handle array format
      colorText = colors.join(', ');
    } else {
      // Handle string format
      colorText = colors.toString();
    }
    
    return (
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="color-palette" size={20} color="#2c3e50" />
          <Text style={styles.sectionTitle}>Recommended Colors</Text>
        </View>
        <Text style={styles.sectionContent}>{colorText}</Text>
      </View>
    );
  };

  const renderListSection = (title, items, icon) => {
    if (!items || items.length === 0) return null;
    
    return (
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name={icon} size={20} color="#2c3e50" />
          <Text style={styles.sectionTitle}>{title}</Text>
        </View>
        <View style={styles.listContainer}>
          {items.map((item, index) => (
            <View key={index} style={styles.listItem}>
              <Text style={styles.bullet}>•</Text>
              <Text style={styles.listText}>{item}</Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  const renderConditionsSection = (title, conditions, icon) => {
    if (!conditions) return null;
    
    return (
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name={icon} size={20} color="#2c3e50" />
          <Text style={styles.sectionTitle}>{title}</Text>
        </View>
        <View style={styles.conditionsGrid}>
          {Object.entries(conditions).map(([key, value]) => (
            <View key={key} style={styles.conditionItem}>
              <Text style={styles.conditionLabel}>{key.replace(/_/g, ' ').toUpperCase()}:</Text>
              <Text style={styles.conditionValue}>{Array.isArray(value) ? value.join(', ') : value}</Text>
            </View>
          ))}
        </View>
      </View>
    );
  };

  // Get lure image URL (supports both local and Supabase formats)
  const lureImageUri = lure.image_url || lure.imageUri || lure.image_path;

  return (
    <ScrollView style={styles.container}>
      {/* Header with Image */}
      <View style={styles.header}>
        {lureImageUri && (
          <Image source={{ uri: lureImageUri }} style={styles.lureImage} />
        )}
        <View style={styles.headerInfo}>
          <Text style={styles.lureType}>{lure.lure_type || 'Unknown Lure'}</Text>
          <Text style={styles.confidence}>
            Confidence: {lure.confidence || lure.chatgpt_analysis?.confidence || 'N/A'}%
          </Text>
          <Text style={styles.analysisDate}>
            Analyzed: {new Date(lure.analysis_date || lure.created_at || Date.now()).toLocaleDateString()}
          </Text>
        </View>
      </View>

      {/* Target Species */}
      {renderListSection(
        'Target Species',
        lure.lure_details?.target_species || lure.chatgpt_analysis?.target_species,
        'fish'
      )}

      {/* Description */}
      {renderSection(
        'Description',
        lure.lure_details?.description,
        'document-text'
      )}

      {/* Best Conditions */}
      {renderConditionsSection(
        'Best Fishing Conditions',
        lure.lure_details?.best_conditions,
        'sunny'
      )}

      {/* Retrieve Styles */}
      {renderListSection(
        'Retrieve Styles',
        lure.lure_details?.retrieve_styles,
        'refresh'
      )}

      {/* Recommended Colors */}
      {renderRecommendedColors(lure.lure_details?.recommended_colors)}

      {/* Common Mistakes */}
      {renderListSection(
        'Common Mistakes to Avoid',
        lure.lure_details?.common_mistakes,
        'warning'
      )}

      {/* Notes */}
      {renderSection(
        'Fishing Tips & Notes',
        lure.lure_details?.notes,
        'bulb'
      )}

      {/* Reasoning */}
      {renderSection(
        'AI Analysis Reasoning',
        lure.chatgpt_analysis?.reasoning || lure.lure_details?.reasoning,
        'analytics'
      )}

      {/* Catches Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="fish" size={20} color="#2c3e50" />
          <Text style={styles.sectionTitle}>My Catches ({catches.length})</Text>
        </View>
        
        {catches && catches.length > 0 ? (
          <FlatList
            data={catches}
            horizontal
            showsHorizontalScrollIndicator={false}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={styles.catchThumbnail}
                onPress={() => {
                  setSelectedCatch(item);
                  setViewCatchModalVisible(true);
                }}
              >
                <Image source={{ uri: item.imageUri }} style={styles.catchImage} />
                <Text style={styles.catchDate}>
                  {new Date(item.timestamp).toLocaleDateString()}
                </Text>
              </TouchableOpacity>
            )}
          />
        ) : (
          <Text style={styles.noCatchesText}>No catches recorded yet. Add your first catch!</Text>
        )}
        
        <TouchableOpacity
          style={styles.addCatchButton}
          onPress={() => setAddCatchModalVisible(true)}
        >
          <Ionicons name="add-circle" size={24} color="white" />
          <Text style={styles.addCatchButtonText}>Add Catch Photo</Text>
        </TouchableOpacity>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
          <Ionicons name="trash" size={20} color="white" />
          <Text style={styles.deleteButtonText}>Delete from Tackle Box</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.bottomSpacer} />

      {/* Add Catch Modal */}
      <Modal
        visible={addCatchModalVisible}
        animationType="slide"
        presentationStyle="pageSheet"
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>📸 Add Catch</Text>
            <TouchableOpacity onPress={() => setAddCatchModalVisible(false)}>
              <Ionicons name="close" size={24} color="#2c3e50" />
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.modalContent}>
            {/* Photo Picker */}
            <View style={styles.photoSection}>
              {catchPhoto ? (
                <Image source={{ uri: catchPhoto.uri }} style={styles.catchPhotoPreview} />
              ) : (
                <View style={styles.photoPlaceholder}>
                  <Ionicons name="camera" size={48} color="#95a5a6" />
                  <Text style={styles.photoPlaceholderText}>Add a photo of your catch</Text>
                </View>
              )}
              
              <View style={styles.photoButtons}>
                <TouchableOpacity
                  style={styles.photoButton}
                  onPress={() => pickCatchPhoto(true)}
                >
                  <Ionicons name="camera" size={20} color="white" />
                  <Text style={styles.photoButtonText}>Take Photo</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={styles.photoButton}
                  onPress={() => pickCatchPhoto(false)}
                >
                  <Ionicons name="images" size={20} color="white" />
                  <Text style={styles.photoButtonText}>Choose Photo</Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Catch Details Form */}
            <View style={styles.formSection}>
              <Text style={styles.formLabel}>Fish Species</Text>
              <TextInput
                style={styles.formInput}
                placeholder="e.g., Largemouth Bass"
                value={catchDetails.fishSpecies}
                onChangeText={(text) => setCatchDetails({...catchDetails, fishSpecies: text})}
              />

              <Text style={styles.formLabel}>Weight</Text>
              <TextInput
                style={styles.formInput}
                placeholder="e.g., 3.5 lbs"
                value={catchDetails.weight}
                onChangeText={(text) => setCatchDetails({...catchDetails, weight: text})}
              />

              <Text style={styles.formLabel}>Length</Text>
              <TextInput
                style={styles.formInput}
                placeholder="e.g., 18 inches"
                value={catchDetails.length}
                onChangeText={(text) => setCatchDetails({...catchDetails, length: text})}
              />

              <Text style={styles.formLabel}>Location</Text>
              <TextInput
                style={styles.formInput}
                placeholder="e.g., Lake Michigan"
                value={catchDetails.location}
                onChangeText={(text) => setCatchDetails({...catchDetails, location: text})}
              />

              <Text style={styles.formLabel}>Notes</Text>
              <TextInput
                style={[styles.formInput, styles.formTextArea]}
                placeholder="Add any notes about this catch..."
                value={catchDetails.notes}
                onChangeText={(text) => setCatchDetails({...catchDetails, notes: text})}
                multiline
                numberOfLines={4}
              />
            </View>
          </ScrollView>

          <View style={styles.modalActions}>
            <TouchableOpacity
              style={styles.cancelButton}
              onPress={() => setAddCatchModalVisible(false)}
            >
              <Text style={styles.cancelButtonText}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.saveButton}
              onPress={saveCatch}
            >
              <Text style={styles.saveButtonText}>Save Catch</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* View Catch Modal */}
      <Modal
        visible={viewCatchModalVisible}
        animationType="fade"
        transparent={true}
      >
        <View style={styles.catchViewModal}>
          <TouchableOpacity
            style={styles.catchViewBackdrop}
            onPress={() => setViewCatchModalVisible(false)}
          />
          {selectedCatch && (
            <View style={styles.catchViewContainer}>
              <Image source={{ uri: selectedCatch.imageUri }} style={styles.catchViewImage} />
              
              <View style={styles.catchViewDetails}>
                {selectedCatch.fishSpecies && (
                  <Text style={styles.catchViewText}>🐟 {selectedCatch.fishSpecies}</Text>
                )}
                {selectedCatch.weight && (
                  <Text style={styles.catchViewText}>⚖️ {selectedCatch.weight}</Text>
                )}
                {selectedCatch.length && (
                  <Text style={styles.catchViewText}>📏 {selectedCatch.length}</Text>
                )}
                {selectedCatch.location && (
                  <Text style={styles.catchViewText}>📍 {selectedCatch.location}</Text>
                )}
                {selectedCatch.notes && (
                  <Text style={styles.catchViewText}>📝 {selectedCatch.notes}</Text>
                )}
                <Text style={styles.catchViewDate}>
                  {new Date(selectedCatch.timestamp).toLocaleDateString()}
                </Text>
              </View>

              <View style={styles.catchViewActions}>
                <TouchableOpacity
                  style={styles.catchDeleteButton}
                  onPress={() => handleDeleteCatch(selectedCatch.id)}
                >
                  <Ionicons name="trash" size={20} color="white" />
                  <Text style={styles.catchDeleteButtonText}>Delete</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.catchCloseButton}
                  onPress={() => setViewCatchModalVisible(false)}
                >
                  <Text style={styles.catchCloseButtonText}>Close</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    backgroundColor: 'white',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
    flexDirection: 'row',
  },
  lureImage: {
    width: 100,
    height: 100,
    borderRadius: 10,
    marginRight: 15,
  },
  headerInfo: {
    flex: 1,
    justifyContent: 'center',
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
    marginBottom: 3,
  },
  analysisDate: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  section: {
    backgroundColor: 'white',
    margin: 10,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginLeft: 8,
  },
  sectionContent: {
    fontSize: 16,
    color: '#34495e',
    lineHeight: 24,
  },
  listContainer: {
    marginLeft: 5,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 5,
  },
  bullet: {
    fontSize: 16,
    color: '#3498db',
    marginRight: 8,
    marginTop: 2,
  },
  listText: {
    fontSize: 16,
    color: '#34495e',
    flex: 1,
    lineHeight: 22,
  },
  conditionsGrid: {
    marginLeft: 5,
  },
  conditionItem: {
    marginBottom: 8,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#ecf0f1',
  },
  conditionLabel: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 2,
  },
  conditionValue: {
    fontSize: 16,
    color: '#34495e',
    marginLeft: 10,
  },
  actionButtons: {
    padding: 20,
  },
  deleteButton: {
    backgroundColor: '#e74c3c',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 10,
  },
  deleteButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  bottomSpacer: {
    height: 50,
  },
  catchThumbnail: {
    marginRight: 15,
    alignItems: 'center',
  },
  catchImage: {
    width: 120,
    height: 120,
    borderRadius: 10,
    marginBottom: 5,
  },
  catchDate: {
    fontSize: 12,
    color: '#7f8c8d',
  },
  noCatchesText: {
    fontSize: 16,
    color: '#7f8c8d',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  addCatchButton: {
    backgroundColor: '#27ae60',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 10,
    marginTop: 15,
  },
  addCatchButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  modalContainer: {
    flex: 1,
    backgroundColor: 'white',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  modalContent: {
    flex: 1,
    padding: 20,
  },
  photoSection: {
    marginBottom: 20,
  },
  catchPhotoPreview: {
    width: '100%',
    height: 250,
    borderRadius: 10,
    marginBottom: 15,
  },
  photoPlaceholder: {
    width: '100%',
    height: 250,
    backgroundColor: '#ecf0f1',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  photoPlaceholderText: {
    fontSize: 16,
    color: '#95a5a6',
    marginTop: 10,
  },
  photoButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  photoButton: {
    flex: 1,
    backgroundColor: '#3498db',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 12,
    borderRadius: 10,
    marginHorizontal: 5,
  },
  photoButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  formSection: {
    marginBottom: 20,
  },
  formLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 8,
    marginTop: 15,
  },
  formInput: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e9ecef',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    color: '#2c3e50',
  },
  formTextArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  modalActions: {
    flexDirection: 'row',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  cancelButton: {
    flex: 1,
    backgroundColor: '#ecf0f1',
    padding: 15,
    borderRadius: 10,
    marginRight: 10,
    alignItems: 'center',
  },
  cancelButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  saveButton: {
    flex: 1,
    backgroundColor: '#27ae60',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  saveButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  catchViewModal: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  catchViewBackdrop: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  catchViewContainer: {
    width: '90%',
    backgroundColor: 'white',
    borderRadius: 15,
    overflow: 'hidden',
  },
  catchViewImage: {
    width: '100%',
    height: 300,
  },
  catchViewDetails: {
    padding: 20,
  },
  catchViewText: {
    fontSize: 16,
    color: '#2c3e50',
    marginBottom: 8,
  },
  catchViewDate: {
    fontSize: 14,
    color: '#7f8c8d',
    marginTop: 10,
  },
  catchViewActions: {
    flexDirection: 'row',
    padding: 15,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  catchDeleteButton: {
    flex: 1,
    backgroundColor: '#e74c3c',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 12,
    borderRadius: 10,
    marginRight: 10,
  },
  catchDeleteButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 5,
  },
  catchCloseButton: {
    flex: 1,
    backgroundColor: '#95a5a6',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 12,
    borderRadius: 10,
  },
  catchCloseButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
});
