"""
CNN Model for ISL Hand Gesture Classification
Trained on the 33-classes Indian Sign Language dataset.
Classifies hand gesture images into A-Z letters and 1-9 digits.
"""

import os
import numpy as np

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image

# Configuration
IMG_SIZE = 64  # Resize all images to 64x64
NUM_CLASSES = 35  # A-Z (26) + 1-9 (9)
BATCH_SIZE = 32
EPOCHS = 10
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'isl_cnn_model.keras')

# Class labels in sorted order (matching folder names)
CLASS_LABELS = sorted([
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
])


def build_model():
    """
    Build CNN model for ISL gesture classification.
    
    Architecture:
    - 3x Conv2D + MaxPool blocks for feature extraction
    - Flatten + Dense layers for classification
    - Dropout for regularization
    """
    model = keras.Sequential([
        # Input
        layers.Input(shape=(IMG_SIZE, IMG_SIZE, 1)),
        
        # Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Classification head
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def load_dataset(dataset_path):
    """
    Load images from the 33-classes dataset.
    Directory structure: dataset_path/<label>/<image>.jpg
    
    Returns (images, labels) as numpy arrays.
    """
    images = []
    labels = []
    
    print(f"Loading dataset from: {dataset_path}")
    
    for label_idx, label_name in enumerate(CLASS_LABELS):
        label_dir = os.path.join(dataset_path, label_name)
        if not os.path.isdir(label_dir):
            print(f"  Warning: Directory not found for label '{label_name}'")
            continue
        
        count = 0
        for img_file in os.listdir(label_dir):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            img_path = os.path.join(label_dir, img_file)
            try:
                img = Image.open(img_path).convert('L')  # Convert to grayscale
                img = img.resize((IMG_SIZE, IMG_SIZE))
                img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize
                images.append(img_array)
                labels.append(label_idx)
                count += 1
            except Exception as e:
                pass  # Skip corrupt images
        
        print(f"  Loaded {count} images for label '{label_name}'")
    
    images = np.array(images).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    labels = keras.utils.to_categorical(labels, NUM_CLASSES)
    
    print(f"Total: {len(images)} images loaded")
    return images, labels


def train_model(dataset_path):
    """Train the CNN model on the dataset."""
    # Load data
    images, labels = load_dataset(dataset_path)
    
    # Shuffle and split (80% train, 20% validation)
    indices = np.arange(len(images))
    np.random.shuffle(indices)
    images = images[indices]
    labels = labels[indices]
    
    split = int(0.8 * len(images))
    X_train, X_val = images[:split], images[split:]
    y_train, y_val = labels[:split], labels[split:]
    
    print(f"\nTraining set: {len(X_train)} images")
    print(f"Validation set: {len(X_val)} images")
    
    # Build and train
    model = build_model()
    model.summary()
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=1
    )
    
    # Save model
    model.save(MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    
    # Print final accuracy
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"Validation Accuracy: {val_acc * 100:.2f}%")
    
    return model, history


def load_trained_model():
    """Load the pre-trained CNN model."""
    if not os.path.exists(MODEL_PATH):
        print(f"No trained model found at {MODEL_PATH}")
        print("Please train the model first using: python cnn_model.py")
        return None
    
    model = keras.models.load_model(MODEL_PATH)
    print(f"Model loaded from: {MODEL_PATH}")
    return model


def predict_sign(model, image_path):
    """
    Predict the ISL sign label for a given image.
    
    Args:
        model: Trained Keras model
        image_path: Path to the image file
    
    Returns:
        dict with 'label', 'confidence', and 'all_predictions'
    """
    img = Image.open(image_path).convert('L')
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = img_array.reshape(1, IMG_SIZE, IMG_SIZE, 1)
    
    predictions = model.predict(img_array, verbose=0)[0]
    top_idx = np.argmax(predictions)
    
    return {
        'label': CLASS_LABELS[top_idx],
        'confidence': float(predictions[top_idx]),
        'all_predictions': {
            CLASS_LABELS[i]: float(predictions[i]) 
            for i in np.argsort(predictions)[-5:][::-1]
        }
    }


if __name__ == "__main__":
    import sys
    
    # Dataset path
    dataset_path = os.path.join(
        os.path.dirname(__file__), '..', 'data sets', '33 classes', 'Indian'
    )
    dataset_path = os.path.normpath(dataset_path)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        print("=" * 50)
        print("ISL CNN Model Training")
        print("=" * 50)
        train_model(dataset_path)
    elif len(sys.argv) > 1 and sys.argv[1] == 'predict':
        if len(sys.argv) < 3:
            print("Usage: python cnn_model.py predict <image_path>")
            sys.exit(1)
        model = load_trained_model()
        if model:
            result = predict_sign(model, sys.argv[2])
            print(f"Prediction: {result['label']} ({result['confidence']*100:.1f}%)")
            print(f"Top 5: {result['all_predictions']}")
    else:
        print("Usage:")
        print("  python cnn_model.py train           - Train the CNN model")
        print("  python cnn_model.py predict <image>  - Predict a sign from image")
