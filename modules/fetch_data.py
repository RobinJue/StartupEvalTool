import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the root directory of the project to sys.path (adjusted for project structure)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'code')))

from modules.data_sources.website_scraping import website_scraping_main

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_startup_data(startup_name):
    """
    Fetches data for the specified startup from various sources.
    """
    logger.info(f"Starting data fetch for {startup_name}...")

    # Fetch data from the website using website_scraping_main function
    try:
        logger.info(f"Fetching website data for startup: {startup_name}...")
        website_scraping_main(startup_name)
        logger.info(f"Website data fetched for startup: {startup_name}.")
    except Exception as e:
        logger.error(f"Failed to fetch website data for startup {startup_name}: {e}")
    
    # Placeholder for fetching data from AngelList
    # logger.info("Fetching AngelList data...")
    # fetch_angellist_data(startup_name)

    # Placeholder for fetching data from Crunchbase
    # logger.info("Fetching Crunchbase data...")
    # fetch_crunchbase_data(startup_name)

    # Placeholder for fetching data from LinkedIn
    # logger.info("Fetching LinkedIn data...")
    # fetch_linkedin_data(startup_name)

    logger.info(f"Data fetch completed for {startup_name}.")
    # You can return the gathered data if needed for further processing
    return None  # Placeholder for actual data return

# Example usage
if __name__ == "__main__":
    startup_name = "N26"  # Replace with the desired startup name
    fetch_startup_data(startup_name)