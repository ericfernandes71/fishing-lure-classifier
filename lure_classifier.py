import cv2
import numpy as np
from PIL import Image
import json
import os
import datetime
from typing import Dict, List, Tuple
import random

class FishingLureClassifier:
    def __init__(self):
        self.lure_database = self._initialize_lure_database()
        
    def _initialize_lure_database(self) -> Dict:
        """Initialize comprehensive database of fishing lure characteristics"""
        return {
            "Spinnerbait": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Northern Pike", "Musky"],
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
            "Squarebill Crankbait": {
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
            "Lipless Crankbait": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Striped Bass"],
                "best_seasons": ["Spring", "Fall", "Winter"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "40-80",
                    "depth_ft": "1-20",
                    "structure_cover": ["weeds", "open water", "shoreline", "drop-offs"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Yo-yo retrieve", "Burning retrieve"],
                "recommended_colors": {
                    "clear_water": ["Natural shad", "Bluegill", "Silver", "White"],
                    "stained_water": ["Chartreuse", "Orange", "Red", "Black"],
                    "muddy_water": ["Chartreuse", "Orange", "Red", "Black", "White"]
                },
                "common_mistakes": ["Not varying retrieve", "Wrong color for conditions", "Not fishing the right depth"],
                "notes": "Versatile lure that works year-round. Excellent for covering water and finding active fish."
            },
            "Spoon": {
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
            "Inline Spinner": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Northern Pike", "Musky"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "1-10",
                    "structure_cover": ["weeds", "shoreline", "open water", "rocks"]
                },
                "retrieve_styles": ["Steady retrieve", "Slow roll", "Stop and go"],
                "recommended_colors": ["Silver", "Gold", "White", "Chartreuse", "Orange"],
                "common_mistakes": ["Retrieving too fast", "Wrong blade size", "Not varying retrieve"],
                "notes": "Great for covering water and catching aggressive fish. Versatile in various conditions."
            },
            "Jerkbait": {
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
            "Topwater Popper": {
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
            "Buzzbait": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["stained", "muddy"],
                    "water_temperature_f": "55-85",
                    "depth_ft": "1-8",
                    "structure_cover": ["weeds", "shoreline", "wood", "rocks"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Burning retrieve"],
                "recommended_colors": ["White", "Black", "Chartreuse", "Orange"],
                "common_mistakes": ["Retrieving too slow", "Wrong color for conditions", "Not fishing around cover"],
                "notes": "Excellent for aggressive fish and low visibility conditions. Creates vibration and noise."
            },
            "Swim Jig": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "50-80",
                    "depth_ft": "2-15",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Bouncing off structure"],
                "recommended_colors": ["Natural shad", "Bluegill", "Crawfish", "Chartreuse", "Black"],
                "common_mistakes": ["Wrong trailer", "Not fishing around cover", "Wrong retrieve speed"],
                "notes": "Versatile jig that can be fished at various depths and speeds."
            },
            "Finesse Jig": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Winter", "Spring", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained"],
                    "water_temperature_f": "35-75",
                    "depth_ft": "5-25",
                    "structure_cover": ["rocks", "drop-offs", "deep structure"]
                },
                "retrieve_styles": ["Dragging", "Hopping", "Swimming"],
                "recommended_colors": ["Natural brown", "Green pumpkin", "Black", "Blue"],
                "common_mistakes": ["Too much action", "Wrong size", "Not being patient"],
                "notes": "Excellent for pressured fish and cold water. Subtle presentation is key."
            },
            "Senko Worm": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Spring", "Summer", "Fall", "Winter"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "35-85",
                    "depth_ft": "1-20",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline", "open water"]
                },
                "retrieve_styles": ["Wacky rig", "Texas rig", "Carolina rig", "Drop shot"],
                "recommended_colors": ["Green pumpkin", "Watermelon", "Black", "Natural brown", "Chartreuse"],
                "common_mistakes": ["Too much action", "Wrong rigging", "Not being patient"],
                "notes": "One of the most versatile baits ever created. Works in all conditions and seasons."
            },
            "Paddle Tail Swimbait": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass", "Striped Bass"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["clear", "stained", "muddy"],
                    "water_temperature_f": "45-80",
                    "depth_ft": "2-20",
                    "structure_cover": ["weeds", "rocks", "wood", "open water", "shoreline"]
                },
                "retrieve_styles": ["Steady retrieve", "Stop and go", "Yo-yo retrieve", "Burning retrieve"],
                "recommended_colors": {
                    "clear_water": ["Natural shad", "Bluegill", "Silver", "White"],
                    "stained_water": ["Chartreuse", "Orange", "Red", "Black"],
                    "muddy_water": ["Chartreuse", "Orange", "Red", "Black", "White"]
                },
                "common_mistakes": ["Wrong size", "Not matching the hatch", "Wrong retrieve speed"],
                "notes": "Excellent for covering water and catching active fish. Versatile presentation options."
            },
            "Creature Bait": {
                "target_species": ["Largemouth Bass", "Smallmouth Bass", "Spotted Bass"],
                "best_seasons": ["Spring", "Summer", "Fall"],
                "best_conditions": {
                    "water_clarity": ["stained", "muddy"],
                    "water_temperature_f": "50-80",
                    "depth_ft": "2-15",
                    "structure_cover": ["weeds", "rocks", "wood", "shoreline"]
                },
                "retrieve_styles": ["Texas rig", "Carolina rig", "Drop shot", "Jig trailer"],
                "recommended_colors": ["Green pumpkin", "Watermelon", "Black", "Natural brown", "Chartreuse"],
                "common_mistakes": ["Too much action", "Wrong size", "Not fishing around cover"],
                "notes": "Excellent for aggressive fish and heavy cover. Creates lots of movement and vibration."
            }
        }
    
    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze a fishing lure image and return classification results
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing lure analysis results
        """
        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Get image dimensions and basic features
            height, width = image.shape[:2]
            
            # Analyze the image using computer vision
            lure_type, confidence, feature_analysis = self._classify_lure_with_features(image)
            
            # Get lure information from database
            lure_info = self.lure_database.get(lure_type, {})
            
            # Generate analysis results
            results = {
                "image_name": os.path.basename(image_path),
                "image_dimensions": f"{width}x{height}",
                "predicted_lure_type": lure_type,
                "confidence": confidence,
                "feature_analysis": feature_analysis,  # NEW: Shows why it made the decision
                "target_species": lure_info.get("target_species", []),
                "best_seasons": lure_info.get("best_seasons", []),
                "best_conditions": lure_info.get("best_conditions", {}),
                "retrieve_styles": lure_info.get("retrieve_styles", []),
                "recommended_colors": lure_info.get("recommended_colors", {}),
                "common_mistakes": lure_info.get("common_mistakes", []),
                "notes": lure_info.get("notes", "")
            }
            
            return results
            
        except Exception as e:
            return {
                "error": f"Failed to analyze image: {str(e)}",
                "image_name": os.path.basename(image_path) if image_path else "unknown"
            }
    
    def _classify_lure_simple(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Real classification method based on actual image analysis
        Uses computer vision techniques to identify lure characteristics
        """
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Get image dimensions and aspect ratio
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        # Analyze color distribution
        h, s, v = cv2.split(hsv)
        avg_saturation = np.mean(s)
        avg_value = np.mean(v)
        avg_hue = np.mean(h)
        
        # Analyze shape characteristics
        # Find contours to detect lure shape
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze the largest contour (main lure body)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Calculate shape features
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
            else:
                circularity = 0
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            rect_aspect = w / h if h > 0 else 0
            
            # Analyze edges for lure features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Analyze color patterns
            # Check for metallic/shimmering effects
            metallic_score = self._detect_metallic_effect(image, hsv)
            
            # Check for specific color patterns
            color_pattern = self._analyze_color_pattern(image, hsv)
            
            # Use these features to classify the lure
            lure_type, confidence, feature_scores = self._classify_by_features(
                aspect_ratio, circularity, rect_aspect, edge_density, 
                metallic_score, color_pattern, avg_saturation, avg_value
            )
            
            return lure_type, confidence
        else:
            # Fallback if no contours found
            return "Unknown", 0.1
    
    def _classify_lure_with_features(self, image: np.ndarray) -> Tuple[str, float, Dict]:
        """
        Real classification method based on actual image analysis
        Uses computer vision techniques to identify lure characteristics
        Returns: (lure_type, confidence, feature_analysis)
        """
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Get image dimensions and aspect ratio
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        # Analyze color distribution
        h, s, v = cv2.split(hsv)
        avg_saturation = np.mean(s)
        avg_value = np.mean(v)
        avg_hue = np.mean(h)
        
        # Analyze shape characteristics
        # Find contours to detect lure shape
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze the largest contour (main lure body)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # Calculate shape features
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
            else:
                circularity = 0
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)
            rect_aspect = w / h if h > 0 else 0
            
            # Analyze edges for lure features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Analyze color patterns
            # Check for metallic/shimmering effects
            metallic_score = self._detect_metallic_effect(image, hsv)
            
            # Check for specific color patterns
            color_pattern = self._analyze_color_pattern(image, hsv)
            
            # Use these features to classify the lure
            lure_type, confidence, feature_scores = self._classify_by_features(
                aspect_ratio, circularity, rect_aspect, edge_density, 
                metallic_score, color_pattern, avg_saturation, avg_value
            )
            
            print(f"DEBUG: Extracted features:")
            print(f"  Aspect ratio: {aspect_ratio:.3f}")
            print(f"  Circularity: {circularity:.3f}")
            print(f"  Rectangular aspect: {rect_aspect:.3f}")
            print(f"  Edge density: {edge_density:.3f}")
            print(f"  Metallic score: {metallic_score:.3f}")
            print(f"  Color pattern: {color_pattern}")
            print(f"  Avg saturation: {avg_saturation:.1f}")
            print(f"  Avg value: {avg_value:.1f}")
            
            # Create detailed feature analysis
            feature_analysis = {
                "shape_features": {
                    "aspect_ratio": round(aspect_ratio, 2),
                    "circularity": round(circularity, 3),
                    "rectangular_aspect": round(rect_aspect, 2),
                    "edge_density": round(edge_density, 3)
                },
                "color_features": {
                    "average_saturation": round(avg_saturation, 1),
                    "average_value": round(avg_value, 1),
                    "average_hue": round(avg_hue, 1),
                    "metallic_score": round(metallic_score, 3),
                    "color_pattern": color_pattern
                },
                "classification_scores": feature_scores,
                "analysis_notes": self._get_analysis_notes(
                    aspect_ratio, circularity, metallic_score, color_pattern
                )
            }
            
            return lure_type, confidence, feature_analysis
        else:
            # Fallback if no contours found
            feature_analysis = {
                "error": "No contours detected in image",
                "shape_features": {},
                "color_features": {},
                "classification_scores": {},
                "analysis_notes": "Could not analyze image structure"
            }
            return "Unknown", 0.1, feature_analysis
    
    def _detect_metallic_effect(self, image: np.ndarray, hsv: np.ndarray) -> float:
        """Detect metallic/shimmering effects in the image"""
        # Metallic objects often have high variance in saturation and value
        h, s, v = cv2.split(hsv)
        s_std = np.std(s)
        v_std = np.std(v)
        
        # Normalize and combine
        metallic_score = (s_std + v_std) / 255.0
        return min(metallic_score, 1.0)
    
    def _analyze_color_pattern(self, image: np.ndarray, hsv: np.ndarray) -> str:
        """Analyze the color pattern of the lure"""
        h, s, v = cv2.split(hsv)
        
        # Count dominant colors
        h_hist = cv2.calcHist([h], [0], None, [180], [0, 180])
        s_hist = cv2.calcHist([s], [0], None, [256], [0, 256])
        
        # Find dominant hue
        dominant_hue = np.argmax(h_hist)
        
        # Classify color pattern
        if dominant_hue < 30 or dominant_hue > 150:  # Red/Blue range
            return "red_blue"
        elif 30 <= dominant_hue < 90:  # Yellow/Green range
            return "yellow_green"
        elif 90 <= dominant_hue < 150:  # Cyan/Blue range
            return "cyan_blue"
        else:
            return "mixed"
    
    def _classify_by_features(self, aspect_ratio: float, circularity: float, 
                            rect_aspect: float, edge_density: float, 
                            metallic_score: float, color_pattern: str,
                            avg_saturation: float, avg_value: float) -> Tuple[str, float, Dict]:
        """
        Improved classification method with better differentiation between lure types
        """
        # Define feature thresholds for different lure types with more specific criteria
        lure_scores = {}
        
        # Spinnerbait - typically long and thin with metallic parts, high edge density
        spinnerbait_score = 0
        if 1.8 < aspect_ratio < 3.5:  # More specific long and thin range
            spinnerbait_score += 3
        elif 1.5 < aspect_ratio < 1.8:  # Slightly shorter range
            spinnerbait_score += 1
        if metallic_score > 0.4:  # Higher metallic threshold
            spinnerbait_score += 2
        if edge_density > 0.08:  # High edge density for spinnerbait
            spinnerbait_score += 2
        if circularity < 0.6:  # Spinnerbaits are typically not very circular
            spinnerbait_score += 1
        lure_scores["Spinnerbait"] = spinnerbait_score
        
        # Crankbait - typically rectangular with diving lip, medium edges
        crankbait_score = 0
        if 0.7 < rect_aspect < 1.3:  # More specific square-ish range
            crankbait_score += 3
        if edge_density > 0.12 and edge_density < 0.25:  # Medium edge density
            crankbait_score += 2
        if metallic_score > 0.2 and metallic_score < 0.6:  # Medium metallic
            crankbait_score += 1
        if circularity < 0.5:  # Crankbaits are not circular
            crankbait_score += 1
        lure_scores["Squarebill Crankbait"] = crankbait_score
        
        # Spoon - typically oval/circular and metallic, low edge density
        spoon_score = 0
        if circularity > 0.75:  # Very circular
            spoon_score += 4
        elif circularity > 0.65:  # Moderately circular
            spoon_score += 2
        if metallic_score > 0.5:  # Very metallic
            spoon_score += 3
        elif metallic_score > 0.3:  # Moderately metallic
            spoon_score += 1
        if 0.6 < aspect_ratio < 1.8:  # Roughly round to oval
            spoon_score += 2
        if edge_density < 0.06:  # Low edge density for smooth spoons
            spoon_score += 1
        lure_scores["Spoon"] = spoon_score
        
        # Jerkbait - typically long and thin, low circularity
        jerkbait_score = 0
        if 2.5 < aspect_ratio < 4.5:  # Very long and thin
            jerkbait_score += 4
        elif 2.0 < aspect_ratio < 2.5:  # Moderately long
            jerkbait_score += 2
        if circularity < 0.4:  # Jerkbaits are not circular
            jerkbait_score += 2
        if edge_density > 0.05 and edge_density < 0.15:  # Medium edge density
            jerkbait_score += 1
        lure_scores["Jerkbait"] = jerkbait_score
        
        # Topwater - typically flat and wide, medium circularity
        topwater_score = 0
        if 1.2 < aspect_ratio < 2.2:  # Wide and flat
            topwater_score += 3
        if avg_value > 120:  # Bright colors
            topwater_score += 2
        if 0.4 < circularity < 0.7:  # Medium circularity
            topwater_score += 1
        if edge_density > 0.08 and edge_density < 0.2:  # Medium edge density
            topwater_score += 1
        lure_scores["Topwater Popper"] = topwater_score
        
        # Jig - typically compact and round, low aspect ratio
        jig_score = 0
        if 0.6 < aspect_ratio < 1.2:  # Roughly round
            jig_score += 3
        if circularity > 0.6:  # Somewhat circular
            jig_score += 2
        if edge_density < 0.08:  # Low edge density
            jig_score += 1
        if metallic_score < 0.4:  # Not very metallic
            jig_score += 1
        lure_scores["Finesse Jig"] = jig_score
        
        # Worm - typically long and thin, very low circularity
        worm_score = 0
        if aspect_ratio > 3.5:  # Very long
            worm_score += 4
        elif aspect_ratio > 2.8:  # Moderately long
            worm_score += 2
        if circularity < 0.3:  # Very low circularity
            worm_score += 2
        if avg_saturation < 60:  # Natural colors
            worm_score += 1
        if edge_density < 0.05:  # Very low edge density
            worm_score += 1
        lure_scores["Senko Worm"] = worm_score
        
        # Inline Spinner - similar to spinnerbait but more circular
        inline_spinner_score = 0
        if 1.4 < aspect_ratio < 2.2:  # Medium length
            inline_spinner_score += 2
        if circularity > 0.6:  # More circular than spinnerbait
            inline_spinner_score += 2
        if metallic_score > 0.4:  # Metallic
            inline_spinner_score += 2
        if edge_density > 0.06:  # Some edges
            inline_spinner_score += 1
        lure_scores["Inline Spinner"] = inline_spinner_score
        
        # Lipless Crankbait - rectangular but longer than squarebill
        lipless_score = 0
        if 1.3 < rect_aspect < 2.0:  # Longer than square
            lipless_score += 3
        if edge_density > 0.1:  # Good edge density
            lipless_score += 2
        if metallic_score > 0.3:  # Somewhat metallic
            lipless_score += 1
        if circularity < 0.5:  # Not circular
            lipless_score += 1
        lure_scores["Lipless Crankbait"] = lipless_score
        
        # Find the best match with tie-breaking
        best_lure = max(lure_scores, key=lure_scores.get)
        best_score = lure_scores[best_lure]
        
        # Check for ties and use additional criteria to break them
        tied_lures = [lure for lure, score in lure_scores.items() if score == best_score]
        if len(tied_lures) > 1:
            print(f"DEBUG: Tie detected between {tied_lures} with score {best_score}")
            # Use aspect ratio and circularity to break ties
            for lure in tied_lures:
                if lure == "Spoon" and circularity > 0.7:
                    best_lure = lure
                    break
                elif lure == "Spinnerbait" and aspect_ratio > 2.0:
                    best_lure = lure
                    break
                elif lure == "Jerkbait" and aspect_ratio > 3.0:
                    best_lure = lure
                    break
        
        # Calculate confidence based on how well it matches
        # Use a fixed maximum score for consistent confidence calculation
        max_possible_score = 8  # Maximum score any lure could get
        confidence = min(best_score / max_possible_score, 0.95)
        
        # If no good match found, use a fallback
        if best_score < 2:
            best_lure = "Unknown"
            confidence = 0.1
        
        print(f"DEBUG: Classification result - {best_lure} with score {best_score} and confidence {confidence}")
        print(f"DEBUG: All scores: {lure_scores}")
        
        # Show detailed scoring for top 3 lures
        sorted_scores = sorted(lure_scores.items(), key=lambda x: x[1], reverse=True)
        print(f"DEBUG: Top 3 classifications:")
        for i, (lure, score) in enumerate(sorted_scores[:3]):
            print(f"  {i+1}. {lure}: {score} points")
        
        # Create detailed feature analysis for the best match
        best_lure_info = self.lure_database.get(best_lure, {})
        feature_analysis = {
            "shape_features": {
                "aspect_ratio": round(aspect_ratio, 2),
                "circularity": round(circularity, 3),
                "rectangular_aspect": round(rect_aspect, 2),
                "edge_density": round(edge_density, 3)
            },
            "color_features": {
                "average_saturation": round(avg_saturation, 1),
                "average_value": round(avg_value, 1),
                "metallic_score": round(metallic_score, 3),
                "color_pattern": color_pattern
            },
            "classification_scores": lure_scores,
            "analysis_notes": self._get_analysis_notes(
                aspect_ratio, circularity, metallic_score, color_pattern
            )
        }
        
        return best_lure, confidence, feature_analysis
    
    def _get_analysis_notes(self, aspect_ratio: float, circularity: float, 
                            metallic_score: float, color_pattern: str) -> str:
        """
        Generates a human-readable analysis note based on features.
        """
        notes = []
        
        if aspect_ratio > 3.0:
            notes.append("Lure is very long and thin.")
        elif aspect_ratio < 0.5:
            notes.append("Lure is very wide and flat.")
        else:
            notes.append(f"Lure has a moderate aspect ratio of {aspect_ratio:.2f}.")

        if circularity > 0.7:
            notes.append("Lure is very circular.")
        elif circularity < 0.3:
            notes.append("Lure is very elongated.")
        else:
            notes.append(f"Lure has a moderate circularity of {circularity:.3f}.")

        if metallic_score > 0.5:
            notes.append("Lure has strong metallic/shimmering effects.")
        elif metallic_score < 0.2:
            notes.append("Lure has minimal metallic/shimmering effects.")
        else:
            notes.append(f"Lure has a moderate metallic score of {metallic_score:.3f}.")

        if color_pattern == "red_blue":
            notes.append("Lure has a dominant red or blue hue.")
        elif color_pattern == "yellow_green":
            notes.append("Lure has a dominant yellow or green hue.")
        elif color_pattern == "cyan_blue":
            notes.append("Lure has a dominant cyan or blue hue.")
        else:
            notes.append(f"Lure has a mixed color pattern.")

        return "; ".join(notes)
    
    def save_analysis_to_json(self, analysis_results: Dict, output_path: str = None) -> str:
        """
        Save analysis results to a JSON file in an organized directory structure
        
        Args:
            analysis_results: Results from analyze_image
            output_path: Optional output file path
            
        Returns:
            Path to saved JSON file
        """
        # Create organized directory structure
        
        # Create main results directory
        results_dir = "analysis_results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Create subdirectories by date
        today = datetime.datetime.now()
        date_dir = today.strftime("%Y-%m-%d")
        full_results_dir = os.path.join(results_dir, date_dir)
        os.makedirs(full_results_dir, exist_ok=True)
        
        # Generate filename with timestamp
        if output_path is None:
            base_name = analysis_results.get("image_name", "analysis")
            # Remove file extension if present
            base_name = os.path.splitext(base_name)[0]
            timestamp = today.strftime("%H-%M-%S")
            output_path = f"{base_name}_{timestamp}_analysis.json"
        
        # Ensure the filename has .json extension
        if not output_path.endswith('.json'):
            output_path += '.json'
        
        # Full path including organized directory
        full_output_path = os.path.join(full_results_dir, output_path)
        
        # Save the file
        with open(full_output_path, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        return full_output_path
    
    def get_lure_recommendations(self, conditions: Dict) -> List[Dict]:
        """
        Get lure recommendations based on fishing conditions
        
        Args:
            conditions: Dictionary with fishing conditions
            
        Returns:
            List of recommended lures with scores
        """
        recommendations = []
        
        for lure_type, lure_info in self.lure_database.items():
            score = 0
            
            # Score based on water clarity
            if "water_clarity" in conditions:
                water_clarity = conditions["water_clarity"]
                if water_clarity in lure_info["best_conditions"]["water_clarity"]:
                    score += 2
            
            # Score based on season
            if "season" in conditions:
                season = conditions["season"]
                if season in lure_info["best_seasons"]:
                    score += 2
            
            # Score based on target species
            if "target_species" in conditions:
                target = conditions["target_species"]
                if target in lure_info["target_species"]:
                    score += 3
            
            if score > 0:
                recommendations.append({
                    "lure_type": lure_type,
                    "score": score,
                    "info": lure_info
                })
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations

    def list_analysis_results(self, date_filter: str = None) -> List[Dict]:
        """
        List all saved analysis results with optional date filtering
        
        Args:
            date_filter: Optional date string in YYYY-MM-DD format
            
        Returns:
            List of analysis result files with metadata
        """
        results_dir = "analysis_results"
        if not os.path.exists(results_dir):
            return []
        
        all_results = []
        
        # Get all date directories
        date_dirs = [d for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d))]
        date_dirs.sort(reverse=True)  # Most recent first
        
        for date_dir in date_dirs:
            # Skip if date filter is specified and doesn't match
            if date_filter and date_dir != date_filter:
                continue
                
            full_date_dir = os.path.join(results_dir, date_dir)
            json_files = [f for f in os.listdir(full_date_dir) if f.endswith('.json')]
            
            for json_file in json_files:
                file_path = os.path.join(full_date_dir, json_file)
                file_stats = os.stat(file_path)
                
                all_results.append({
                    "filename": json_file,
                    "date": date_dir,
                    "full_path": file_path,
                    "size_bytes": file_stats.st_size,
                    "created": datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    "modified": datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return all_results
    
    def get_analysis_result(self, filename: str, date: str = None) -> Dict:
        """
        Retrieve a specific analysis result by filename and optional date
        
        Args:
            filename: Name of the JSON file
            date: Optional date string in YYYY-MM-DD format
            
        Returns:
            Analysis results dictionary or None if not found
        """
        if date:
            file_path = os.path.join("analysis_results", date, filename)
        else:
            # Search all date directories
            for date_dir in os.listdir("analysis_results"):
                potential_path = os.path.join("analysis_results", date_dir, filename)
                if os.path.exists(potential_path):
                    file_path = potential_path
                    break
            else:
                return None
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                return {"error": f"Failed to load file: {str(e)}"}
        
        return None
    
    def cleanup_old_results(self, days_to_keep: int = 30) -> int:
        """
        Clean up old analysis results older than specified days
        
        Args:
            days_to_keep: Number of days to keep results
            
        Returns:
            Number of files deleted
        """
        
        results_dir = "analysis_results"
        if not os.path.exists(results_dir):
            return 0
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_to_keep)
        deleted_count = 0
        
        for date_dir in os.listdir(results_dir):
            try:
                dir_date = datetime.datetime.strptime(date_dir, "%Y-%m-%d")
                if dir_date < cutoff_date:
                    full_dir_path = os.path.join(results_dir, date_dir)
                    # Delete all files in the directory
                    for file in os.listdir(full_dir_path):
                        os.remove(os.path.join(full_dir_path, file))
                    # Remove the empty directory
                    os.rmdir(full_dir_path)
                    deleted_count += 1
            except ValueError:
                # Skip directories that don't match date format
                continue
        
        return deleted_count

def main():
    """Example usage of the FishingLureClassifier"""
    classifier = FishingLureClassifier()
    
    # Example: Get recommendations for spring bass fishing
    conditions = {
        "season": "Spring",
        "water_clarity": "clear",
        "target_species": "Largemouth Bass"
    }
    
    recommendations = classifier.get_lure_recommendations(conditions)
    print("Top lure recommendations for Spring bass fishing:")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. {rec['lure_type']} (Score: {rec['score']})")
    
    print("\nClassifier ready for image analysis!")
    print("Use classifier.analyze_image('path/to/image.jpg') to analyze a lure image.")

if __name__ == "__main__":
    main()

