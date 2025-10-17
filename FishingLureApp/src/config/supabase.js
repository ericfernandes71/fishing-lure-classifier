/**
 * Supabase Configuration for Fishing Lure App
 * Cloud database, authentication, and storage
 */

import { createClient } from '@supabase/supabase-js';
import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Supabase credentials
const SUPABASE_URL = 'https://wisqqrerjbfbdiorlxtn.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indpc3FxcmVyamJmYmRpb3JseHRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2Mjc1NzEsImV4cCI6MjA3NjIwMzU3MX0.Wq0SYq1KafI_lputqfTjKzf6ruCMK9v0LoOlo6KqYxo';

// Create Supabase client
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});

// Export configuration
export const SUPABASE_CONFIG = {
  url: SUPABASE_URL,
  anonKey: SUPABASE_ANON_KEY,
  storageBucket: 'lure-images',
};

export default supabase;

