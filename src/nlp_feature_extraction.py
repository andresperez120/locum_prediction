# src/nlp_feature_extraction.py
# ---------------------------------
# This module contains all functions related to Natural Language Processing (NLP)
# for extracting structured features from unstructured job description text.
# ---------------------------------

from typing import List, Dict, Any
import pandas as pd
from bs4 import BeautifulSoup
import re

# Keyword Definitions
# These keywords are derived from the analysis of the most common phrases.
KEYWORD_FEATURES = {
    'is_board_certified': ['board certified', 'board certification', 'board eligible'],
    'has_weekend_shift': ['monday friday', 'weekend', 'weekends'],
    'is_trauma_center': ['trauma level'],
    'requires_acls': ['acls bls', 'acls atls', 'atls bls pals'],
    'uses_epic_emr': ['emr epic', 'emr system epic']
}

def extract_text_from_bullets(html: str) -> str:
    """
    Parses HTML to find all list items (<li>) and extracts their text.
    This focuses the analysis on the most structured part of the description.
    """
    if not isinstance(html, str):
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    bullets = [li.get_text() for li in soup.find_all('li')]
    return ' '.join(bullets).lower()

def search_for_keywords(text: str, keywords: List[str]) -> int:
    """
    Searches a given text for the presence of any keyword from a list.
    Returns 1 if found, 0 otherwise.
    """
    for keyword in keywords:
        if keyword in text:
            return 1
    return 0

def generate_nlp_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function to orchestrate the NLP feature generation process.
    It extracts text from bullet points and then creates binary flag features
    based on the presence of predefined keywords.

    Args:
        df (pd.DataFrame): DataFrame with a 'description_html' column.

    Returns:
        pd.DataFrame: The original DataFrame augmented with new NLP features.
    """
    print("Generating NLP features from job descriptions...")
    
    # 1. Extract text only from bullet points (<li> tags) for higher signal
    df['bullet_text'] = df['description_html'].apply(extract_text_from_bullets)
    
    # Create a binary flag for each keyword group
    for feature_name, keywords in KEYWORD_FEATURES.items():
        print(f"  - Creating feature: {feature_name}")
        df[feature_name] = df['bullet_text'].apply(lambda text: search_for_keywords(text, keywords))
        
    # Drop the intermediate text column
    df = df.drop(columns=['bullet_text'])
    
    print("NLP feature generation complete.")
    return df
