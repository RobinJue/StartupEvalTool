import sys
import os

# Add the root directory of the project to sys.path (adjusted for project structure)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'code')))

from modules.data_sources.website_scraping import website_scraping_main

def fetch_startup_data(startup_name):
    """
    Fetches data for the specified startup from various sources.
    """
    print(f"Starting data fetch for {startup_name}...")

    # Fetch data from the website using website_scraping_main function
    try:
        print(f"Fetching website data for startup: {startup_name}...")
        website_scraping_main(startup_name)
        print(f"Website data fetched for startup: {startup_name}.")
    except Exception as e:
        print(f"Failed to fetch website data for startup {startup_name}: {e}")
    
    # Placeholder for fetching data from AngelList
    # fetch_angellist_data(startup_name)

    # Placeholder for fetching data from Crunchbase
    # fetch_crunchbase_data(startup_name)

    # Placeholder for fetching data from LinkedIn
    # fetch_linkedin_data(startup_name)

    print(f"Data fetch completed for {startup_name}.")
    # You can return the gathered data if needed for further processing
    return None  # Placeholder for actual data return

# Example usage
if __name__ == "__main__":
    startup_name = "N26"  # Replace with the desired startup name
    fetch_startup_data(startup_name)