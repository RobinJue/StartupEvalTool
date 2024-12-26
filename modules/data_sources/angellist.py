import requests
import os
import sys
from pathlib import Path

# Dynamic project path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from utils.logger import get_logger  

logger = get_logger("AngelList")

def fetch_angellist_data():
    """
    Fetches data from AngelList API.
    Returns a list of startups with their details.
    """
    api_key = os.getenv("ANGELLIST_API_KEY")
    if not api_key:
        raise ValueError("AngelList API key not found in environment variables.")

    url = "https://api.angel.co/1/startups"
    params = {"access_token": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        logger.error(f"AngelList API returned status code {response.status_code}")
        raise Exception("Failed to fetch data from AngelList.")

    data = response.json()
    startups = [
        {"name": startup["name"], "url": startup["angellist_url"], "industry": startup["markets"]}
        for startup in data.get("startups", [])
    ]
    return startups