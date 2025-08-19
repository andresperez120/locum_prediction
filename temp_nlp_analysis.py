# temp_nlp_analysis.py
# -----------------------
# This is a temporary, one-off script to analyze the job description text
# and identify the most common and relevant keywords and bigrams (two-word phrases).
# The output of this script will inform the feature engineering logic in the main project.
# -----------------------

import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import json
from typing import Optional

# --- Setup ---
# Ensure you have the necessary NLTK data
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')

# Use the raw data path for this analysis
RAW_DATA_PATH = os.path.join('data', 'raw')

def find_latest_raw_data_file() -> Optional[str]:
    date_dirs = [d for d in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, d))]
    if not date_dirs:
        return None
    latest_dir = sorted(date_dirs, reverse=True)[0]
    return os.path.join(RAW_DATA_PATH, latest_dir, 'jobs.jsonl')

# --- Functions ---

def clean_html_to_text(html: str) -> str:
    """Converts HTML to clean, lowercased text."""
    if not isinstance(html, str):
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text.lower()

def get_most_common_phrases(series: pd.Series, n: int = 2, top_k: int = 50):
    """
    Finds the most common n-grams (phrases) in a series of text.
    """
    # Define a list of common but irrelevant words to exclude
    custom_stop_words = set(stopwords.words('english')).union([
        'specialty', 'physician', 'opportunity', 'job', 'locum', 'tenens',
        'rate', 'schedule', 'details', 'position', 'description', 'work',
        'required', 'requirements', 'coverage', 'type', 'start', 'date',
        'contact', 'information', 'email', 'phone', 'us', 'call', 'details',
        'per', 'hour', 'day', 'week', 'month', 'year', 'pm', 'am'
    ])

    all_phrases = []
    for i, text in enumerate(series):
        # Remove punctuation and numbers, but keep spaces
        text = re.sub(r'[^a-z\\s]', ' ', text)
        words = text.split()
        
        # Filter out stop words
        filtered_words = [word for word in words if word not in custom_stop_words and len(word) > 2]
        
        # Generate n-grams
        n_grams = ngrams(filtered_words, n)
        all_phrases.extend([' '.join(grams) for grams in n_grams])
        
    return Counter(all_phrases).most_common(top_k)

# --- Main Execution ---

if __name__ == "__main__":
    print("Starting NLP analysis of job descriptions...")
    
    latest_file = find_latest_raw_data_file()
    if not latest_file:
        print("Error: No raw data file found.")
    else:
        # Load raw data directly to get full descriptions
        records = [json.loads(line) for line in open(latest_file, 'r')]
        df = pd.DataFrame(records)
        
        # 1. Clean the HTML descriptions
        df['description_text'] = df['Description'].apply(clean_html_to_text)
        
        # 2. Find the most common bigrams (two-word phrases)
        print("\\n--- Most Common Two-Word Phrases (Bigrams) ---")
        common_bigrams = get_most_common_phrases(df['description_text'], n=2, top_k=30)
        for phrase, count in common_bigrams:
            print(f"  - '{phrase}' (appeared {count} times)")
            
        # 3. Find the most common trigrams (three-word phrases)
        print("\\n--- Most Common Three-Word Phrases (Trigrams) ---")
        common_trigrams = get_most_common_phrases(df['description_text'], n=3, top_k=20)
        for phrase, count in common_trigrams:
            print(f"  - '{phrase}' (appeared {count} times)")

        print("\\nAnalysis complete.")
        print("Review the phrases above to identify strong candidates for keyword features.")
