"""
Supabase Client for Flask Backend
Handles database and storage operations
"""

from supabase import create_client, Client
import config
from typing import Dict, List, Optional
import datetime

class SupabaseService:
    def __init__(self):
        """Initialize Supabase client with service role key (backend only)"""
        if not config.SUPABASE_URL or not config.SUPABASE_SERVICE_ROLE_KEY:
            print("[WARNING] Supabase credentials not found in config")
            self.client = None
            self.enabled = False
        else:
            self.client: Client = create_client(
                config.SUPABASE_URL,
                config.SUPABASE_SERVICE_ROLE_KEY
            )
            self.enabled = True
            print("[OK] Supabase client initialized")
    
    def is_enabled(self) -> bool:
        """Check if Supabase is properly configured"""
        return self.enabled and self.client is not None
    
    # ========================================================================
    # LURE ANALYSES
    # ========================================================================
    
    def save_lure_analysis(self, user_id: str, analysis_data: Dict) -> Optional[Dict]:
        """Save lure analysis to Supabase database"""
        if not self.is_enabled():
            return None
        
        try:
            data_to_insert = {
                'user_id': user_id,
                'lure_type': analysis_data.get('lure_type'),
                'confidence': analysis_data.get('confidence'),
                'image_url': analysis_data.get('image_url'),
                'image_name': analysis_data.get('image_name'),
                'image_path': analysis_data.get('image_path'),
                'analysis_method': analysis_data.get('analysis_method', 'ChatGPT Vision API'),
                'chatgpt_analysis': analysis_data.get('chatgpt_analysis', {}),
                'lure_details': analysis_data.get('lure_details', {}),
                'api_cost_usd': analysis_data.get('api_cost_usd'),
                'tokens_used': analysis_data.get('tokens_used'),
            }
            
            response = self.client.table('lure_analyses').insert(data_to_insert).execute()
            print(f"[OK] Saved lure analysis to Supabase for user {user_id}")
            return response.data[0] if response.data else None
            
        except Exception as e:
            print(f"[ERROR] Failed to save to Supabase: {str(e)}")
            return None
    
    def get_user_lure_analyses(self, user_id: str) -> List[Dict]:
        """Get all lure analyses for a user"""
        if not self.is_enabled():
            return []
        
        try:
            response = self.client.table('lure_analyses')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"[ERROR] Failed to get analyses from Supabase: {str(e)}")
            return []
    
    def get_lure_analysis_by_id(self, analysis_id: str, user_id: str) -> Optional[Dict]:
        """Get single lure analysis by ID"""
        if not self.is_enabled():
            return None
        
        try:
            response = self.client.table('lure_analyses')\
                .select('*')\
                .eq('id', analysis_id)\
                .eq('user_id', user_id)\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            print(f"[ERROR] Failed to get analysis from Supabase: {str(e)}")
            return None
    
    def delete_lure_analysis(self, analysis_id: str, user_id: str) -> bool:
        """Delete a lure analysis"""
        if not self.is_enabled():
            return False
        
        try:
            self.client.table('lure_analyses')\
                .delete()\
                .eq('id', analysis_id)\
                .eq('user_id', user_id)\
                .execute()
            
            print(f"[OK] Deleted lure analysis {analysis_id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to delete from Supabase: {str(e)}")
            return False
    
    def bulk_delete_lure_analyses(self, analysis_ids: List[str], user_id: str) -> int:
        """Bulk delete lure analyses"""
        if not self.is_enabled():
            return 0
        
        deleted_count = 0
        for analysis_id in analysis_ids:
            if self.delete_lure_analysis(analysis_id, user_id):
                deleted_count += 1
        
        return deleted_count
    
    # ========================================================================
    # STORAGE
    # ========================================================================
    
    def upload_lure_image(self, user_id: str, file_path: str, file_name: str) -> Optional[str]:
        """Upload lure image to Supabase Storage"""
        if not self.is_enabled():
            return None
        
        try:
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Upload to storage with user-specific path
            storage_path = f"{user_id}/{file_name}"
            
            self.client.storage.from_('lure-images').upload(
                storage_path,
                file_data,
                file_options={"content-type": "image/jpeg"}
            )
            
            # Get public URL
            public_url = self.client.storage.from_('lure-images').get_public_url(storage_path)
            
            print(f"[OK] Uploaded image to Supabase Storage: {storage_path}")
            return public_url
            
        except Exception as e:
            print(f"[ERROR] Failed to upload to Supabase Storage: {str(e)}")
            return None
    
    def delete_lure_image(self, storage_path: str) -> bool:
        """Delete lure image from Supabase Storage"""
        if not self.is_enabled():
            return False
        
        try:
            self.client.storage.from_('lure-images').remove([storage_path])
            print(f"[OK] Deleted image from Supabase Storage: {storage_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to delete from Supabase Storage: {str(e)}")
            return False
    
    # ========================================================================
    # USER PROFILE
    # ========================================================================
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile"""
        if not self.is_enabled():
            return None
        
        try:
            response = self.client.table('profiles')\
                .select('*')\
                .eq('id', user_id)\
                .single()\
                .execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            print(f"[ERROR] Failed to get profile from Supabase: {str(e)}")
            return None
    
    def update_user_profile(self, user_id: str, updates: Dict) -> bool:
        """Update user profile"""
        if not self.is_enabled():
            return False
        
        try:
            self.client.table('profiles')\
                .update(updates)\
                .eq('id', user_id)\
                .execute()
            
            print(f"[OK] Updated profile for user {user_id}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to update profile: {str(e)}")
            return False

# Global Supabase service instance
supabase_service = SupabaseService()

