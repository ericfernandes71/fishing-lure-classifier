#!/usr/bin/env python3
"""
Test script for the Fishing Lure Classifier
"""

from lure_classifier import FishingLureClassifier
import numpy as np
import cv2

def create_test_image():
    """Create a simple test image for testing"""
    # Create a 300x400 test image with some colors
    image = np.zeros((400, 300, 3), dtype=np.uint8)
    
    # Add some colored rectangles to simulate a lure
    cv2.rectangle(image, (50, 100), (250, 300), (0, 255, 0), -1)  # Green body
    cv2.rectangle(image, (100, 150), (200, 250), (255, 0, 0), -1)  # Blue detail
    cv2.circle(image, (150, 200), 30, (0, 0, 255), -1)  # Red circle
    
    # Save the test image
    test_image_path = "test_lure.jpg"
    cv2.imwrite(test_image_path, image)
    print(f"Created test image: {test_image_path}")
    return test_image_path

def test_classifier():
    """Test the lure classifier"""
    print("Testing Fishing Lure Classifier...")
    print("=" * 50)
    
    # Initialize classifier
    classifier = FishingLureClassifier()
    
    # Test 1: Basic functionality
    print("\n1. Testing basic classifier functionality...")
    print(f"Available lure types: {len(classifier.lure_database)}")
    print(f"Sample lure types: {list(classifier.lure_database.keys())[:5]}")
    
    # Test 2: Recommendations
    print("\n2. Testing lure recommendations...")
    conditions = {
        "season": "Summer",
        "water_clarity": "clear",
        "target_species": "Largemouth Bass"
    }
    recommendations = classifier.get_lure_recommendations(conditions)
    print(f"Top 3 recommendations for Summer bass fishing:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec['lure_type']} (Score: {rec['score']})")
    
    # Test 3: Image analysis (if test image exists)
    print("\n3. Testing image analysis...")
    try:
        test_image_path = create_test_image()
        results = classifier.analyze_image(test_image_path)
        
        if "error" not in results:
            print(f"✅ Image analysis successful!")
            print(f"   Predicted lure: {results['predicted_lure_type']}")
            print(f"   Confidence: {results['confidence']:.2f}")
            print(f"   Target species: {', '.join(results['target_species'][:3])}")
            
            # Save results to JSON
            json_path = classifier.save_analysis_to_json(results)
            print(f"   Results saved to: {json_path}")
        else:
            print(f"❌ Image analysis failed: {results['error']}")
            
    except Exception as e:
        print(f"❌ Image analysis test failed: {str(e)}")
    
    # Test 4: Lure information
    print("\n4. Testing lure information retrieval...")
    lure_type = "Spinnerbait"
    lure_info = classifier.lure_database.get(lure_type)
    if lure_info:
        print(f"✅ {lure_type} information retrieved:")
        print(f"   Best seasons: {', '.join(lure_info['best_seasons'])}")
        print(f"   Target species: {', '.join(lure_info['target_species'][:3])}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_classifier()

