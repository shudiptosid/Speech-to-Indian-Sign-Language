"""
Flask Backend Server for ISL Generator
Provides REST API for text → ISL sign conversion.
"""

import os
import sys
import json
import random
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from nlp_processor import text_to_sign_sequence, preprocess_text

app = Flask(__name__)
CORS(app)

# Dataset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

ISL_GENERAL_PATH = os.path.join(PROJECT_DIR, 'data sets', 'ISL General')
CLASSES_33_PATH = os.path.join(PROJECT_DIR, 'data sets', '33 classes', 'Indian')

# Available labels in each dataset
ISL_GENERAL_LABELS = set()
CLASSES_33_LABELS = set()

def init_labels():
    """Scan dataset directories to find available labels."""
    global ISL_GENERAL_LABELS, CLASSES_33_LABELS
    
    if os.path.exists(ISL_GENERAL_PATH):
        ISL_GENERAL_LABELS = {
            d.upper() for d in os.listdir(ISL_GENERAL_PATH)
            if os.path.isdir(os.path.join(ISL_GENERAL_PATH, d))
        }
        print(f"ISL General labels: {sorted(ISL_GENERAL_LABELS)}")
    
    if os.path.exists(CLASSES_33_PATH):
        CLASSES_33_LABELS = {
            d.upper() for d in os.listdir(CLASSES_33_PATH)
            if os.path.isdir(os.path.join(CLASSES_33_PATH, d))
        }
        print(f"33 Classes labels: {sorted(CLASSES_33_LABELS)}")


def get_sign_image_path(label):
    """
    Get the path to a sign image for the given label.
    Prefers ISL General (clearer images), falls back to 33 Classes.
    Returns a random image from the available ones.
    """
    label_upper = label.upper()
    label_lower = label.lower()
    
    # Try ISL General first (clearer, larger images)
    isl_dir = os.path.join(ISL_GENERAL_PATH, label_lower)
    if os.path.isdir(isl_dir):
        images = [f for f in os.listdir(isl_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            # Pick a representative image (middle of set for consistency)
            chosen = images[len(images) // 2]
            return os.path.join(isl_dir, chosen)
    
    # Fallback to 33 Classes
    cls_dir = os.path.join(CLASSES_33_PATH, label_upper)
    if os.path.isdir(cls_dir):
        images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            chosen = images[len(images) // 2]
            return os.path.join(cls_dir, chosen)
    
    return None


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'isl_general_labels': len(ISL_GENERAL_LABELS),
        'classes_33_labels': len(CLASSES_33_LABELS),
    })


@app.route('/api/process-text', methods=['POST'])
def process_text():
    """
    Convert English text to ISL sign sequence.
    
    Request body: { "text": "What is your name?" }
    
    Response: {
        "original_text": "What is your name?",
        "isl_tokens": ["your", "name", "what"],
        "signs": [
            {"type": "letter", "label": "Y", "original": "your", "image_url": "/api/sign-image/Y"},
            ...
        ]
    }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" in request body'}), 400
    
    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Empty text provided'}), 400
    
    # Process through NLP pipeline
    isl_tokens = preprocess_text(text)
    sign_sequence = text_to_sign_sequence(text)
    
    # Add image URLs to sign sequence
    for sign in sign_sequence:
        if sign['type'] == 'space':
            sign['image_url'] = None
            sign['available'] = False
        else:
            label = sign['label']
            img_path = get_sign_image_path(label)
            sign['available'] = img_path is not None
            sign['image_url'] = f'/api/sign-image/{label}' if img_path else None
    
    return jsonify({
        'original_text': text,
        'isl_tokens': isl_tokens,
        'signs': sign_sequence,
        'total_signs': len([s for s in sign_sequence if s['type'] != 'space'])
    })


@app.route('/api/sign-image/<label>', methods=['GET'])
def sign_image(label):
    """
    Serve a sign image for the given label.
    
    URL params:
    - label: The sign label (e.g., 'A', 'B', '1', '2')
    - ?source=general|33classes (optional, default: auto)
    """
    source = request.args.get('source', 'auto')
    
    img_path = None
    
    if source == 'general':
        isl_dir = os.path.join(ISL_GENERAL_PATH, label.lower())
        if os.path.isdir(isl_dir):
            images = [f for f in os.listdir(isl_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if images:
                img_path = os.path.join(isl_dir, images[len(images) // 2])
    elif source == '33classes':
        cls_dir = os.path.join(CLASSES_33_PATH, label.upper())
        if os.path.isdir(cls_dir):
            images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if images:
                img_path = os.path.join(cls_dir, images[len(images) // 2])
    else:
        img_path = get_sign_image_path(label)
    
    if img_path and os.path.exists(img_path):
        return send_file(img_path, mimetype='image/png')
    
    return jsonify({'error': f'No image found for label: {label}'}), 404


@app.route('/api/available-signs', methods=['GET'])
def available_signs():
    """Return list of all available sign labels."""
    all_labels = sorted(ISL_GENERAL_LABELS | CLASSES_33_LABELS)
    return jsonify({
        'labels': all_labels,
        'total': len(all_labels),
        'isl_general': sorted(ISL_GENERAL_LABELS),
        'classes_33': sorted(CLASSES_33_LABELS)
    })


if __name__ == '__main__':
    print("=" * 50)
    print("ISL Generator Backend Server")
    print("=" * 50)
    
    init_labels()
    
    print(f"\nDataset paths:")
    print(f"  ISL General: {ISL_GENERAL_PATH}")
    print(f"  33 Classes:  {CLASSES_33_PATH}")
    print(f"\nStarting server on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
