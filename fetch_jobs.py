"""
fetch_jobs.py
Day 1 script: pulls real job postings from the Adzuna API and saves each
response as a JSON file in data/raw/, so we always have the raw data saved
even before we build the database in Day 2.
"""

import requests
import json
import os
from datetime import datetime

from config import ADZUNA_APP_ID, ADZUNA_APP_KEY

# ---- Settings you can tweak ----
COUNTRY = "in"          # "in" = India, "us" = United States, "gb" = UK, etc.
RESULTS_PER_PAGE = 50   # max Adzuna allows per page on the free tier
SEARCH_QUERIES = [
    {"what": "data analyst", "where": ""},
    {"what": "python developer", "where": ""},
    {"what": "data scientist", "where": ""},
    {"what": "sql developer", "where": ""},
]
OUTPUT_DIR = "data/raw"


def fetch_jobs(what, where=""):
    """Calls the Adzuna API for one search query and returns the JSON response."""
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": what,
    }
    if where:
        params["where"] = where

    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"  FAILED ({response.status_code}) for query: {what} | {where}")
        print(f"  Response: {response.text[:200]}")
        return None


def save_json(data, query_label):
    """Saves the JSON response to disk with a timestamp in the filename."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_label = query_label.replace(" ", "_")
    filename = f"{OUTPUT_DIR}/{safe_label}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    num_jobs = len(data.get("results", []))
    print(f"  Saved {num_jobs} jobs -> {filename}")


def main():
    print("Starting job fetch run...\n")

    for query in SEARCH_QUERIES:
        what = query["what"]
        where = query["where"]
        label = f"{what}_{where}" if where else what

        print(f"Fetching: {what} {('in ' + where) if where else ''}")
        data = fetch_jobs(what, where)

        if data:
            save_json(data, label)
        else:
            print("  Skipping save due to failed request.\n")

    print("\nDone. Check the data/raw folder for your saved JSON files.")


if __name__ == "__main__":
    main()