#!/usr/bin/env python3
"""
Demo Script for the Complete Hybrid Fishing Lure Classification System
Showcases both traditional CV and ChatGPT Vision approaches
"""

import os
import cv2
import numpy as np
from enhanced_hybrid_classifier import EnhancedHybridLureClassifier
from training_pipeline import LureTrainingPipeline
import json

def demo_traditional_cv():
    """Demo traditional computer vision analysis"""
    print("🔬 Traditional Computer Vision Demo")
    print("=" * 50)
    
    # Create sample images for demo
    create_sample_images()
    
    # Initialize traditional classifier
    from lure_classifier import FishingLureClassifier
    classifier = FishingLureClassifier()
    
    # Analyze sample images
    sample_images = ["sample_spinnerbait.jpg", "sample_spoon.jpg", "sample_jerkbait.jpg"]
    
    for image_file in sample_images:
        if os.path.exists(image_file):
            print(f"\n📸 Analyzing: {image_file}")
            try:
                results = classifier.analyze_image(image_file)
                print(f"   🎯 Predicted: {results.get('predicted_lure_type', 'Unknown')}")
                print(f"   📊 Confidence: {results.get('confidence', 0):.1%}")
                
                if 'feature_analysis' in results:
                    fa = results['feature_analysis']
                    print(f"   📏 Aspect Ratio: {fa.get('aspect_ratio', 'N/A')}")
                    print(f"   🔵 Circularity: {fa.get('circularity', 'N/A')}")
                    print(f"   🔍 Edge Density: {fa.get('edge_density', 'N/A')}")
                    print(f"   ✨ Metallic Score: {fa.get('metallic_score', 'N/A')}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        else:
            print(f"   ⚠️ File not found: {image_file}")

def demo_hybrid_system(api_key: str = None):
    """Demo hybrid system (ChatGPT + CV)"""
    print("\n🚀 Hybrid System Demo (ChatGPT + Computer Vision)")
    print("=" * 50)
    
    if not api_key:
        print("⚠️ No OpenAI API key provided. Skipping ChatGPT analysis.")
        print("💡 To test ChatGPT Vision, provide your API key:")
        print("   demo_hybrid_system('your-api-key-here')")
        return
    
    try:
        # Initialize hybrid classifier
        classifier = EnhancedHybridLureClassifier(api_key)
        print("✅ Hybrid classifier initialized successfully!")
        
        # Test with sample images
        sample_images = ["sample_spinnerbait.jpg", "sample_spoon.jpg", "sample_jerkbait.jpg"]
        
        for image_file in sample_images:
            if os.path.exists(image_file):
                print(f"\n🔍 Hybrid Analysis: {image_file}")
                
                # Traditional CV analysis
                cv_result = classifier.analyze_with_traditional_cv(image_file)
                if 'cv_analysis' in cv_result:
                    cv = cv_result['cv_analysis']
                    print(f"   🔬 CV - Aspect Ratio: {cv.get('aspect_ratio', 'N/A')}")
                    print(f"   🔬 CV - Circularity: {cv.get('circularity', 'N/A')}")
                    print(f"   🔬 CV - Metallic Score: {cv.get('metallic_score', 'N/A')}")
                
                # ChatGPT analysis
                chatgpt_result = classifier.analyze_with_chatgpt(image_file)
                if 'chatgpt_analysis' in chatgpt_result:
                    cg = chatgpt_result['chatgpt_analysis']
                    print(f"   🧠 ChatGPT - Type: {cg.get('lure_type', 'Unknown')}")
                    print(f"   🧠 ChatGPT - Confidence: {cg.get('confidence', 0)}%")
                    print(f"   🧠 ChatGPT - Features: {', '.join(cg.get('visual_features', []))}")
                
                # Hybrid decision
                hybrid_result = classifier.hybrid_analysis(image_file)
                if 'hybrid_decision' in hybrid_result:
                    hd = hybrid_result['hybrid_decision']
                    print(f"   🚀 Hybrid - Final Type: {hd.get('final_lure_type', 'Unknown')}")
                    print(f"   🚀 Hybrid - Adjusted Confidence: {hd.get('adjusted_confidence', 0)}%")
                    print(f"   🚀 Hybrid - CV Validation: +{hd.get('cv_validation_score', 0)} points")
                
            else:
                print(f"   ⚠️ File not found: {image_file}")
                
    except Exception as e:
        print(f"❌ Error initializing hybrid classifier: {str(e)}")

def demo_training_pipeline(api_key: str = None):
    """Demo the training pipeline"""
    print("\n🧠 Training Pipeline Demo")
    print("=" * 50)
    
    if not api_key:
        print("⚠️ No OpenAI API key provided. Skipping training pipeline demo.")
        return
    
    try:
        # Initialize training pipeline
        pipeline = LureTrainingPipeline(api_key)
        print("✅ Training pipeline initialized successfully!")
        
        # Generate training dataset
        print("\n📊 Generating training dataset...")
        training_data = pipeline.generate_training_dataset(".")
        
        # Show dataset statistics
        print(f"\n📈 Dataset Statistics:")
        print(f"   Total samples: {training_data['total_samples']}")
        print(f"   Lure types: {list(training_data['lure_type_distribution'].keys())}")
        print(f"   Distribution: {training_data['lure_type_distribution']}")
        
        # Prepare training data
        print("\n🔧 Preparing training data...")
        X, y = pipeline.prepare_training_data(training_data, ".")
        
        print(f"   Images shape: {X.shape}")
        print(f"   Labels: {np.unique(y)}")
        
        # Create and train model (with reduced epochs for demo)
        print("\n🏗️ Creating and training model...")
        training_result = pipeline.train_model(X, y, epochs=5)  # Reduced for demo
        
        print(f"✅ Training completed!")
        print(f"   Training samples: {training_result['training_samples']}")
        print(f"   Validation samples: {training_result['validation_samples']}")
        
        # Save model
        model_file, labels_file = pipeline.save_model()
        print(f"💾 Model saved: {model_file}")
        print(f"🏷️ Labels saved: {labels_file}")
        
        # Test prediction
        if os.path.exists("sample_spinnerbait.jpg"):
            print("\n🔮 Testing prediction...")
            prediction = pipeline.predict_single_image("sample_spinnerbait.jpg")
            print(f"   Predicted: {prediction['predicted_class']}")
            print(f"   Confidence: {prediction['confidence']:.1%}")
        
    except Exception as e:
        print(f"❌ Error in training pipeline: {str(e)}")

def create_sample_images():
    """Create sample lure images for demo"""
    print("🎨 Creating sample lure images...")
    
    # Sample Spinnerbait (long, thin)
    spinnerbait = np.zeros((300, 600, 3), dtype=np.uint8)
    cv2.rectangle(spinnerbait, (100, 100), (500, 200), (0, 255, 0), -1)  # Green body
    cv2.circle(spinnerbait, (150, 150), 30, (255, 255, 0), -1)  # Yellow blade
    cv2.circle(spinnerbait, (450, 150), 30, (255, 255, 0), -1)  # Yellow blade
    cv2.imwrite("sample_spinnerbait.jpg", spinnerbait)
    
    # Sample Spoon (circular)
    spoon = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.ellipse(spoon, (150, 150), (80, 60), 0, 0, 360, (255, 215, 0), -1)  # Gold spoon
    cv2.imwrite("sample_spoon.jpg", spoon)
    
    # Sample Jerkbait (very long, thin)
    jerkbait = np.zeros((200, 600, 3), dtype=np.uint8)
    cv2.rectangle(jerkbait, (50, 75), (550, 125), (0, 0, 255), -1)  # Blue body
    cv2.rectangle(jerkbait, (100, 50), (500, 150), (0, 0, 255), -1)  # Blue body
    cv2.imwrite("sample_jerkbait.jpg", jerkbait)
    
    print("✅ Sample images created!")

def main():
    """Main demo function"""
    print("🎣 Complete Hybrid Fishing Lure Classification System Demo")
    print("=" * 60)
    
    # Create sample images
    create_sample_images()
    
    # Demo traditional CV
    demo_traditional_cv()
    
    # Demo hybrid system (without API key)
    demo_hybrid_system()
    
    # Demo training pipeline (without API key)
    demo_training_pipeline()
    
    print("\n" + "=" * 60)
    print("🎯 Demo Summary:")
    print("✅ Traditional Computer Vision - Ready to use")
    print("⏳ Hybrid System - Requires OpenAI API key")
    print("⏳ Training Pipeline - Requires OpenAI API key")
    print("\n🚀 To enable full functionality:")
    print("1. Get OpenAI API key from https://platform.openai.com/")
    print("2. Run: demo_hybrid_system('your-api-key')")
    print("3. Run: demo_training_pipeline('your-api-key')")
    print("\n🌐 Or start the Flask app: python app.py")
    print("   Then go to http://localhost:5000")

if __name__ == "__main__":
    main()
