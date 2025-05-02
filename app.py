from flask import Flask, request, jsonify, render_template
from googletrans import Translator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        text = data['text']
        source_lang = data.get('source_lang', 'auto')  # Default to auto-detect
        
        # Translate the text to English
        translation = translator.translate(text, src=source_lang, dest='en')
        
        return jsonify({
            'original_text': text,
            'translated_text': translation.text,
            'source_language': translation.src,
            'confidence': translation.extra_data.get('confidence', None)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 