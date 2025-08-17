from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from lure_classifier import FishingLureClassifier
from enhanced_hybrid_classifier import EnhancedHybridLureClassifier
import json
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize classifiers
traditional_classifier = FishingLureClassifier()
hybrid_classifier = None  # Will be initialized when API key is provided

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get analysis type from request
        analysis_type = request.form.get('analysis_type', 'traditional')
        
        try:
            if analysis_type == 'hybrid' and hybrid_classifier:
                # Use hybrid classifier
                results = hybrid_classifier.hybrid_analysis(filepath)
                analysis_method = "Hybrid (ChatGPT + Computer Vision)"
            else:
                # Use traditional classifier
                results = traditional_classifier.analyze_image(filepath)
                analysis_method = "Traditional Computer Vision"
            
            print(f"DEBUG: Analysis completed. Results type: {type(results)}")
            print(f"DEBUG: Results keys: {results.keys() if isinstance(results, dict) else 'Not a dict'}")
            print(f"DEBUG: Results: {results}")
            
            # Save results
            if analysis_type == 'hybrid' and hybrid_classifier:
                json_path = hybrid_classifier.save_analysis_to_json(results)
            else:
                json_path = traditional_classifier.save_analysis_to_json(results)
            
            # Add analysis method to results
            results['analysis_method'] = analysis_method
            results['json_file'] = json_path
            
            print(f"DEBUG: Final results to return: {results}")
            return jsonify(results)
            
        except Exception as e:
            print(f"DEBUG: Analysis failed with error: {str(e)}")
            return jsonify({'error': f'Analysis failed: {str(e)}'})
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'})

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/lure-info/<lure_type>')
def lure_info(lure_type):
    if hybrid_classifier:
        lure_data = hybrid_classifier.get_lure_info(lure_type)
    else:
        lure_data = traditional_classifier.get_lure_info(lure_type)
    
    return render_template('lure_info.html', lure_type=lure_type, lure_data=lure_data)

@app.route('/results')
def results():
    # Get analysis results from both classifiers
    traditional_results = traditional_classifier.list_analysis_results()
    
    hybrid_results = []
    if hybrid_classifier:
        hybrid_results = hybrid_classifier.get_analysis_history()
    
    return render_template('results.html', 
                         traditional_results=traditional_results,
                         hybrid_results=hybrid_results)

@app.route('/results/<date>/<filename>')
def view_result(date, filename):
    try:
        if 'hybrid' in filename:
            # Handle hybrid results
            if hybrid_classifier:
                # Find the result in history
                for entry in hybrid_classifier.get_analysis_history():
                    if filename in entry.get('image_path', ''):
                        return jsonify(entry['result'])
        else:
            # Handle traditional results
            result = traditional_classifier.get_analysis_result(filename, date)
            if result:
                return jsonify(result)
        
        return jsonify({'error': 'Result not found'})
    except Exception as e:
        return jsonify({'error': f'Error retrieving result: {str(e)}'})

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        days_to_keep = int(request.form.get('days', 30))
        if hybrid_classifier:
            # Clean up hybrid results (they're in memory, so just clear old ones)
            current_time = datetime.datetime.now()
            hybrid_classifier.analysis_history = [
                entry for entry in hybrid_classifier.analysis_history
                if (current_time - datetime.datetime.fromisoformat(entry['timestamp'])).days <= days_to_keep
            ]
        
        # Clean up traditional results
        removed_count = traditional_classifier.cleanup_old_results(days_to_keep)
        
        return jsonify({
            'success': True,
            'message': f'Cleaned up {removed_count} old results',
            'days_kept': days_to_keep
        })
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'})

@app.route('/setup-hybrid', methods=['POST'])
def setup_hybrid():
    """Setup hybrid classifier with OpenAI API key"""
    try:
        api_key = request.form.get('api_key')
        if not api_key:
            return jsonify({'error': 'API key is required'})
        
        global hybrid_classifier
        hybrid_classifier = EnhancedHybridLureClassifier(openai_api_key=api_key)
        
        return jsonify({
            'success': True,
            'message': 'Hybrid classifier initialized successfully!'
        })
    except Exception as e:
        return jsonify({'error': f'Failed to initialize hybrid classifier: {str(e)}'})

@app.route('/generate-training-data', methods=['POST'])
def generate_training_data():
    """Generate training data from ChatGPT analysis"""
    if not hybrid_classifier:
        return jsonify({'error': 'Hybrid classifier not initialized. Please set up your API key first.'})
    
    try:
        # Get list of images from uploads folder
        upload_folder = app.config['UPLOAD_FOLDER']
        image_files = [f for f in os.listdir(upload_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if not image_files:
            return jsonify({'error': 'No images found in uploads folder'})
        
        # Generate training data
        image_paths = [os.path.join(upload_folder, f) for f in image_files]
        training_data = hybrid_classifier.generate_training_data(image_paths)
        
        # Save training data
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        training_file = f"training_data_{timestamp}.json"
        
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'training_data': training_data,
            'training_file': training_file,
            'message': f'Generated training data for {len(image_files)} images'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate training data: {str(e)}'})

@app.route('/api/classifier-status')
def classifier_status():
    """Get status of available classifiers"""
    return jsonify({
        'traditional': True,
        'hybrid': hybrid_classifier is not None,
        'hybrid_ready': hybrid_classifier is not None
    })

if __name__ == '__main__':
    print("🎣 Starting Fishing Lure Classifier App...")
    print("=" * 50)
    print("Available classifiers:")
    print("✅ Traditional Computer Vision")
    print("⏳ Hybrid (ChatGPT + CV) - Set up API key to enable")
    print("\nTo enable hybrid classifier:")
    print("1. Go to /setup-hybrid")
    print("2. Enter your OpenAI API key")
    print("3. Upload images for hybrid analysis")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

