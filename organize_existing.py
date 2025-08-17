#!/usr/bin/env python3
"""
Script to organize existing JPG files and their analysis results
"""

import os
import shutil
import datetime
from lure_classifier import FishingLureClassifier

def organize_existing_files():
    """Organize existing JPG files and move them to the organized structure"""
    print("🗂️ Organizing Existing Files")
    print("=" * 50)
    
    # Files to organize
    jpg_files = [
        "worm.jpg", "topwater.jpg", "jerkbait.jpg", 
        "spoon.jpg", "spinnerbait.jpg", "test_lure.jpg"
    ]
    
    # Create organized directory structure
    results_dir = "analysis_results"
    today = datetime.datetime.now()
    date_dir = today.strftime("%Y-%m-%d")
    full_results_dir = os.path.join(results_dir, date_dir)
    os.makedirs(full_results_dir, exist_ok=True)
    
    print(f"📁 Organizing files into: {full_results_dir}")
    
    # Move and analyze each JPG file
    for jpg_file in jpg_files:
        if os.path.exists(jpg_file):
            print(f"\n🔍 Processing: {jpg_file}")
            
            try:
                # Analyze the image
                classifier = FishingLureClassifier()
                results = classifier.analyze_image(jpg_file)
                
                if "error" not in results:
                    print(f"   ✅ Analysis successful: {results['predicted_lure_type']}")
                    
                    # Save results to organized structure
                    json_path = classifier.save_analysis_to_json(results)
                    print(f"   📄 Results saved to: {json_path}")
                    
                    # Move the JPG file to organized structure
                    jpg_dest = os.path.join(full_results_dir, jpg_file)
                    shutil.move(jpg_file, jpg_dest)
                    print(f"   🖼️ Image moved to: {jpg_dest}")
                    
                else:
                    print(f"   ❌ Analysis failed: {results['error']}")
                    
            except Exception as e:
                print(f"   ❌ Error processing {jpg_file}: {str(e)}")
        else:
            print(f"   ⚠️ File not found: {jpg_file}")
    
    # Clean up old JSON files in root directory
    print(f"\n🧹 Cleaning up old JSON files...")
    old_json_files = [f for f in os.listdir('.') if f.endswith('_analysis.json')]
    
    for json_file in old_json_files:
        try:
            os.remove(json_file)
            print(f"   🗑️ Removed: {json_file}")
        except Exception as e:
            print(f"   ❌ Could not remove {json_file}: {str(e)}")
    
    # Show final organized structure
    print(f"\n📊 Final organized structure:")
    if os.path.exists(results_dir):
        for date_dir in os.listdir(results_dir):
            full_date_dir = os.path.join(results_dir, date_dir)
            if os.path.isdir(full_date_dir):
                jpg_files = [f for f in os.listdir(full_date_dir) if f.endswith('.jpg')]
                json_files = [f for f in os.listdir(full_date_dir) if f.endswith('.json')]
                print(f"   📅 {date_dir}/")
                print(f"      🖼️ Images: {len(jpg_files)}")
                print(f"      📄 Results: {len(json_files)}")
    
    print(f"\n✅ Organization completed!")
    print(f"💡 All files are now organized in the 'analysis_results' folder")

if __name__ == "__main__":
    organize_existing_files()
