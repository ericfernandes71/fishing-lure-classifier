import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Import screens
import HomeScreen from './src/screens/HomeScreen';
import TackleBoxScreen from './src/screens/TackleBoxScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import LureDetailScreen from './src/screens/LureDetailScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function TackleBoxStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="TackleBoxList" 
        component={TackleBoxScreen} 
        options={{ title: '🎒 My Tackle Box' }}
      />
      <Stack.Screen 
        name="LureDetail" 
        component={LureDetailScreen} 
        options={{ title: '🎣 Lure Details' }}
      />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === 'Home') {
              iconName = focused ? 'camera' : 'camera-outline';
            } else if (route.name === 'TackleBox') {
              iconName = focused ? 'fish' : 'fish-outline';
            } else if (route.name === 'Settings') {
              iconName = focused ? 'settings' : 'settings-outline';
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#3498db',
          tabBarInactiveTintColor: 'gray',
          headerStyle: {
            backgroundColor: '#2c3e50',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        })}
      >
        <Tab.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ title: '🎣 Lure Analyzer' }}
        />
        <Tab.Screen 
          name="TackleBox" 
          component={TackleBoxStack} 
          options={{ title: '🎒 Tackle Box' }}
        />
        <Tab.Screen 
          name="Settings" 
          component={SettingsScreen} 
          options={{ title: '⚙️ Settings' }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});