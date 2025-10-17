import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  Alert,
  RefreshControl,
  TextInput,
  Modal,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import { getTackleBox, deleteLureFromTackleBox, toggleFavorite } from '../services/storageService';
import { getUserLureAnalyses, deleteLureAnalysis } from '../services/supabaseService';
import { useAuth } from '../contexts/AuthContext';

export default function TackleBoxScreen({ navigation }) {
  const [lures, setLures] = useState([]);
  const [filteredLures, setFilteredLures] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterModalVisible, setFilterModalVisible] = useState(false);
  const [selectedFilters, setSelectedFilters] = useState({
    lureType: '',
    targetSpecies: '',
    confidence: '',
    showFavoritesOnly: false,
  });
  const [useSupabase, setUseSupabase] = useState(true); // Use Supabase by default
  const { user } = useAuth();

  const loadTackleBox = async () => {
    try {
      if (__DEV__) {
        console.log('Loading tackle box...');
      }
      
      let tackleBoxData = [];
      
      // Try Supabase first if user is logged in
      if (user && useSupabase) {
        try {
          tackleBoxData = await getUserLureAnalyses();
          console.log('[TackleBox] Loaded from Supabase:', tackleBoxData.length, 'lures');
        } catch (supabaseError) {
          console.log('[TackleBox] Supabase failed, falling back to local:', supabaseError.message);
          // Fallback to local storage
          tackleBoxData = await getTackleBox();
        }
      } else {
        // Use local storage
        tackleBoxData = await getTackleBox();
        console.log('[TackleBox] Loaded from local storage:', tackleBoxData.length, 'lures');
      }
      
      setLures(tackleBoxData);
      setFilteredLures(tackleBoxData);
    } catch (error) {
      if (__DEV__) {
        console.error('Error loading tackle box:', error);
      }
      Alert.alert('Error', 'Failed to load tackle box');
    }
  };

  const applyFilters = () => {
    let filtered = lures;

    // Favorites filter
    if (selectedFilters.showFavoritesOnly) {
      filtered = filtered.filter(lure => lure.isFavorite === true);
    }

    // Search filter
    if (searchQuery.trim()) {
      filtered = filtered.filter(lure =>
        lure.lure_type?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lure.lure_details?.target_species?.some(species => 
          species.toLowerCase().includes(searchQuery.toLowerCase())
        ) ||
        lure.chatgpt_analysis?.target_species?.some(species => 
          species.toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
    }

    // Lure type filter
    if (selectedFilters.lureType) {
      filtered = filtered.filter(lure => 
        lure.lure_type?.toLowerCase().includes(selectedFilters.lureType.toLowerCase())
      );
    }

    // Target species filter
    if (selectedFilters.targetSpecies) {
      filtered = filtered.filter(lure => {
        const targetSpecies = lure.lure_details?.target_species || lure.chatgpt_analysis?.target_species || [];
        return targetSpecies.some(species => 
          species.toLowerCase().includes(selectedFilters.targetSpecies.toLowerCase())
        );
      });
    }

    // Confidence filter
    if (selectedFilters.confidence) {
      const minConfidence = parseInt(selectedFilters.confidence);
      filtered = filtered.filter(lure => {
        const confidence = lure.confidence || lure.chatgpt_analysis?.confidence || 0;
        return confidence >= minConfidence;
      });
    }

    setFilteredLures(filtered);
    setFilterModalVisible(false);
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedFilters({
      lureType: '',
      targetSpecies: '',
      confidence: '',
      showFavoritesOnly: false,
    });
    setFilteredLures(lures);
  };

  const handleToggleFavorite = async (lureId) => {
    try {
      await toggleFavorite(lureId);
      await loadTackleBox();
    } catch (error) {
      if (__DEV__) {
        console.error('Error toggling favorite:', error);
      }
      Alert.alert('Error', 'Failed to update favorite status');
    }
  };

  const getUniqueValues = (key, subKey) => {
    const values = new Set();
    lures.forEach(lure => {
      let value;
      if (subKey) {
        value = lure[key]?.[subKey];
      } else {
        value = lure[key];
      }
      if (Array.isArray(value)) {
        value.forEach(v => values.add(v));
      } else if (value) {
        values.add(value);
      }
    });
    return Array.from(values).sort();
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadTackleBox();
    setRefreshing(false);
  };

  const deleteLure = async (id) => {
    Alert.alert(
      'Delete Lure',
      'Are you sure you want to delete this lure from your tackle box?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteLureFromTackleBox(id);
              await loadTackleBox();
              Alert.alert('Success', 'Lure deleted from tackle box');
            } catch (error) {
              if (__DEV__) {
                console.error('Error deleting lure:', error);
              }
              Alert.alert('Error', 'Failed to delete lure');
            }
          },
        },
      ]
    );
  };

  useEffect(() => {
    loadTackleBox();
  }, []);

  // Refresh tackle box when screen comes into focus
  useFocusEffect(
    React.useCallback(() => {
      loadTackleBox();
    }, [])
  );

  useEffect(() => {
    applyFilters();
  }, [searchQuery, selectedFilters, lures]);

  const renderLureItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.lureCard}
      onPress={() => navigation.navigate('LureDetail', { lure: item })}
    >
      {item.imageUri && (
        <Image source={{ uri: item.imageUri }} style={styles.lureImage} />
      )}
      <View style={styles.lureInfo}>
        <View style={styles.lureHeader}>
          <Text style={styles.lureType}>{item.lure_type || 'Unknown Lure'}</Text>
          <TouchableOpacity
            onPress={(e) => {
              e.stopPropagation();
              handleToggleFavorite(item.id);
            }}
            style={styles.favoriteButton}
          >
            <Ionicons 
              name={item.isFavorite ? "heart" : "heart-outline"} 
              size={24} 
              color={item.isFavorite ? "#e74c3c" : "#95a5a6"} 
            />
          </TouchableOpacity>
        </View>
        <Text style={styles.confidence}>
          Confidence: {item.confidence || item.chatgpt_analysis?.confidence || 'N/A'}%
        </Text>
        <Text style={styles.targetSpecies}>
          Target: {item.lure_details?.target_species?.join(', ') || 
                   item.chatgpt_analysis?.target_species?.join(', ') || 'Various'}
        </Text>
        {item.catchCount > 0 && (
          <View style={styles.catchBadge}>
            <Ionicons name="fish" size={16} color="#27ae60" />
            <Text style={styles.catchCount}>{item.catchCount} catch{item.catchCount !== 1 ? 'es' : ''}</Text>
          </View>
        )}
        <Text style={styles.timestamp}>
          {new Date(item.analysis_date || Date.now()).toLocaleDateString()}
        </Text>
      </View>
      <TouchableOpacity
        style={styles.deleteButton}
        onPress={(e) => {
          e.stopPropagation();
          deleteLure(item.id);
        }}
      >
        <Ionicons name="trash" size={20} color="white" />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  const renderFilterModal = () => (
    <Modal
      visible={filterModalVisible}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>🔍 Filter & Search</Text>
          <TouchableOpacity
            onPress={() => setFilterModalVisible(false)}
            style={styles.closeButton}
          >
            <Ionicons name="close" size={24} color="#2c3e50" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.modalContent}>
          {/* Favorites Filter */}
          <View style={styles.filterSection}>
            <TouchableOpacity
              style={[
                styles.favoritesToggle,
                selectedFilters.showFavoritesOnly && styles.favoritesToggleActive
              ]}
              onPress={() => setSelectedFilters({
                ...selectedFilters,
                showFavoritesOnly: !selectedFilters.showFavoritesOnly
              })}
            >
              <Ionicons 
                name={selectedFilters.showFavoritesOnly ? "heart" : "heart-outline"} 
                size={24} 
                color={selectedFilters.showFavoritesOnly ? "#e74c3c" : "#2c3e50"} 
              />
              <Text style={[
                styles.favoritesToggleText,
                selectedFilters.showFavoritesOnly && styles.favoritesToggleTextActive
              ]}>
                Show Favorites Only
              </Text>
            </TouchableOpacity>
          </View>

          {/* Search */}
          <View style={styles.filterSection}>
            <Text style={styles.filterLabel}>🔎 Search</Text>
            <TextInput
              style={styles.searchInput}
              placeholder="Search by lure type, fish species..."
              value={searchQuery}
              onChangeText={setSearchQuery}
            />
          </View>

          {/* Lure Type Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterLabel}>🎣 Lure Type</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <TouchableOpacity
                style={[
                  styles.filterChip,
                  selectedFilters.lureType === '' && styles.filterChipActive
                ]}
                onPress={() => setSelectedFilters({...selectedFilters, lureType: ''})}
              >
                <Text style={styles.filterChipText}>All</Text>
              </TouchableOpacity>
              {getUniqueValues('lure_type').map((type, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.filterChip,
                    selectedFilters.lureType === type && styles.filterChipActive
                  ]}
                  onPress={() => setSelectedFilters({...selectedFilters, lureType: type})}
                >
                  <Text style={styles.filterChipText}>{type}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>

          {/* Target Species Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterLabel}>🐟 Target Species</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <TouchableOpacity
                style={[
                  styles.filterChip,
                  selectedFilters.targetSpecies === '' && styles.filterChipActive
                ]}
                onPress={() => setSelectedFilters({...selectedFilters, targetSpecies: ''})}
              >
                <Text style={styles.filterChipText}>All</Text>
              </TouchableOpacity>
              {getUniqueValues('lure_details', 'target_species').concat(
                getUniqueValues('chatgpt_analysis', 'target_species')
              ).filter((value, index, self) => self.indexOf(value) === index).map((species, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.filterChip,
                    selectedFilters.targetSpecies === species && styles.filterChipActive
                  ]}
                  onPress={() => setSelectedFilters({...selectedFilters, targetSpecies: species})}
                >
                  <Text style={styles.filterChipText}>{species}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>

          {/* Confidence Filter */}
          <View style={styles.filterSection}>
            <Text style={styles.filterLabel}>📊 Minimum Confidence</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <TouchableOpacity
                style={[
                  styles.filterChip,
                  selectedFilters.confidence === '' && styles.filterChipActive
                ]}
                onPress={() => setSelectedFilters({...selectedFilters, confidence: ''})}
              >
                <Text style={styles.filterChipText}>All</Text>
              </TouchableOpacity>
              {['70', '80', '90', '95'].map((confidence, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.filterChip,
                    selectedFilters.confidence === confidence && styles.filterChipActive
                  ]}
                  onPress={() => setSelectedFilters({...selectedFilters, confidence})}
                >
                  <Text style={styles.filterChipText}>{confidence}%+</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </ScrollView>

        <View style={styles.modalActions}>
          <TouchableOpacity style={styles.clearButton} onPress={clearFilters}>
            <Text style={styles.clearButtonText}>Clear All</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.applyButton} onPress={applyFilters}>
            <Text style={styles.applyButtonText}>Apply Filters</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>🎒 My Tackle Box</Text>
          <Text style={styles.subtitle}>
            {filteredLures.length} of {lures.length} lure{lures.length !== 1 ? 's' : ''}
          </Text>
        </View>
        <TouchableOpacity
          style={styles.filterButton}
          onPress={() => setFilterModalVisible(true)}
        >
          <Ionicons name="filter" size={24} color="#2c3e50" />
        </TouchableOpacity>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#7f8c8d" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search your tackle box..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        {searchQuery.length > 0 && (
          <TouchableOpacity onPress={() => setSearchQuery('')}>
            <Ionicons name="close-circle" size={20} color="#7f8c8d" />
          </TouchableOpacity>
        )}
      </View>

      {/* Lures List */}
      {filteredLures.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>🎣</Text>
          <Text style={styles.emptyTitle}>
            {lures.length === 0 ? 'No lures yet!' : 'No matching lures'}
          </Text>
          <Text style={styles.emptySubtitle}>
            {lures.length === 0 
              ? 'Start by analyzing your first lure from the Home tab'
              : 'Try adjusting your search or filters'
            }
          </Text>
        </View>
      ) : (
        <FlatList
          data={filteredLures}
          renderItem={renderLureItem}
          keyExtractor={(item) => item.id.toString()}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          contentContainerStyle={styles.listContainer}
        />
      )}

      {renderFilterModal()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  subtitle: {
    fontSize: 14,
    color: '#7f8c8d',
    marginTop: 2,
  },
  filterButton: {
    padding: 10,
    backgroundColor: '#ecf0f1',
    borderRadius: 20,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'white',
    margin: 15,
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  searchIcon: {
    marginRight: 10,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#2c3e50',
  },
  listContainer: {
    padding: 15,
  },
  lureCard: {
    backgroundColor: 'white',
    borderRadius: 15,
    marginBottom: 15,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lureImage: {
    width: 80,
    height: 80,
    borderRadius: 10,
    marginRight: 15,
  },
  lureInfo: {
    flex: 1,
  },
  lureHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  lureType: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    flex: 1,
  },
  favoriteButton: {
    padding: 4,
  },
  catchBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#d5f4e6',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginTop: 4,
  },
  catchCount: {
    fontSize: 14,
    color: '#27ae60',
    fontWeight: '600',
    marginLeft: 4,
  },
  confidence: {
    fontSize: 14,
    color: '#27ae60',
    marginBottom: 2,
  },
  targetSpecies: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 2,
  },
  timestamp: {
    fontSize: 12,
    color: '#95a5a6',
  },
  deleteButton: {
    backgroundColor: '#e74c3c',
    padding: 10,
    borderRadius: 20,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 64,
    marginBottom: 20,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#7f8c8d',
    textAlign: 'center',
    lineHeight: 24,
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
  closeButton: {
    padding: 5,
  },
  modalContent: {
    flex: 1,
    padding: 20,
  },
  filterSection: {
    marginBottom: 25,
  },
  filterLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 10,
  },
  filterChip: {
    backgroundColor: '#ecf0f1',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    marginRight: 10,
  },
  filterChipActive: {
    backgroundColor: '#3498db',
  },
  filterChipText: {
    fontSize: 14,
    color: '#2c3e50',
  },
  modalActions: {
    flexDirection: 'row',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  clearButton: {
    flex: 1,
    backgroundColor: '#ecf0f1',
    padding: 15,
    borderRadius: 10,
    marginRight: 10,
    alignItems: 'center',
  },
  clearButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  applyButton: {
    flex: 1,
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  applyButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  favoritesToggle: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ecf0f1',
    padding: 15,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  favoritesToggleActive: {
    backgroundColor: '#ffe5e5',
    borderColor: '#e74c3c',
  },
  favoritesToggleText: {
    fontSize: 16,
    color: '#2c3e50',
    marginLeft: 10,
    fontWeight: '600',
  },
  favoritesToggleTextActive: {
    color: '#e74c3c',
  },
});