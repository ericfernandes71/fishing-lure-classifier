import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function LureDetailScreen({ route, navigation }) {
  const { lure } = route.params;

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

  return (
    <ScrollView style={styles.container}>
      {/* Header with Image */}
      <View style={styles.header}>
        {lure.imageUri && (
          <Image source={{ uri: lure.imageUri }} style={styles.lureImage} />
        )}
        <View style={styles.headerInfo}>
          <Text style={styles.lureType}>{lure.lure_type || 'Unknown Lure'}</Text>
          <Text style={styles.confidence}>
            Confidence: {lure.confidence || lure.chatgpt_analysis?.confidence || 'N/A'}%
          </Text>
          <Text style={styles.analysisDate}>
            Analyzed: {new Date(lure.analysis_date || Date.now()).toLocaleDateString()}
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

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
          <Ionicons name="trash" size={20} color="white" />
          <Text style={styles.deleteButtonText}>Delete from Tackle Box</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.bottomSpacer} />
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
});
