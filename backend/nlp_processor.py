"""
NLP Processor for Indian Sign Language Generator
Converts English text into ISL grammar structure.
ISL uses Subject-Object-Verb (SOV) order and drops helper words.
"""

import nltk
import os
import re

# Download required NLTK data
nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.insert(0, nltk_data_dir)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', download_dir=nltk_data_dir)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', download_dir=nltk_data_dir)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng', download_dir=nltk_data_dir)

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag

# ISL stop words - words that are typically omitted in ISL
ISL_STOP_WORDS = {
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'the', 'a', 'an',
    'do', 'does', 'did',
    'has', 'have', 'had',
    'will', 'shall', 'would', 'should', 'could', 'might',
    'to', 'of', 'for',
    'it', 'its',
}

# Common word signs available in our dataset (expand as needed)
# These are words that have dedicated sign gestures
KNOWN_WORD_SIGNS = set()  # We only have alphabet & number signs in our dataset

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """
    Full NLP pipeline to convert English text to ISL-compatible tokens.
    
    Steps:
    1. Clean and normalize text
    2. Tokenize into words
    3. Remove ISL stop words
    4. Lemmatize words to root form
    5. Reorder to ISL grammar (SOV)
    
    Returns a list of tokens ready for sign mapping.
    """
    # Step 1: Clean text
    text = text.strip().lower()
    text = re.sub(r'[^\w\s\?]', '', text)  # Remove punctuation except ?
    
    if not text:
        return []
    
    # Step 2: Tokenize
    tokens = word_tokenize(text)
    
    # Step 3: POS tagging (for grammar reordering)
    tagged = pos_tag(tokens)
    
    # Step 4: Remove ISL stop words
    filtered = [(word, tag) for word, tag in tagged if word not in ISL_STOP_WORDS]
    
    # Step 5: Lemmatize
    lemmatized = []
    for word, tag in filtered:
        # Convert POS tag to WordNet format
        if tag.startswith('V'):
            lemma = lemmatizer.lemmatize(word, pos='v')
        elif tag.startswith('N'):
            lemma = lemmatizer.lemmatize(word, pos='n')
        elif tag.startswith('J'):
            lemma = lemmatizer.lemmatize(word, pos='a')
        else:
            lemma = lemmatizer.lemmatize(word)
        lemmatized.append((lemma, tag))
    
    # Step 6: Reorder to ISL grammar (SOV)
    reordered = reorder_to_isl(lemmatized)
    
    return reordered


def reorder_to_isl(tagged_tokens):
    """
    Reorder English SVO to ISL SOV structure.
    
    English: "I eat food" (SVO)
    ISL:     "I food eat" (SOV)
    
    English: "What is your name?"
    ISL:     "your name what"
    
    Simple heuristic approach:
    - WH-words (what, who, where, when, why, how) move to end
    - Verbs move to end
    - Subject and Object stay in relative order
    """
    wh_words = {'what', 'who', 'where', 'when', 'why', 'how', 'which'}
    
    subjects = []
    objects_and_modifiers = []
    verbs = []
    wh = []
    
    for word, tag in tagged_tokens:
        if word in wh_words:
            wh.append(word)
        elif tag.startswith('V'):
            verbs.append(word)
        elif tag.startswith('PRP') or tag.startswith('NN') and not subjects:
            # First noun/pronoun is likely subject
            subjects.append(word)
        else:
            objects_and_modifiers.append(word)
    
    # ISL order: Subject + Objects/Modifiers + Verb + WH-word
    result = subjects + objects_and_modifiers + verbs + wh
    
    # If result is empty but we had tokens, just return them in original order
    if not result and tagged_tokens:
        result = [word for word, tag in tagged_tokens]
    
    return result


def text_to_sign_sequence(text):
    """
    Convert text to a sequence of sign labels.
    
    For each word:
    - If the word has a dedicated sign → use that sign
    - Otherwise → spell it out letter by letter
    
    Returns list of dicts: [{"type": "word"|"letter", "label": "...", "original": "..."}]
    """
    tokens = preprocess_text(text)
    
    if not tokens:
        return []
    
    sequence = []
    
    for token in tokens:
        if token in KNOWN_WORD_SIGNS:
            # Word-level sign
            sequence.append({
                "type": "word",
                "label": token,
                "original": token
            })
        else:
            # Spell out letter by letter
            for char in token:
                if char.isalpha():
                    sequence.append({
                        "type": "letter",
                        "label": char.upper(),
                        "original": token
                    })
                elif char.isdigit():
                    sequence.append({
                        "type": "number",
                        "label": char,
                        "original": token
                    })
            # Add a space/pause marker between words
            sequence.append({
                "type": "space",
                "label": "SPACE",
                "original": " "
            })
    
    # Remove trailing space
    if sequence and sequence[-1]["type"] == "space":
        sequence.pop()
    
    return sequence


# Quick test
if __name__ == "__main__":
    test_sentences = [
        "What is your name?",
        "I am going to school",
        "How are you?",
        "Hello my friend",
        "Thank you very much",
    ]
    
    for sentence in test_sentences:
        print(f"\nInput:  {sentence}")
        tokens = preprocess_text(sentence)
        print(f"ISL:    {' '.join(tokens)}")
        signs = text_to_sign_sequence(sentence)
        labels = [s['label'] for s in signs if s['type'] != 'space']
        print(f"Signs:  {labels}")
