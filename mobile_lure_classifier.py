#!/usr/bin/env python3
"""
Mobile-Optimized Lure Classifier: ChatGPT Vision + Comprehensive Fishing Database
Designed for mobile apps with API-first architecture
"""

import json
import os
import requests
from typing import Dict, List
import base64
from PIL import Image
import datetime
import config

class MobileLureClassifier:
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
    
    def analyze_lure(self, image_path: str) -> Dict:
        """
        Analyze lure image using ChatGPT Vision API and return comprehensive results
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
                "model": config.CHATGPT_MODEL,
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
                "max_tokens": config.MAX_TOKENS
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
                    
                    # Get lure type and confidence
                    lure_type = chatgpt_analysis.get("lure_type", "Unknown")
                    confidence = chatgpt_analysis.get("confidence", 0)
                    
                    # Get detailed lure information from database
                    lure_info = self.get_lure_info(lure_type)
                    
                    # Store in history
                    self.analysis_history.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "image_path": image_path,
                        "lure_type": lure_type,
                        "confidence": confidence,
                        "analysis": chatgpt_analysis
                    })
                    
                    # Return comprehensive results
                    return {
                        "success": True,
                        "image_path": image_path,
                        "lure_type": lure_type,
                        "confidence": confidence,
                        "chatgpt_analysis": chatgpt_analysis,
                        "lure_details": lure_info,
                        "analysis_method": "ChatGPT Vision API",
                        "analysis_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                except json.JSONDecodeError:
                    print(f"⚠️ JSON parsing failed, raw response: {content}")
                    return {"error": f"Failed to parse ChatGPT response: {content}"}
            else:
                return {"error": f"API request failed: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
        finally:
            # Clean up compressed image
            if 'compressed_path' in locals():
                self._cleanup_compressed_image(compressed_path)
    
    def get_lure_info(self, lure_type: str) -> Dict:
        """Get comprehensive lure information from database"""
        return self.lure_database.get(lure_type, {})
    
    def get_analysis_history(self) -> List[Dict]:
        """Get analysis history for monitoring and improvement"""
        return self.analysis_history
    
    def save_analysis_to_json(self, analysis_results: Dict, output_path: str = None) -> str:
        """
        Save analysis results to a JSON file in an organized directory structure
        """
        # Create organized directory structure
        results_dir = config.RESULTS_FOLDER
        os.makedirs(results_dir, exist_ok=True)
        
        # Create subdirectories by date
        today = datetime.datetime.now()
        date_dir = today.strftime("%Y-%m-%d")
        full_results_dir = os.path.join(results_dir, date_dir)
        os.makedirs(full_results_dir, exist_ok=True)
        
        # Generate filename with timestamp
        if output_path is None:
            # Extract image name from results if available
            image_path = analysis_results.get("image_path", "analysis")
            if isinstance(image_path, str):
                base_name = os.path.basename(image_path)
                base_name = os.path.splitext(base_name)[0]
            else:
                base_name = "analysis"
            
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

    def _compress_image_for_api(self, image_path: str, max_size_kb: int = None) -> str:
        """
        Compress image for API while preserving important lure details
        """
        if max_size_kb is None:
            max_size_kb = config.TARGET_COMPRESSION_KB
            
        try:
            # Ensure uploads directory exists
            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
            
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
                max_dimension = config.MAX_IMAGE_DIMENSION
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
                compressed_path = f"{config.UPLOAD_FOLDER}/compressed_{base_name}.jpg"
                
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
    """Example usage of the Mobile Lure Classifier"""
    print("🎣 Mobile Lure Classifier Demo")
    print("=" * 50)
    
    # Initialize classifier (you'll need to add your OpenAI API key)
    classifier = MobileLureClassifier()
    
    print("💡 To use ChatGPT Vision API, set your OpenAI API key in config.py:")
    print("   OPENAI_API_KEY = 'your-actual-api-key-here'")
    
    print("\n🔍 Available analysis methods:")
    print("   1. classifier.analyze_lure(image_path) - ChatGPT Vision analysis")
    print("   2. classifier.get_lure_info(lure_type) - Get lure information")
    print("   3. classifier.estimate_api_cost(image_path) - Cost estimation")
    
    print("\n🚀 Benefits of mobile-optimized approach:")
    print("   - Lightweight: No heavy CV models")
    print("   - Fast: API-first architecture")
    print("   - Accurate: ChatGPT Vision analysis")
    print("   - Comprehensive: Rich lure database")
    print("   - Mobile-friendly: Optimized for phones")

if __name__ == "__main__":
    main()
