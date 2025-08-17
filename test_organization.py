#!/usr/bin/env python3
"""
Test script to demonstrate the new organized file structure
"""

from lure_classifier import FishingLureClassifier
import numpy as np
import cv2
import os
import time

def test_organized_storage():
    """Test the new organized storage system"""
    print("🗂️ Testing Organized File Storage System")
    print("=" * 50)
    
    # Initialize classifier
    classifier = FishingLureClassifier()
    
    # Create a test image
    test_image = np.zeros((300, 200, 3), dtype=np.uint8)
    cv2.rectangle(test_image, (50, 100), (150, 250), (0, 255, 0), -1)
    cv2.circle(test_image, (100, 75), 25, (255, 0, 0), -1)
    
    # Save test image
    test_image_path = "test_organized.jpg"
    cv2.imwrite(test_image_path, test_image)
    
    print(f"📸 Created test image: {test_image_path}")
    
    # Analyze multiple times to create different results
    for i in range(3):
        print(f"\n🔍 Analysis #{i+1}:")
        
        # Analyze the image
        results = classifier.analyze_image(test_image_path)
        
        if "error" not in results:
            print(f"   Predicted: {results['predicted_lure_type']}")
            print(f"   Confidence: {results['confidence']:.1%}")
            
            # Save results (this will create organized structure)
            json_path = classifier.save_analysis_to_json(results)
            print(f"   Saved to: {json_path}")
            
            # Wait a bit to create different timestamps
            time.sleep(1)
        else:
            print(f"   Error: {results['error']}")
    
    # Clean up test image
    os.remove(test_image_path)
    
    # List all results
    print(f"\n📊 Listing all analysis results:")
    all_results = classifier.list_analysis_results()
    
    if all_results:
        print(f"   Found {len(all_results)} result files:")
        for result in all_results:
            print(f"   📁 {result['date']}/{result['filename']} ({result['size_bytes']} bytes)")
            print(f"      Created: {result['created']}")
    else:
        print("   No results found")
    
    # Show directory structure
    print(f"\n📁 Directory structure:")
    results_dir = "analysis_results"
    if os.path.exists(results_dir):
        for date_dir in os.listdir(results_dir):
            full_date_dir = os.path.join(results_dir, date_dir)
            if os.path.isdir(full_date_dir):
                json_files = [f for f in os.listdir(full_date_dir) if f.endswith('.json')]
                print(f"   📅 {date_dir}/ ({len(json_files)} files)")
                for json_file in json_files[:3]:  # Show first 3 files
                    print(f"      📄 {json_file}")
                if len(json_files) > 3:
                    print(f"      ... and {len(json_files) - 3} more")
    else:
        print("   No results directory found")
    
    print(f"\n✅ Organization test completed!")
    print(f"💡 Check the 'analysis_results' folder to see the organized structure")

if __name__ == "__main__":
    test_organized_storage()
