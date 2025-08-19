# src/data_cleaning.py
# --------------------------
# This script is responsible for cleaning and normalizing the raw job data
# collected from the ProLocums website. It reads the raw JSONL files,
# processes the data, and saves it in a clean, analyzable format.
# --------------------------

import json
import os
import glob
import re
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Import our new NLP feature generator
from nlp_feature_extraction import generate_nlp_features

# Define the path to the raw data
RAW_DATA_PATH = os.path.join('data', 'raw')
PROCESSED_DATA_PATH = os.path.join('data', 'processed')

def find_latest_raw_data_file() -> Optional[str]:
    """
    Finds the most recent raw data directory and returns the path to the jobs.jsonl file.

    Returns:
        Optional[str]: The full path to the latest jobs.jsonl file, or None if not found.
    """
    # List all subdirectories in the raw data path (they are named by date YYYY-MM-DD)
    date_dirs = [d for d in os.listdir(RAW_DATA_PATH) if os.path.isdir(os.path.join(RAW_DATA_PATH, d))]
    
    if not date_dirs:
        print("No raw data directories found.")
        return None
        
    # Sort directories by date to find the most recent
    latest_dir = sorted(date_dirs, reverse=True)[0]
    latest_file = os.path.join(RAW_DATA_PATH, latest_dir, 'jobs.jsonl')
    
    if os.path.exists(latest_file):
        return latest_file
    else:
        print(f"Error: jobs.jsonl not found in the latest directory: {latest_dir}")
        return None

