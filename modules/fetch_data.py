from modules.data_sources.angellist import fetch_angellist_data
from modules.data_sources.crunchbase import fetch_crunchbase_data
from modules.data_sources.linkedin import fetch_linkedin_data
from utils.logger import get_logger

logger = get_logger("FetchData")

def fetch_startup_data():
    """
    Fetches data from AngelList, Crunchbase, and LinkedIn APIs.
    Returns a combined list of startup data.
    """
    logger.info("Starting data fetch from all sources...")
    combined_data = []

    try:
        logger.info("Fetching data from AngelList...")
        angellist_data = fetch_angellist_data()
        combined_data.extend(angellist_data)
        logger.info(f"Retrieved {len(angellist_data)} records from AngelList.")
    except Exception as e:
        logger.error(f"Failed to fetch data from AngelList: {e}")

    try:
        logger.info("Fetching data from Crunchbase...")
        crunchbase_data = fetch_crunchbase_data()
        combined_data.extend(crunchbase_data)
        logger.info(f"Retrieved {len(crunchbase_data)} records from Crunchbase.")
    except Exception as e:
        logger.error(f"Failed to fetch data from Crunchbase: {e}")

    try:
        logger.info("Fetching data from LinkedIn...")
        linkedin_data = fetch_linkedin_data()
        combined_data.extend(linkedin_data)
        logger.info(f"Retrieved {len(linkedin_data)} records from LinkedIn.")
    except Exception as e:
        logger.error(f"Failed to fetch data from LinkedIn: {e}")

    logger.info("Data fetching completed.")
    return combined_data