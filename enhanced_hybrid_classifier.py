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
            },
            "Soft Plastic Worm": {
                "description": "Long, flexible plastic worms that mimic natural bait, excellent for finesse fishing",
                "visual_features": ["long body", "flexible material", "realistic texture", "natural colors"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Trout"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "1-25",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline", "drop-offs"]
                },
                "retrieve_styles": ["Texas rig", "Carolina rig", "Wacky rig", "Drop shot", "Neko rig"],
                "recommended_colors": {
                    "clear_water": ["Natural brown", "Green pumpkin", "Watermelon", "Black"],
                    "stained_water": ["Junebug", "Purple", "Black", "Chartreuse"],
                    "muddy_water": ["Black", "Chartreuse", "White", "Bright colors"]
                },
                "common_mistakes": ["Retrieving too fast", "Not being patient", "Wrong hook size", "Poor presentation"],
                "notes": "The most versatile bass lure. Perfect for pressured waters and finicky fish. Match colors to water clarity and use natural movements."
            },
            "Creature Bait": {
                "description": "Soft plastic baits with appendages, claws, or tentacles that mimic crustaceans and other creatures",
                "visual_features": ["appendages", "claws", "tentacles", "textured surface", "realistic details"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Catfish"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "50-85",
                    "depth_ft": "1-15",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline"]
                },
                "retrieve_styles": ["Slow drag", "Hop and pause", "Dead stick", "Swim retrieve"],
                "recommended_colors": {
                    "clear_water": ["Natural brown", "Green pumpkin", "Watermelon", "Black"],
                    "stained_water": ["Junebug", "Purple", "Black", "Chartreuse"],
                    "muddy_water": ["Black", "Chartreuse", "White", "Bright colors"]
                },
                "common_mistakes": ["Too much action", "Wrong size for conditions", "Not matching the hatch", "Poor hook placement"],
                "notes": "Excellent for aggressive fish and when you need a different presentation. The appendages create natural movement and attract attention."
            },
            "Swimbait": {
                "description": "Soft plastic baits designed to mimic baitfish swimming, often with paddle tails or segmented bodies",
                "visual_features": ["fish-like shape", "paddle tail", "segmented body", "realistic fins", "natural colors"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Pike", "Musky"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "2-20",
                    "structure_cover": ["open water", "drop-offs", "weeds", "shoreline"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Jigging", "Slow roll"],
                "recommended_colors": {
                    "clear_water": ["Natural shad", "Bluegill", "Perch", "Silver"],
                    "stained_water": ["Chartreuse", "White", "Black", "Bright colors"],
                    "muddy_water": ["Chartreuse", "White", "Black", "Bright colors"]
                },
                "common_mistakes": ["Retrieving too fast", "Wrong size for target species", "Not matching the hatch", "Poor hook placement"],
                "notes": "Perfect for covering water and targeting suspended fish. Match the size and color to local baitfish for best results."
            },
            "Crawfish Imitation": {
                "description": "Soft plastic baits specifically designed to mimic crawfish, with claws, segmented body, and realistic details",
                "visual_features": ["claws", "segmented body", "realistic details", "natural colors", "textured surface"],
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Trout", "Pike"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "1-15",
                    "structure_cover": ["rocks", "weeds", "wood", "shoreline", "drop-offs"]
                },
                "retrieve_styles": ["Hop and pause", "Slow drag", "Dead stick", "Swim retrieve"],
                "recommended_colors": {
                    "clear_water": ["Natural brown", "Green pumpkin", "Watermelon", "Black"],
                    "stained_water": ["Junebug", "Purple", "Black", "Chartreuse"],
                    "muddy_water": ["Black", "Chartreuse", "White", "Bright colors"]
                },
                "common_mistakes": ["Too much action", "Wrong size for conditions", "Not matching the hatch", "Poor presentation"],
                "notes": "Crawfish are a primary food source for bass. Use natural movements and match the size to local crawfish. Best in rocky areas and around structure."
            }
        }
    
    def analyze_with_chatgpt(self, image_path: str) -> Dict:
        """
        Use ChatGPT Vision API to analyze lure image
        """
        if not self.openai_api_key:
            return {"error": "OpenAI API key not provided"}
        
        try:
            # Compress image for API efficiency
            print("🖼️ Compressing image for API...")
            compressed_path = self._compress_image_for_api(image_path)
            
            # Encode compressed image to base64
            with open(compressed_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            print(f"📊 Compressed image size: {len(encoded_image)} characters (base64)")
            
            # ChatGPT Vision API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this fishing lure image and provide:
                                1. Lure type (Spinnerbait, Crankbait, Spoon, Jerkbait, Topwater, Soft Plastic Worm, Creature Bait, Swimbait, or Crawfish Imitation)
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
            
            print("🚀 Sending request to ChatGPT Vision API...")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            print(f"DEBUG: ChatGPT API response status: {response.status_code}")
            print(f"DEBUG: ChatGPT API response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response (handle markdown code blocks)
                try:
                    # Remove markdown code blocks if present
                    if content.startswith('```json'):
                        content = content.replace('```json', '').replace('```', '').strip()
                    elif content.startswith('```'):
                        content = content.replace('```', '').strip()
                    
                    chatgpt_analysis = json.loads(content)
                    return {"success": True, "chatgpt_analysis": chatgpt_analysis}
                except json.JSONDecodeError:
                    print(f"⚠️ JSON parsing failed, raw response: {content}")
                    return {"success": True, "raw_response": content}
            else:
                return {"error": f"API request failed: {response.status_code} - {response.text}"}
                
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
        
        # Compress image for API efficiency
        compressed_path = self._compress_image_for_api(image_path)
        
        try:
            # Get both analyses using compressed image for ChatGPT
            chatgpt_result = self.analyze_with_chatgpt(compressed_path)
            cv_result = self.analyze_with_traditional_cv(image_path)  # Use original for CV
            
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
            
        finally:
            # Clean up compressed image
            self._cleanup_compressed_image(compressed_path)
    
    def _combine_analyses(self, chatgpt_result: Dict, cv_result: Dict) -> Dict:
        """
        Intelligently combine both analysis methods with fallback
        """
        # If ChatGPT failed, fall back to traditional CV analysis
        if "error" in chatgpt_result:
            print(f"⚠️ ChatGPT analysis failed: {chatgpt_result['error']}")
            print("🔄 Falling back to traditional CV analysis...")
            
            # Use traditional CV to classify the lure
            cv_features = cv_result.get("cv_analysis", {})
            if "error" not in cv_features:
                lure_type, confidence = self._classify_with_cv_only(cv_features)
                lure_info = self.get_lure_info(lure_type)
                return {
                    "final_lure_type": lure_type,
                    "adjusted_confidence": confidence,
                    "chatgpt_confidence": 0,
                    "cv_validation_score": confidence,
                    "reasoning": f"ChatGPT API unavailable. Traditional CV classified as {lure_type} with {confidence}% confidence.",
                    "fallback_used": True,
                    "lure_details": lure_info
                }
            else:
                return {"error": "Both analyses failed"}
        
        # If CV failed, use ChatGPT only
        if "error" in cv_result:
            print(f"⚠️ CV analysis failed: {cv_result['error']}")
            chatgpt_prediction = chatgpt_result.get("chatgpt_analysis", {})
            lure_type = chatgpt_prediction.get("lure_type", "Unknown")
            confidence = chatgpt_prediction.get("confidence", 0)
            lure_info = self.get_lure_info(lure_type)
            return {
                "final_lure_type": lure_type,
                "adjusted_confidence": confidence,
                "chatgpt_confidence": confidence,
                "cv_validation_score": 0,
                "reasoning": f"CV analysis failed. ChatGPT identified as {lure_type} with {confidence}% confidence.",
                "fallback_used": True,
                "lure_details": lure_info
            }
        
        # Both analyses succeeded - combine them
        chatgpt_prediction = chatgpt_result.get("chatgpt_analysis", {})
        lure_type = chatgpt_prediction.get("lure_type", "Unknown")
        confidence = chatgpt_prediction.get("confidence", 0)
        
        # Extract CV features
        cv_features = cv_result.get("cv_analysis", {})
        
        # Cross-validate with CV features
        validation_score = self._validate_with_cv(lure_type, cv_features)
        
        # Adjust confidence based on CV validation
        adjusted_confidence = min(confidence + validation_score, 100)
        
        # Get detailed lure information from database
        lure_info = self.get_lure_info(lure_type)
        
        return {
            "final_lure_type": lure_type,
            "adjusted_confidence": adjusted_confidence,
            "chatgpt_confidence": confidence,
            "cv_validation_score": validation_score,
            "reasoning": f"ChatGPT identified as {lure_type} with {confidence}% confidence. CV validation added {validation_score} points.",
            "fallback_used": False,
            "lure_details": lure_info  # Add comprehensive lure information
        }
    
    def _classify_with_cv_only(self, cv_features: Dict) -> Tuple[str, float]:
        """
        Classify lure using only traditional CV features when ChatGPT is unavailable
        """
        aspect_ratio = cv_features.get("aspect_ratio", 1.0)
        circularity = cv_features.get("circularity", 0.0)
        edge_density = cv_features.get("edge_density", 0.0)
        metallic_score = cv_features.get("metallic_score", 0.0)
        
        # Simple rule-based classification
        if circularity > 0.7 and 0.8 < aspect_ratio < 1.5:
            return "Spoon", 85.0
        elif aspect_ratio > 2.5:
            return "Jerkbait", 80.0
        elif 1.5 < aspect_ratio < 2.5 and edge_density > 0.1:
            return "Spinnerbait", 75.0
        elif 0.8 < aspect_ratio < 1.5 and edge_density > 0.15:
            return "Crankbait", 70.0
        elif 1.0 < aspect_ratio < 2.0:
            return "Topwater", 65.0
        else:
            return "Unknown", 50.0
    
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
        
        elif lure_type == "Soft Plastic Worm":
            if 1.0 < aspect_ratio < 2.5:  # Moderate aspect ratio
                score += 8
            if edge_density > 0.05:  # Some texture/details
                score += 7
            if metallic_score < 0.5:  # Not very metallic (soft plastic)
                score += 5
            if circularity < 0.8:  # Not perfectly round
                score += 5
        
        elif lure_type == "Creature Bait":
            if 1.0 < aspect_ratio < 2.5:  # Moderate aspect ratio
                score += 8
            if edge_density > 0.05:  # Some texture/details
                score += 7
            if metallic_score < 0.5:  # Not very metallic (soft plastic)
                score += 5
            if circularity < 0.8:  # Not perfectly round
                score += 5
        
        elif lure_type == "Swimbait":
            if 1.0 < aspect_ratio < 2.5:  # Moderate aspect ratio
                score += 8
            if edge_density > 0.05:  # Some texture/details
                score += 7
            if metallic_score < 0.5:  # Not very metallic (soft plastic)
                score += 5
            if circularity < 0.8:  # Not perfectly round
                score += 5
        
        elif lure_type == "Crawfish Imitation":
            if 1.0 < aspect_ratio < 2.5:  # Moderate aspect ratio
                score += 8
            if edge_density > 0.05:  # Some texture/details
                score += 7
            if metallic_score < 0.5:  # Not very metallic (soft plastic)
                score += 5
            if circularity < 0.8:  # Not perfectly round
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
    
    def save_analysis_to_json(self, analysis_results: Dict, output_path: str = None) -> str:
        """
        Save analysis results to a JSON file in an organized directory structure
        
        Args:
            analysis_results: Results from hybrid analysis
            output_path: Optional output file path
            
        Returns:
            Path to saved JSON file
        """
        # Create organized directory structure
        results_dir = "analysis_results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Create subdirectories by date
        today = datetime.datetime.now()
        date_dir = today.strftime("%Y-%m-%d")
        full_results_dir = os.path.join(results_dir, date_dir)
        os.makedirs(full_results_dir, exist_ok=True)
        
        # Generate filename with timestamp
        if output_path is None:
            # Extract image name from results if available
            image_path = analysis_results.get("image_path", "hybrid_analysis")
            if isinstance(image_path, str):
                base_name = os.path.basename(image_path)
                base_name = os.path.splitext(base_name)[0]
            else:
                base_name = "hybrid_analysis"
            
            timestamp = today.strftime("%H-%M-%S")
            output_path = f"{base_name}_hybrid_{timestamp}_analysis.json"
        
        # Ensure the filename has .json extension
        if not output_path.endswith('.json'):
            output_path += '.json'
        
        # Full path including organized directory
        full_output_path = os.path.join(full_results_dir, output_path)
        
        # Save the file
        with open(full_output_path, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        return full_output_path

    def _compress_image_for_api(self, image_path: str, max_size_kb: int = 500) -> str:
        """
        Compress image for API while preserving important lure details
        
        Args:
            image_path: Path to original image
            max_size_kb: Target file size in KB (default: 500KB for API efficiency)
            
        Returns:
            Path to compressed image
        """
        try:
            # Ensure uploads directory exists
            os.makedirs("uploads", exist_ok=True)
            
            # Open image with PIL
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get original dimensions
                original_width, original_height = img.size
                print(f"Original image: {original_width}x{original_height}")
                
                # Calculate target dimensions (maintain aspect ratio)
                # ChatGPT works well with images around 800-1200px on longest side
                max_dimension = 1200
                new_width, new_height = original_width, original_height
                
                if original_width > max_dimension or original_height > max_dimension:
                    if original_width > original_height:
                        new_width = max_dimension
                        new_height = int((original_height * max_dimension) / original_width)
                    else:
                        new_height = max_dimension
                        new_width = int((original_width * max_dimension) / original_height)
                    
                    # Resize image
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Resized to: {new_width}x{new_height}")
                
                # Create compressed version path
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                compressed_path = f"uploads/compressed_{base_name}.jpg"
                
                # Save with quality optimization
                quality = 95
                img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
                
                # Check file size and reduce quality if needed
                file_size_kb = os.path.getsize(compressed_path) / 1024
                print(f"Compressed size: {file_size_kb:.1f} KB")
                
                # If still too large, reduce quality further
                if file_size_kb > max_size_kb:
                    quality = 85
                    img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
                    file_size_kb = os.path.getsize(compressed_path) / 1024
                    print(f"Further compressed: {file_size_kb:.1f} KB")
                
                # If still too large, resize more aggressively
                if file_size_kb > max_size_kb:
                    # Reduce to 800px max dimension
                    if new_width > 800 or new_height > 800:
                        if new_width > new_height:
                            new_width = 800
                            new_height = int((new_height * 800) / new_width)
                        else:
                            new_height = 800
                            new_width = int((new_width * 800) / new_height)
                        
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
                        file_size_kb = os.path.getsize(compressed_path) / 1024
                        print(f"Aggressively compressed: {file_size_kb:.1f} KB")
                
                print(f"✅ Image compressed successfully: {compressed_path}")
                return compressed_path
                
        except Exception as e:
            print(f"❌ Image compression failed: {str(e)}")
            return image_path  # Return original if compression fails
    
    def _cleanup_compressed_image(self, compressed_path: str):
        """
        Clean up compressed image after analysis
        """
        try:
            if compressed_path != compressed_path and os.path.exists(compressed_path):
                os.remove(compressed_path)
                print(f"🧹 Cleaned up compressed image: {compressed_path}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup compressed image: {str(e)}")

    def estimate_api_cost(self, image_path: str) -> Dict:
        """
        Estimate API cost and token usage for an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with cost estimates
        """
        try:
            # Compress image to see final size
            compressed_path = self._compress_image_for_api(image_path)
            
            # Get compressed image size
            file_size_kb = os.path.getsize(compressed_path) / 1024
            
            # Estimate tokens (rough calculation)
            # Base64 encoding increases size by ~33%
            # ChatGPT Vision pricing: $0.01 per 1K tokens (input)
            estimated_tokens = int((file_size_kb * 1.33) * 0.75)  # Rough estimate
            estimated_cost = (estimated_tokens / 1000) * 0.01
            
            # Clean up compressed image
            self._cleanup_compressed_image(compressed_path)
            
            return {
                "original_size_kb": os.path.getsize(image_path) / 1024,
                "compressed_size_kb": file_size_kb,
                "compression_ratio": f"{((os.path.getsize(image_path) - os.path.getsize(compressed_path)) / os.path.getsize(image_path) * 100):.1f}%",
                "estimated_tokens": estimated_tokens,
                "estimated_cost_usd": f"${estimated_cost:.4f}",
                "cost_efficiency": "✅ Good" if file_size_kb < 500 else "⚠️ High cost"
            }
            
        except Exception as e:
            return {"error": f"Cost estimation failed: {str(e)}"}

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
