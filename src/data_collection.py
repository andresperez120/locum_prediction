# src/data_collection.py
# --------------------------
# This script is responsible for collecting all locum tenens job postings
# from ProLocums by handling the site's pagination API.
# --------------------------

import json
import os
import re
import math
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Constants
BASE_URL = "https://www.prolocums.com"
JOB_SEARCH_URL = f"{BASE_URL}/job-search"
PAGINATION_URL = f"{BASE_URL}/Default/GetPaginationAjax"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Referer': JOB_SEARCH_URL
}
PAGE_SIZE = 12 # Based on inspection of the site

def fetch_page_html() -> Optional[str]:
    """Fetches the HTML content of the job search page."""
    try:
        response = requests.get(JOB_SEARCH_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error fetching initial page HTML: {e}")
        return None

def extract_initial_jobs(html: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[int]]:
    """Extracts the first page of jobs and the total number of jobs from the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    job_script_text = None
    for script in scripts:
        if script.string and 'var JobList = {' in script.string:
            job_script_text = script.string
            break

    if not job_script_text:
        return None, None

    match = re.search(r'var JobList = ({.*?});', job_script_text, re.DOTALL)
    if not match:
        return None, None

    try:
        data = json.loads(match.group(1))
        jobs = data.get("Data", {}).get("data", [])
        total_jobs = jobs[0].get('Totalrow', 0) if jobs else 0
        return jobs, total_jobs
    except (json.JSONDecodeError, KeyError, IndexError):
        return None, None

def fetch_paginated_jobs(page_number: int) -> Optional[List[Dict[str, Any]]]:
    """Fetches a specific page of job listings from the pagination API."""
    payload = {
        "StateId": "",
        "DegreeId": "",
        "SpecialtyId": "",
        "pageSize": PAGE_SIZE,
        "page": page_number,
    }
    try:
        response = requests.post(PAGINATION_URL, headers=HEADERS, data=payload, timeout=30)
        response.raise_for_status()
        # The response is nested, e.g., {"data": {"Data": [...]}}
        return response.json().get("data", {}).get("Data", [])
    except RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON for page {page_number}.")
    return None

def save_jobs_to_jsonl(jobs: List[Dict[str, Any]]) -> None:
    """Saves a list of job postings to a JSONL file."""
    today = datetime.utcnow()
    output_dir = os.path.join('data', 'raw', today.strftime('%Y-%m-%d'))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'jobs.jsonl')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for job in jobs:
            job['scrape_timestamp_utc'] = today.isoformat()
            f.write(json.dumps(job) + '\n')
            
    print(f"\nSuccessfully saved a total of {len(jobs)} jobs to {output_path}")

def main():
    """Main function to orchestrate the full data collection process."""
    print("Starting full data scrape...")
    html = fetch_page_html()
    if not html:
        return

    initial_jobs, total_jobs = extract_initial_jobs(html)
    if not initial_jobs or not total_jobs:
        print("Could not extract initial jobs or total job count. Aborting.")
        return

    print(f"Found {total_jobs} total job listings across all pages.")
    all_jobs = initial_jobs
    
    total_pages = math.ceil(total_jobs / PAGE_SIZE)
    print(f"Calculated {total_pages} total pages to scrape.")
    
    # Page numbers for the API seem to be 0-indexed, but the first page's data
    # is already included, so we start fetching from page 1.
    for page_num in range(1, total_pages):
        print(f"Fetching page {page_num + 1} of {total_pages}...")
        paginated_jobs = fetch_paginated_jobs(page_num)
        if paginated_jobs:
            all_jobs.extend(paginated_jobs)
        # Be a good web citizen and pause between requests
        time.sleep(0.5)

    if all_jobs:
        save_jobs_to_jsonl(all_jobs)
        print("\n--- Sample Job Listing from final batch ---")
        print(json.dumps(all_jobs[-1], indent=2))
        print("-------------------------------------------\n")

if __name__ == "__main__":
    main()
