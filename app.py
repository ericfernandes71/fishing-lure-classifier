from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from mobile_lure_classifier import MobileLureClassifier

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the mobile-optimized lure classifier
mobile_classifier = None

# Load API key from environment variable
def load_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        global mobile_classifier
        mobile_classifier = MobileLureClassifier(openai_api_key=api_key)
        print("✅ OpenAI API key loaded successfully")
        return True
    else:
        print("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return False

# Try to load API key on startup
load_api_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file:
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            print(f"📸 File uploaded: {filename}")
            
            # Check if classifier is available
            if not mobile_classifier:
                return jsonify({'error': 'Lure classifier not initialized. Please set up your API key first.'})
            
            # Analyze the lure using ChatGPT Vision
            print("🔍 Starting lure analysis...")
            results = mobile_classifier.analyze_lure(filepath)
            
            if 'error' in results:
                print(f"❌ Analysis failed: {results['error']}")
                return jsonify({'error': results['error']})
            
            # Save results to JSON file
            json_file = mobile_classifier.save_analysis_to_json(results)
            results['json_file'] = json_file
            
            print(f"✅ Analysis completed successfully")
            print(f"📊 Results: {results}")
            
            return jsonify(results)
            
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            return jsonify({'error': f'Analysis failed: {str(e)}'})
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"🧹 Cleaned up uploaded file: {filepath}")
            except Exception as e:
                print(f"⚠️ Failed to cleanup uploaded file: {str(e)}")

@app.route('/estimate-cost', methods=['POST'])
def estimate_cost():
    """Estimate API cost for lure analysis"""
    if not mobile_classifier:
        return jsonify({'error': 'Lure classifier not initialized. Please set up your API key first.'})
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if file:
            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Get cost estimate
                cost_estimate = mobile_classifier.estimate_api_cost(filepath)
                
                # Clean up temporary file
                os.remove(filepath)
                
                return jsonify(cost_estimate)
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise e
                
    except Exception as e:
        return jsonify({'error': f'Cost estimation failed: {str(e)}'})

@app.route('/reload-api-key')
def reload_api_key():
    """Reload API key from environment (useful for testing)"""
    success = load_api_key()
    return jsonify({'success': success, 'message': 'API key reloaded' if success else 'API key not found'})

if __name__ == '__main__':
    print("🎣 Mobile Lure Classifier Flask App Starting...")
    print("=" * 60)
    
    if mobile_classifier:
        print("✅ OpenAI API key loaded - Ready for lure analysis!")
        print("🌐 Server starting on http://localhost:5000")
    else:
        print("⚠️  OpenAI API key not loaded - Analysis will not work")
        print("💡 Set OPENAI_API_KEY environment variable to enable analysis")
    
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

