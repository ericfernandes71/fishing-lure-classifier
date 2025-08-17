#!/usr/bin/env python3
"""
Hybrid Lure Classifier: ChatGPT Vision + Traditional Computer Vision
"""

import cv2
import numpy as np
import json
import os
import requests
from typing import Dict, List, Tuple
import base64
from PIL import Image
import io

class HybridLureClassifier:
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.lure_database = self._initialize_lure_database()
        
    def _initialize_lure_database(self) -> Dict:
        """Initialize comprehensive database of fishing lure characteristics"""
        return {
            "Spinnerbait": {
                "description": "Long, thin lure with metallic spinning blades, typically has a jig head and skirt",
                "visual_features": ["spinning blades", "long body", "metallic parts", "jig head", "skirt"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Northern Pike"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "2-15"
                }
            },
            "Crankbait": {
                "description": "Rectangular body with diving lip, mimics baitfish swimming",
                "visual_features": ["diving lip", "rectangular body", "fish-like shape", "hooks"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Walleye"],
                "best_seasons": ["Spring", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "50-75",
                    "depth_ft": "2-8"
                }
            },
            "Spoon": {
                "description": "Oval or teardrop shaped metallic lure that wobbles and flashes",
                "visual_features": ["oval shape", "metallic surface", "teardrop", "wobbling action"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Northern Pike"],
                "best_seasons": ["Fall", "Winter", "Spring"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "35-70",
                    "depth_ft": "5-30"
                }
            },
            "Jerkbait": {
                "description": "Very long and thin lure, often with multiple segments for realistic movement",
                "visual_features": ["very long", "thin body", "segmented", "realistic fish shape"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Walleye"],
                "best_seasons": ["Winter", "Spring", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "35-70",
                    "depth_ft": "2-15"
                }
            },
            "Topwater": {
                "description": "Wide, flat lure that floats on surface, creates splashing and popping sounds",
                "visual_features": ["wide body", "flat shape", "surface action", "popping sounds"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass"],
                "best_seasons": ["Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "60-85",
                    "depth_ft": "1-5"
                }
            }
        }
    
    def analyze_with_chatgpt(self, image_path: str) -> Dict:
        """
        Use ChatGPT Vision API to analyze lure image
        """
        if not self.openai_api_key:
            return {"error": "OpenAI API key not provided"}
        
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # ChatGPT Vision API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this fishing lure image and provide:
                                1. Lure type (Spinnerbait, Crankbait, Spoon, Jerkbait, Topwater, or Other)
                                2. Confidence level (0-100%)
                                3. Key visual features you observe
                                4. Why you think it's this type
                                5. Target fish species this lure would attract
                                
                                Respond in JSON format:
                                {
                                    "lure_type": "type",
                                    "confidence": percentage,
                                    "visual_features": ["feature1", "feature2"],
                                    "reasoning": "explanation",
                                    "target_species": ["species1", "species2"]
                                }"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                try:
                    chatgpt_analysis = json.loads(content)
                    return {"success": True, "chatgpt_analysis": chatgpt_analysis}
                except json.JSONDecodeError:
                    return {"success": True, "raw_response": content}
            else:
                return {"error": f"API request failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"ChatGPT analysis failed: {str(e)}"}
    
    def analyze_with_traditional_cv(self, image_path: str) -> Dict:
        """
        Traditional computer vision analysis (current system)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Basic CV analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            height, width = image.shape[:2]
            aspect_ratio = width / height
            
            # Color analysis
            h, s, v = cv2.split(hsv)
            avg_saturation = np.mean(s)
            avg_value = np.mean(v)
            
            # Shape analysis
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                # Edge analysis
                edges = cv2.Canny(gray, 50, 150)
                edge_density = np.sum(edges > 0) / (width * height)
                
                cv_analysis = {
                    "aspect_ratio": round(aspect_ratio, 2),
                    "circularity": round(circularity, 3),
                    "edge_density": round(edge_density, 3),
                    "avg_saturation": round(avg_saturation, 1),
                    "avg_value": round(avg_value, 1)
                }
            else:
                cv_analysis = {"error": "No contours detected"}
            
            return {"success": True, "cv_analysis": cv_analysis}
            
        except Exception as e:
            return {"error": f"CV analysis failed: {str(e)}"}
    
    def hybrid_analysis(self, image_path: str) -> Dict:
        """
        Combine ChatGPT and traditional CV analysis
        """
        print("🔍 Starting hybrid analysis...")
        
        # Get both analyses
        chatgpt_result = self.analyze_with_chatgpt(image_path)
        cv_result = self.analyze_with_traditional_cv(image_path)
        
        # Combine results
        hybrid_result = {
            "image_path": image_path,
            "chatgpt_analysis": chatgpt_result,
            "traditional_cv": cv_result,
            "hybrid_decision": self._combine_analyses(chatgpt_result, cv_result)
        }
        
        return hybrid_result
    
    def _combine_analyses(self, chatgpt_result: Dict, cv_result: Dict) -> Dict:
        """
        Intelligently combine both analysis methods
        """
        if "error" in chatgpt_result or "error" in cv_result:
            return {"error": "One or both analyses failed"}
        
        # Extract ChatGPT prediction
        chatgpt_prediction = chatgpt_result.get("chatgpt_analysis", {})
        lure_type = chatgpt_prediction.get("lure_type", "Unknown")
        confidence = chatgpt_prediction.get("confidence", 0)
        
        # Extract CV features
        cv_features = cv_result.get("cv_analysis", {})
        
        # Cross-validate with CV features
        validation_score = self._validate_with_cv(lure_type, cv_features)
        
        # Adjust confidence based on CV validation
        adjusted_confidence = min(confidence + validation_score, 100)
        
        return {
            "final_lure_type": lure_type,
            "adjusted_confidence": adjusted_confidence,
            "chatgpt_confidence": confidence,
            "cv_validation_score": validation_score,
            "reasoning": f"ChatGPT identified as {lure_type} with {confidence}% confidence. CV validation added {validation_score} points."
        }
    
    def _validate_with_cv(self, lure_type: str, cv_features: Dict) -> float:
        """
        Validate ChatGPT prediction using CV features
        """
        if "error" in cv_features:
            return 0.0
        
        score = 0.0
        aspect_ratio = cv_features.get("aspect_ratio", 1.0)
        circularity = cv_features.get("circularity", 0.0)
        edge_density = cv_features.get("edge_density", 0.0)
        
        # Validate based on lure type characteristics
        if lure_type == "Spinnerbait":
            if 1.5 < aspect_ratio < 4.0:  # Long and thin
                score += 10
            if edge_density > 0.1:  # Lots of edges/details
                score += 5
                
        elif lure_type == "Spoon":
            if circularity > 0.7:  # Very circular
                score += 15
            if 0.8 < aspect_ratio < 1.5:  # Roughly round
                score += 10
                
        elif lure_type == "Jerkbait":
            if aspect_ratio > 3.0:  # Very long and thin
                score += 15
                
        elif lure_type == "Topwater":
            if 1.0 < aspect_ratio < 2.0:  # Wide and flat
                score += 10
                
        elif lure_type == "Crankbait":
            if 0.8 < aspect_ratio < 1.5:  # Roughly square-ish
                score += 10
            if edge_density > 0.15:  # Lots of edges
                score += 5
        
        return score
    
    def generate_training_data(self, image_paths: List[str]) -> Dict:
        """
        Generate training data from ChatGPT analysis for model training
        """
        training_data = []
        
        for image_path in image_paths:
            print(f"📸 Generating training data for: {image_path}")
            
            result = self.analyze_with_chatgpt(image_path)
            if "success" in result and "chatgpt_analysis" in result:
                analysis = result["chatgpt_analysis"]
                
                training_sample = {
                    "image_path": image_path,
                    "label": analysis.get("lure_type", "Unknown"),
                    "confidence": analysis.get("confidence", 0),
                    "features": analysis.get("visual_features", []),
                    "reasoning": analysis.get("reasoning", ""),
                    "target_species": analysis.get("target_species", [])
                }
                
                training_data.append(training_sample)
        
        return {
            "total_samples": len(training_data),
            "samples": training_data,
            "lure_type_distribution": self._get_label_distribution(training_data)
        }
    
    def _get_label_distribution(self, training_data: List[Dict]) -> Dict:
        """Get distribution of lure types in training data"""
        distribution = {}
        for sample in training_data:
            label = sample["label"]
            distribution[label] = distribution.get(label, 0) + 1
        return distribution

def main():
    """Example usage of the Hybrid Lure Classifier"""
    print("🎣 Hybrid Lure Classifier Demo")
    print("=" * 50)
    
    # Initialize classifier (you'll need to add your OpenAI API key)
    classifier = HybridLureClassifier()
    
    print("💡 To use ChatGPT Vision API, set your OpenAI API key:")
    print("   classifier = HybridLureClassifier(openai_api_key='your-key-here')")
    
    print("\n🔍 Available analysis methods:")
    print("   1. classifier.analyze_with_chatgpt(image_path) - ChatGPT Vision")
    print("   2. classifier.analyze_with_traditional_cv(image_path) - Traditional CV")
    print("   3. classifier.hybrid_analysis(image_path) - Combined approach")
    print("   4. classifier.generate_training_data(image_paths) - Generate training data")
    
    print("\n🚀 Benefits of hybrid approach:")
    print("   - ChatGPT: Natural language understanding of lure features")
    print("   - Traditional CV: Precise measurements and validation")
    print("   - Training data generation: Create datasets for custom models")
    print("   - Continuous improvement: Learn from ChatGPT's analysis")

if __name__ == "__main__":
    main()
