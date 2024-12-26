import requests
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Dynamic project path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Load environment variables explicitly
env_path = project_root / "config/settings.env"
load_dotenv(dotenv_path=env_path)

from utils.logger import get_logger

logger = get_logger("Crunchbase")

def fetch_crunchbase_data():
    """
    Fetches data from Crunchbase API.
    Returns a list of startups with their details.
    """
    api_key = os.getenv("CRUNCHBASE_API_KEY")
    if not api_key:
        raise ValueError("Crunchbase API key not found in environment variables.")

    url = "https://api.crunchbase.com/v3.1/organizations"
    params = {"user_key": api_key, "page": 1}
    response = requests.get(url, params=params)

    # Log the full response for debugging
    logger.debug(f"Raw response content: {response.text}")

    if response.status_code != 200:
        logger.error(f"Crunchbase API returned status code {response.status_code}")
        raise Exception("Failed to fetch data from Crunchbase.")

    data = response.json()

    # Log the structure of the response for debugging
    logger.debug(f"Response structure: {data.keys()}")
    if "data" in data:
        logger.debug(f"Data structure: {data['data'].keys()}")

    startups = [
        {
            "name": org.get("properties", {}).get("name"),
            "url": f"https://www.crunchbase.com/organization/{org.get('properties', {}).get('permalink')}",
            "industry": org.get("properties", {}).get("categories", []),
        }
        for org in data.get("data", {}).get("items", [])
    ]
    return startups

if __name__ == "__main__":
    logger.info("Starting Crunchbase data fetch...")
    logger.info(f"Loaded Crunchbase API Key: {os.getenv('CRUNCHBASE_API_KEY')}")
    try:
        startups = fetch_crunchbase_data()
        logger.info(f"Fetched {len(startups)} startups from Crunchbase.")
        for startup in startups[:5]:  # Show the first 5 startups
            logger.info(startup)
    except Exception as e:
        logger.error(f"An error occurred: {e}")