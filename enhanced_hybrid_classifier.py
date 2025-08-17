#!/usr/bin/env python3
"""
Enhanced Hybrid Lure Classifier: ChatGPT Vision + Traditional Computer Vision
Integrated with the existing lure classification system
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
import datetime

class EnhancedHybridLureClassifier:
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.lure_database = self._initialize_lure_database()
        self.analysis_history = []
        
    def _initialize_lure_database(self) -> Dict:
        """Initialize comprehensive database of fishing lure characteristics"""
        return {
            "Spinnerbait": {
                "description": "Long, thin lure with metallic spinning blades, typically has a jig head and skirt",
                "visual_features": ["spinning blades", "long body", "metallic parts", "jig head", "skirt"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Northern Pike", "Spotted Bass", "Musky"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "2-15",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Slow roll", "Burning retrieve"],
                "recommended_colors": {
                    "clear_water": ["White", "Chartreuse", "Silver", "Blue"],
                    "stained_water": ["Chartreuse", "Orange", "Red", "Black"],
                    "muddy_water": ["Chartreuse", "Orange", "Red", "Black", "White"]
                },
                "common_mistakes": ["Retrieving too fast", "Not varying retrieve speed", "Using wrong blade size for conditions"],
                "notes": "Excellent for covering water quickly. Vary blade sizes based on water clarity and fish activity."
            },
            "Crankbait": {
                "description": "Rectangular body with diving lip, mimics baitfish swimming",
                "visual_features": ["diving lip", "rectangular body", "fish-like shape", "hooks"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Walleye"],
                "best_seasons": ["Spring", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "50-75",
                    "depth_ft": "2-8",
                    "structure_cover": ["rocks", "wood", "shoreline", "weeds"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Bouncing off structure"],
                "recommended_colors": ["Natural shad", "Crawfish", "Bluegill", "Chartreuse"],
                "common_mistakes": ["Not deflecting off structure", "Retrieving too fast", "Wrong depth for conditions"],
                "notes": "Perfect for deflecting off rocks and wood. Match the hatch with natural colors."
            },
            "Spoon": {
                "description": "Oval or teardrop shaped metallic lure that wobbles and flashes",
                "visual_features": ["oval shape", "metallic surface", "teardrop", "wobbling action"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Northern Pike", "Musky", "Walleye"],
                "best_seasons": ["Fall", "Winter", "Spring"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "35-70",
                    "depth_ft": "5-30",
                    "structure_cover": ["open water", "drop-offs", "deep structure"]
                },
                "retrieve_styles": ["Jigging", "Trolling", "Casting and retrieving"],
                "recommended_colors": ["Silver", "Gold", "Copper", "White", "Chartreuse"],
                "common_mistakes": ["Too much action", "Wrong size for target species", "Not matching the hatch"],
                "notes": "Excellent for deep water and cold water fishing. Mimics injured baitfish effectively."
            },
            "Jerkbait": {
                "description": "Very long and thin lure, often with multiple segments for realistic movement",
                "visual_features": ["very long", "thin body", "segmented", "realistic fish shape"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Walleye"],
                "best_seasons": ["Winter", "Spring", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "35-70",
                    "depth_ft": "2-15",
                    "structure_cover": ["open water", "shoreline", "drop-offs"]
                },
                "retrieve_styles": ["Jerk-pause", "Suspending", "Floating", "Sinking"],
                "recommended_colors": ["Natural shad", "Bluegill", "Crawfish", "White", "Chartreuse"],
                "common_mistakes": ["Too much action", "Wrong pause timing", "Not matching water temperature"],
                "notes": "Excellent for cold water and suspended fish. Suspending models are deadly in winter."
            },
            "Topwater": {
                "description": "Wide, flat lure that floats on surface, creates splashing and popping sounds",
                "visual_features": ["wide body", "flat shape", "surface action", "popping sounds"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "60-85",
                    "depth_ft": "1-5",
                    "structure_cover": ["shoreline", "weeds", "wood", "rocks"]
                },
                "retrieve_styles": ["Pop-pause", "Walking the dog", "Steady retrieve"],
                "recommended_colors": ["Natural shad", "Bluegill", "White", "Black", "Chartreuse"],
                "common_mistakes": ["Too much noise", "Wrong timing", "Not being patient"],
                "notes": "Most exciting way to catch bass. Best during low light and calm conditions."
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
        Traditional computer vision analysis (enhanced version)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Enhanced CV analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            height, width = image.shape[:2]
            aspect_ratio = width / height
            
            # Color analysis
            h, s, v = cv2.split(hsv)
            avg_saturation = np.mean(s)
            avg_value = np.mean(v)
            avg_hue = np.mean(h)
            
            # Enhanced shape analysis
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                rect_aspect = w / h if h > 0 else 0
                
                # Edge analysis
                edges = cv2.Canny(gray, 50, 150)
                edge_density = np.sum(edges > 0) / (width * height)
                
                # Metallic effect detection
                metallic_score = self._detect_metallic_effect(image, hsv)
                
                # Color pattern analysis
                color_pattern = self._analyze_color_pattern(image, hsv)
                
                cv_analysis = {
                    "aspect_ratio": round(aspect_ratio, 2),
                    "circularity": round(circularity, 3),
                    "rectangular_aspect": round(rect_aspect, 2),
                    "edge_density": round(edge_density, 3),
                    "avg_saturation": round(avg_saturation, 1),
                    "avg_value": round(avg_value, 1),
                    "avg_hue": round(avg_hue, 1),
                    "metallic_score": round(metallic_score, 3),
                    "color_pattern": color_pattern
                }
            else:
                cv_analysis = {"error": "No contours detected"}
            
            return {"success": True, "cv_analysis": cv_analysis}
            
        except Exception as e:
            return {"error": f"CV analysis failed: {str(e)}"}
    
    def _detect_metallic_effect(self, image: np.ndarray, hsv: np.ndarray) -> float:
        """Detect metallic/shimmering effects in the image"""
        h, s, v = cv2.split(hsv)
        s_std = np.std(s)
        v_std = np.std(v)
        metallic_score = (s_std + v_std) / 255.0
        return min(metallic_score, 1.0)
    
    def _analyze_color_pattern(self, image: np.ndarray, hsv: np.ndarray) -> str:
        """Analyze the color pattern of the lure"""
        h, s, v = cv2.split(hsv)
        h_hist = cv2.calcHist([h], [0], None, [180], [0, 180])
        dominant_hue = np.argmax(h_hist)
        
        if dominant_hue < 30 or dominant_hue > 150:
            return "red_blue"
        elif 30 <= dominant_hue < 90:
            return "yellow_green"
        elif 90 <= dominant_hue < 150:
            return "cyan_blue"
        else:
            return "mixed"
    
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
        
        # Store in history
        self.analysis_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "image_path": image_path,
            "result": hybrid_result
        })
        
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
        metallic_score = cv_features.get("metallic_score", 0.0)
        
        # Enhanced validation based on lure type characteristics
        if lure_type == "Spinnerbait":
            if 1.5 < aspect_ratio < 4.0:  # Long and thin
                score += 10
            if edge_density > 0.1:  # Lots of edges/details
                score += 5
            if metallic_score > 0.3:  # Metallic parts
                score += 5
                
        elif lure_type == "Spoon":
            if circularity > 0.7:  # Very circular
                score += 15
            if 0.8 < aspect_ratio < 1.5:  # Roughly round
                score += 10
            if metallic_score > 0.4:  # Very metallic
                score += 5
                
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
    
    def get_lure_info(self, lure_type: str) -> Dict:
        """Get comprehensive lure information"""
        return self.lure_database.get(lure_type, {})
    
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
    
    def get_analysis_history(self) -> List[Dict]:
        """Get analysis history for monitoring and improvement"""
        return self.analysis_history

def main():
    """Example usage of the Enhanced Hybrid Lure Classifier"""
    print("🎣 Enhanced Hybrid Lure Classifier Demo")
    print("=" * 50)
    
    # Initialize classifier (you'll need to add your OpenAI API key)
    classifier = EnhancedHybridLureClassifier()
    
    print("💡 To use ChatGPT Vision API, set your OpenAI API key:")
    print("   classifier = EnhancedHybridLureClassifier(openai_api_key='your-key-here')")
    
    print("\n🔍 Available analysis methods:")
    print("   1. classifier.analyze_with_chatgpt(image_path) - ChatGPT Vision")
    print("   2. classifier.analyze_with_traditional_cv(image_path) - Traditional CV")
    print("   3. classifier.hybrid_analysis(image_path) - Combined approach")
    print("   4. classifier.generate_training_data(image_paths) - Generate training data")
    print("   5. classifier.get_lure_info(lure_type) - Get lure information")
    
    print("\n🚀 Benefits of enhanced hybrid approach:")
    print("   - ChatGPT: Natural language understanding of lure features")
    print("   - Traditional CV: Precise measurements and validation")
    print("   - Training data generation: Create datasets for custom models")
    print("   - Continuous improvement: Learn from ChatGPT's analysis")
    print("   - Analysis history: Track and improve over time")

if __name__ == "__main__":
    main()