def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Loads the raw JSONL data into a pandas DataFrame.

    Args:
        file_path (str): The path to the jobs.jsonl file.

    Returns:
        pd.DataFrame: A DataFrame containing the raw job data.
    """
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))
    
    return pd.DataFrame(records)

def parse_pay_rate(row: pd.Series) -> Optional[float]:
    """
    Extracts an hourly pay rate from the raw data.
    
    It first checks the 'RegularHR' column. If that is empty or zero,
    it falls back to searching for a rate in the 'Description' HTML.

    Args:
        row (pd.Series): A row from the raw jobs DataFrame.

    Returns:
        Optional[float]: The extracted hourly rate, or None if not found.
    """
    # 1. Check the structured 'RegularHR' column first.
    if pd.notna(row['RegularHR']) and row['RegularHR'] > 0:
        return float(row['RegularHR'])
        
    # 2. If no rate in 'RegularHR', search the description text.
    description = str(row['Description'])
    # Regex to find patterns like "$350/hr", "$300 / hr", "$350 per hour"
    match = re.search(r'\$(\d{2,4})\s*(?:/|per)\s*hr', description, re.IGNORECASE)
    if match:
        return float(match.group(1))
        
    return None

def extract_structured_from_description(html_content: str) -> Dict[str, Optional[str]]:
    """
    Parses HTML job description to extract structured data based on common headers.

    Args:
        html_content (str): The HTML string of the job description.

    Returns:
        Dict[str, Optional[str]]: A dictionary with extracted data.
    """
    if not isinstance(html_content, str):
        return {'coverage_type': None, 'schedule': None}

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\\n', strip=True)
    lines = text.split('\\n')

    extracted_data = {'coverage_type': None, 'schedule': None}
    keywords = {
        'coverage_type': ['Coverage Type', 'Coverage:'],
        'schedule': ['Schedule', 'Schedule:']
    }
    
    # Reverse keywords for easier popping
    active_section = None
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        # Check if the line is a header
        found_key = None
        for key, patterns in keywords.items():
            for pattern in patterns:
                if pattern.lower() in cleaned_line.lower():
                    found_key = key
                    break
            if found_key:
                break
        
        if found_key:
            active_section = found_key
            # Try to extract data from the same line as the header
            data_part = cleaned_line.lower().replace(found_key.lower(), '').strip(': ').strip()
            if data_part:
                extracted_data[active_section] = data_part
        elif active_section and not extracted_data[active_section]:
            # If we're in a section and haven't found data yet, this line is the data
            extracted_data[active_section] = cleaned_line
            active_section = None # Reset after capturing
            
    return extracted_data


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs all the cleaning and normalization steps on the DataFrame.

    Args:
        df (pd.DataFrame): The raw data DataFrame.

    Returns:
        pd.DataFrame: The cleaned and normalized DataFrame.
    """
    print("Cleaning and normalizing data...")
    
    # Apply the pay rate parsing function to each row
    df['rate_hourly'] = df.apply(parse_pay_rate, axis=1)
    
    # Normalize to a daily rate, assuming an 8-hour workday
    # This is an explicit assumption as per the project plan.
    df['rate_daily'] = df['rate_hourly'] * 8
    
    # Convert date columns to datetime objects
    for col in ['CreartedOn', 'StartDate', 'EndDate', 'PostedOn', 'scrape_timestamp_utc']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # --- Feature Engineering: Job Duration ---
    # Calculate the duration of the job in days
    df['job_duration_days'] = (df['EndDate'] - df['StartDate']).dt.days
    
    # Replace zero rates with NaN (Not a Number) to represent missing data
    df['rate_hourly'] = df['rate_hourly'].replace({0: np.nan})
    df['rate_daily'] = df['rate_daily'].replace({0: np.nan})

    print("\nPay rate cleaning summary:")
    print(f"  - Found {df['rate_hourly'].notna().sum()} jobs with an hourly rate.")
    print(f"  - Min hourly rate: ${df['rate_hourly'].min():.2f}")
    print(f"  - Max hourly rate: ${df['rate_hourly'].max():.2f}")
    print(f"  - Median hourly rate: ${df['rate_hourly'].median():.2f}")
        
    # Column Selection and Renaming
    # Select a subset of columns and rename them for clarity
    column_mapping = {
        'Id': 'job_id',
        'Title': 'job_title',
        'SpecialtyName': 'specialty',
        'StateName': 'state',
        'StateId': 'state_id', # Add state_id for mapping
        'City': 'city',
        'Description': 'description_html',
        'CreartedOn': 'posted_date',
        'StartDate': 'start_date',
        'EndDate': 'end_date',
        'Source': 'source',
        'JobIdStrnew': 'job_id_string',
        'scrape_timestamp_utc': 'scrape_timestamp_utc'
    }
    
    # We will add our new rate columns to the final selection
    final_columns = list(column_mapping.values()) + [
        'rate_hourly', 'rate_daily', 'job_duration_days'
    ]
    
    df_cleaned = df.rename(columns=column_mapping)
    df_cleaned = df_cleaned[final_columns]

    # Text Cleaning and Standardization
    for col in ['job_title', 'specialty', 'state', 'city', 'source']:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].str.strip()

    # URL Creation
    # The base URL for a job posting seems to be /job-detail/{job_id_string}
    base_job_url = "https://www.prolocums.com/job-detail/"
    df_cleaned['job_url'] = base_job_url + df_cleaned['job_id_string']
    
    # Deduplication
    # Sort by the scrape timestamp so the most recent scrape is first.
    df_cleaned = df_cleaned.sort_values(by='scrape_timestamp_utc', ascending=False)
    
    # Define the key for identifying unique jobs
    deduplication_key = ['job_url', 'job_title', 'posted_date']
    
    # Drop duplicates, keeping the first (most recent) record
    original_rows = len(df_cleaned)
    df_deduplicated = df_cleaned.drop_duplicates(subset=deduplication_key, keep='first')
    new_rows = len(df_deduplicated)
    
    print(f"\nDeduplication summary:")
    print(f"  - Original rows: {original_rows}")
    print(f"  - Dropped {original_rows - new_rows} duplicate rows.")
    print(f"  - Final rows: {new_rows}")
        
    # Final Step: Generate NLP Features
    # This must be done after deduplication to save processing time
    df_final = generate_nlp_features(df_deduplicated.copy())
        
    return df_final

def save_processed_data(df: pd.DataFrame) -> None:
    """
    Saves the cleaned DataFrame to a Parquet file.

    Args:
        df (pd.DataFrame): The cleaned data to save.
    """
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    output_path = os.path.join(PROCESSED_DATA_PATH, 'jobs.parquet')
    df.to_parquet(output_path, index=False)
    print(f"Successfully saved cleaned data to {output_path}")

def main():
    """
    Main function to orchestrate the data cleaning process.
    """
    print("Starting data cleaning process...")
    
    latest_file = find_latest_raw_data_file()
    
    if latest_file:
        print(f"Loading raw data from: {latest_file}")
        raw_df = load_raw_data(latest_file)
        
        print("Raw data loaded. Shape:", raw_df.shape)
        print("Columns:", raw_df.columns.tolist())
        
        cleaned_df = clean_data(raw_df.copy())
        
        print("\nCleaned data preview (first 5 rows):")
        print(cleaned_df.head())
        
        save_processed_data(cleaned_df)

if __name__ == "__main__":
    main()
