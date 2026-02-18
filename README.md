# Speech to Indian Sign Language (ISL) Generator

A full-stack web application that converts spoken or typed English into Indian Sign Language (ISL) hand gesture sequences. The system leverages Natural Language Processing (NLP) for grammar transformation and a Convolutional Neural Network (CNN) for gesture classification.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Datasets](#datasets)
- [NLP Pipeline](#nlp-pipeline)
- [CNN Model](#cnn-model)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [License](#license)

---

## Overview

Communication between hearing individuals and the deaf community remains a significant challenge. This application bridges that gap by automatically translating English speech or text into a visual sequence of ISL hand gestures.

The system processes input through a multi-stage pipeline: speech recognition, natural language processing with ISL grammar transformation, sign mapping against curated datasets, and visual output as an animated slideshow of gesture images.

---

## Features

- **Speech-to-Text**: Real-time voice capture and transcription using the Web Speech API.
- **Text Input**: Manual text entry for direct translation.
- **ISL Grammar Conversion**: Automatic reordering of English sentences to ISL Subject-Object-Verb (SOV) structure.
- **Stop Word Removal**: Elimination of words that do not have ISL equivalents (e.g., "is", "am", "the").
- **Sign Image Slideshow**: Animated playback of gesture images with play, pause, previous, next, and replay controls.
- **Adjustable Playback Speed**: Four speed settings (0.5x, 1x, 1.5x, 2x).
- **Interactive Timeline**: Clickable sign chips for direct navigation to any gesture in the sequence.
- **CNN Classification**: Deep learning model for hand gesture recognition trained on 42,000+ images.
- **Responsive Design**: Fully functional across desktop and mobile devices.

---

## System Architecture

```
User Input (Speech / Text)
        |
        v
  [Web Speech API]  -->  English Text
        |
        v
  [NLP Processor]   -->  Tokenization, Lemmatization, POS Tagging
        |
        v
  [ISL Grammar]     -->  SOV Reordering, Stop Word Removal
        |
        v
  [Sign Mapper]     -->  Word-to-Sign Lookup (with letter fallback)
        |
        v
  [Image Server]    -->  Gesture images from dataset
        |
        v
  [Frontend]        -->  Animated sign slideshow
```

---

## Technology Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Frontend   | React 19, Vite 7              |
| Backend    | Flask, Python                  |
| NLP        | NLTK (tokenization, lemmatization, POS tagging) |
| ML/AI      | TensorFlow, Keras (CNN)        |
| Speech     | Web Speech API (browser-native)|
| Styling    | Vanilla CSS (custom design system) |

---

## Project Structure

```
Speech-to-Indian-Sign-Language/
|
|-- backend/
|   |-- server.py              # Flask API server
|   |-- nlp_processor.py       # NLP pipeline for ISL grammar conversion
|   |-- cnn_model.py           # CNN model architecture, training, and inference
|   |-- requirements.txt       # Python dependencies
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx            # Application root with routing
|   |   |-- index.css          # Design system and global styles
|   |   |-- main.jsx           # Entry point
|   |   |-- components/
|   |   |   |-- SpeechInput.jsx    # Voice and text input component
|   |   |   |-- SignDisplay.jsx    # Gesture slideshow and playback controls
|   |   |-- pages/
|   |       |-- Home.jsx       # Main translation interface
|   |       |-- About.jsx      # Project documentation and pipeline details
|   |-- package.json
|   |-- vite.config.js
|
|-- data sets/
|   |-- 33 classes/Indian/     # CNN training dataset (A-Z, 1-9)
|   |-- ISL General/           # Display dataset (clearer gesture images)
|
|-- .gitignore
|-- LICENSE
```

---

## Datasets

### 33 Classes - Indian ISL (Training)

| Property         | Value              |
|------------------|--------------------|
| Classes          | 35 (A-Z and 1-9)   |
| Images per class | ~1,200              |
| Total images     | ~42,000             |
| Format           | JPG (~6 KB each)    |
| Purpose          | CNN model training  |

### ISL General Gestures (Display)

| Property         | Value               |
|------------------|---------------------|
| Classes          | 33                   |
| Images per class | ~300                 |
| Total images     | ~9,900               |
| Format           | PNG (~30 KB each)    |
| Purpose          | Visual output display|

The system prioritizes ISL General images for display due to their higher clarity. If a sign is unavailable, it falls back to the 33 Classes dataset.

---

## NLP Pipeline

The NLP processor transforms English text into ISL-compatible grammar:

1. **Text Cleaning**: Converts to lowercase and removes special characters.
2. **Tokenization**: Splits text into individual words using NLTK.
3. **Stop Word Removal**: Removes words without ISL equivalents ("is", "am", "are", "the", "a", "an", "was", "were", "be", "been", "being", "do", "does", "did", "have", "has", "had").
4. **Lemmatization**: Reduces words to their base form using WordNet Lemmatizer.
5. **POS Tagging**: Identifies parts of speech for grammar reordering.
6. **ISL Reordering**: Transforms English SVO order to ISL SOV order. WH-question words are moved to the end of the sentence.

### Example Transformations

| English Input              | ISL Output          |
|---------------------------|---------------------|
| What is your name?        | your name what      |
| I am going to school      | i school go         |
| She likes reading books   | she book read like  |

---

## CNN Model

### Architecture

```
Input: 64 x 64 x 1 (grayscale)

Block 1: Conv2D(32, 3x3) -> BatchNorm -> MaxPool(2x2) -> Dropout(0.25)
Block 2: Conv2D(64, 3x3) -> BatchNorm -> MaxPool(2x2) -> Dropout(0.25)
Block 3: Conv2D(128, 3x3) -> BatchNorm -> MaxPool(2x2) -> Dropout(0.25)

Classification: Flatten -> Dense(256) -> BatchNorm -> Dropout(0.5) -> Dense(35, softmax)

Optimizer: Adam
Loss: Categorical Crossentropy
```

### Training

To train the model:

```bash
cd backend
pip install tensorflow
python cnn_model.py train
```

Training uses an 80/20 train-validation split with 10 epochs and a batch size of 32.

### Prediction

To classify a single image:

```bash
python cnn_model.py predict <path_to_image>
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

The first run will automatically download required NLTK data packages (punkt, wordnet, averaged_perceptron_tagger, stopwords).

### Frontend Setup

```bash
cd frontend
npm install
```

---

## Usage

### 1. Start the Backend Server

```bash
cd backend
python server.py
```

The Flask server starts on `http://localhost:5000`.

### 2. Start the Frontend Development Server

Open a separate terminal:

```bash
cd frontend
npm run dev
```

The React application starts on `http://localhost:5173`.

### 3. Access the Application

Open `http://localhost:5173` in a web browser (Google Chrome recommended for speech recognition support).

1. Type a sentence in the input field or click the microphone icon to speak.
2. Click the Translate button.
3. The application displays the ISL gesture sequence as an animated slideshow.
4. Use the playback controls to navigate through individual signs.

---

## API Reference

### Health Check

```
GET /api/health
```

Returns server status and dataset availability.

### Process Text

```
POST /api/process-text
Content-Type: application/json

{
  "text": "What is your name?"
}
```

Returns the ISL token sequence and sign image URLs.

### Get Sign Image

```
GET /api/sign-image/<label>
```

Returns the gesture image for the specified label (e.g., A, B, 1, 2).

Optional query parameter: `?source=general|33classes`

### List Available Signs

```
GET /api/available-signs
```

Returns all available sign labels across both datasets.

---

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
