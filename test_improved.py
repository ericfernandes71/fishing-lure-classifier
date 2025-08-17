#!/usr/bin/env python3
"""
Test script for the IMPROVED Fishing Lure Classifier
This version actually analyzes images instead of random guessing!
"""

from lure_classifier import FishingLureClassifier
import numpy as np
import cv2

def create_test_lures():
    """Create different types of test lures to demonstrate the classifier"""
    test_images = {}
    
    # 1. Spinnerbait - long and thin with metallic parts
    spinnerbait = np.zeros((400, 200, 3), dtype=np.uint8)
    cv2.rectangle(spinnerbait, (50, 100), (150, 300), (0, 255, 0), -1)  # Green body
    cv2.rectangle(spinnerbait, (150, 150), (180, 250), (255, 255, 0), -1)  # Metallic blade
    cv2.circle(spinnerbait, (100, 80), 20, (255, 0, 0), -1)  # Blue head
    test_images["spinnerbait.jpg"] = spinnerbait
    
    # 2. Spoon - circular and metallic
    spoon = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.ellipse(spoon, (150, 150), (100, 60), 0, 0, 360, (255, 255, 0), -1)  # Metallic oval
    cv2.ellipse(spoon, (150, 150), (80, 40), 0, 0, 360, (255, 255, 255), -1)  # White highlight
    test_images["spoon.jpg"] = spoon
    
    # 3. Jerkbait - very long and thin
    jerkbait = np.zeros((500, 150, 3), dtype=np.uint8)
    cv2.rectangle(jerkbait, (50, 200), (100, 300), (0, 0, 255), -1)  # Red body
    cv2.rectangle(jerkbait, (100, 220), (120, 280), (255, 255, 255), -1)  # White detail
    cv2.rectangle(jerkbait, (120, 240), (130, 260), (0, 255, 255), -1)  # Yellow tail
    test_images["jerkbait.jpg"] = jerkbait
    
    # 4. Topwater - wide and flat
    topwater = np.zeros((200, 400, 3), dtype=np.uint8)
    cv2.rectangle(topwater, (50, 75), (350, 125), (255, 0, 0), -1)  # Blue body
    cv2.rectangle(topwater, (150, 50), (250, 75), (255, 255, 0), -1)  # Yellow top
    cv2.circle(topwater, (200, 100), 15, (255, 255, 255), -1)  # White eye
    test_images["topwater.jpg"] = topwater
    
    # 5. Worm - very long and thin
    worm = np.zeros((600, 100, 3), dtype=np.uint8)
    cv2.rectangle(worm, (25, 100), (75, 500), (0, 100, 0), -1)  # Dark green body
    cv2.ellipse(worm, (50, 100), (25, 15), 0, 0, 360, (0, 150, 0), -1)  # Green head
    cv2.ellipse(worm, (50, 500), (20, 10), 0, 0, 360, (0, 100, 0), -1)  # Green tail
    test_images["worm.jpg"] = worm
    
    return test_images

def test_improved_classifier():
    """Test the improved lure classifier"""
    print("🎣 Testing IMPROVED Fishing Lure Classifier")
    print("=" * 60)
    print("This version actually analyzes images instead of random guessing!")
    print()
    
    # Initialize classifier
    classifier = FishingLureClassifier()
    
    # Create test images
    print("📸 Creating test lure images...")
    test_images = create_test_lures()
    
    # Test each image
    for filename, image in test_images.items():
        print(f"\n🔍 Testing: {filename}")
        print("-" * 40)
        
        # Save the test image
        cv2.imwrite(filename, image)
        
        try:
            # Analyze the image
            results = classifier.analyze_image(filename)
            
            if "error" not in results:
                print(f"✅ Classification: {results['predicted_lure_type']}")
                print(f"   Confidence: {results['confidence']:.1%}")
                print(f"   Image Size: {results['image_dimensions']}")
                
                # Show feature analysis
                if results.get('feature_analysis'):
                    fa = results['feature_analysis']
                    print(f"   Shape: Aspect={fa['shape_features'].get('aspect_ratio', 'N/A')}, "
                          f"Circularity={fa['shape_features'].get('circularity', 'N/A')}")
                    print(f"   Color: Metallic={fa['color_features'].get('metallic_score', 'N/A')}, "
                          f"Pattern={fa['color_features'].get('color_pattern', 'N/A')}")
                    
                    if fa.get('analysis_notes'):
                        print(f"   Notes: {fa['analysis_notes']}")
                
                # Show lure info
                print(f"   Target: {', '.join(results['target_species'][:3])}")
                print(f"   Seasons: {', '.join(results['best_seasons'])}")
                
            else:
                print(f"❌ Analysis failed: {results['error']}")
                
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n💡 Now you can see WHY the classifier made each decision!")
    print("   - Shape features (aspect ratio, circularity, edges)")
    print("   - Color features (metallic effects, color patterns)")
    print("   - Analysis notes explaining the reasoning")

if __name__ == "__main__":
    test_improved_classifier()

