import os
import time
import requests
from googlesearch import search
from datetime import datetime
import logging
from bs4 import BeautifulSoup
import json
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from modules.data_sources.chatgpt_txt_data_extraction import process_file  # Import process_file

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the temporary directory path
TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_sources', 'temp')

# Ensure the temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

def delete_temp_files():
    """Delete all files in the temporary directory."""
    try:
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the file
                logger.info(f"Deleted: {file_path}")
    except Exception as e:
        logger.error(f"An error occurred while deleting temp files: {e}")

def google_search(query):
    """Perform a Google search and return the first result."""
    start_time = time.time()  # Track start time for timeout detection
    try:
        results = list(search(query))
        if time.time() - start_time > 45:
            raise TimeoutError("Google search took too long. Exceeded 45 seconds.")
        return results[0] if results else None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("Received 429 error. Waiting for 5 seconds before retrying...")
            time.sleep(5)
            return google_search(query)
        logger.error(f"An error occurred: {e}")
        return None
    except TimeoutError as e:
        logger.error(f"Google search timeout: {e}")
        return None

def find_financial_links(startup_url):
    """Find financial-related links for the given startup URL."""
    search_words = [
        "financial statements",
        "annual report",
        "investor relations",
        "financial analysis",
        "SEC filings"
    ]
    financial_links = set()  # Use a set to avoid duplicates
    for word in search_words:
        query = f"{startup_url} {word}"
        result = google_search(query)
        if result:
            financial_links.add(result)
    return list(financial_links)

def scrape_website(url):
    """Scrape the website and return its HTML content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while scraping the website: {e}")
        return None

def preprocess_html(html_content):
    """Pre-process the HTML content to reduce its size and remove duplicates."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        relevant_tags = ["div", "p", "table"]
        relevant_content = []
        for tag in relevant_tags:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                if text:
                    relevant_content.append(text)
        return "\n".join(dict.fromkeys("\n".join(relevant_content).splitlines()))
    except Exception as e:
        logger.error(f"An error occurred while preprocessing HTML: {e}")
        return None

def unionize_json_from_files(temp_dir, output_file):
    """Process all text files in the temp directory using ChatGPT and unionize the results into a single JSON file."""
    all_data = []  # A list to hold all extracted dictionaries
    try:
        for filename in os.listdir(temp_dir):
            if filename.endswith(".txt"):  # Process only text files
                file_path = os.path.join(temp_dir, filename)
                logger.info(f"Processing file: {file_path}")

                # Extract data from the file using ChatGPT
                json_data = process_file(file_path)
                if json_data:
                    all_data.append(json_data)  # Append the dictionary to the list
                else:
                    logger.warning(f"No valid data extracted from {file_path}")

        # Save the unionized data as a JSON array
        unionized_file_path = os.path.join(temp_dir, output_file)
        with open(unionized_file_path, "w", encoding="utf-8") as json_file:
            json.dump(all_data, json_file, indent=4)
        logger.info(f"Unionized JSON saved to {unionized_file_path}")

    except Exception as e:
        logger.error(f"An error occurred while unionizing data: {e}")

def website_scraping_main(startup_name):
    """Main function to find the startup URL, financial links, and scrape the website."""
    logger.info("Starting Web Scraping")
    delete_temp_files()
    startup_url = google_search(startup_name)
    if not startup_url:
        logger.error("No valid startup URL found.")
        return
    logger.info(f"Startup URL found: {startup_url}")
    financial_links = find_financial_links(startup_url)
    logger.info(f"Financial links found: {financial_links}")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    for index, link in enumerate(financial_links, start=1):
        html_content = scrape_website(link)
        if html_content:
            reduced_content = preprocess_html(html_content)
            if reduced_content:
                filename = f"{startup_name.lower().replace(' ', '-')}_{timestamp}_{index}.txt"
                file_path = os.path.join(TEMP_DIR, filename)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Source URL: {link}\n\n")  # Add the source URL as metadata
                    file.write(reduced_content)
                logger.info(f"Pre-processed content saved to {file_path}")
    # Unionize all data from processed files
    unionize_json_from_files(TEMP_DIR, "unionized_data.json")

# Call the main function directly with a specific startup name
if __name__ == "__main__":
    website_scraping_main("N26")