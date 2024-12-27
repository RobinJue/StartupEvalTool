import os
import time
import requests
from googlesearch import search
from datetime import datetime
import logging
from bs4 import BeautifulSoup

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
        
        # Check if the search exceeded the time limit (45 seconds)
        if time.time() - start_time > 45:
            raise TimeoutError("Google search took too long. Exceeded 45 seconds.")
        
        return results[0] if results else None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("Received 429 error. Waiting for 5 seconds before retrying...")
            time.sleep(5)  # Retry after waiting
            return google_search(query)  # Retry the search
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
            financial_links.add(result)  # Add to set to avoid duplicates
    
    return list(financial_links)  # Convert back to list for further processing

def scrape_website(url):
    """Scrape the website and return its HTML content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text  # Return the HTML content
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while scraping the website: {e}")
        return None

def remove_consecutive_duplicates(text):
    """Remove consecutive duplicate lines from text."""
    lines = text.splitlines()
    filtered_lines = [lines[0]] if lines else []
    
    for line in lines[1:]:
        if line != filtered_lines[-1]:
            filtered_lines.append(line)
    
    return "\n".join(filtered_lines)

def preprocess_html(html_content):
    """Pre-process the HTML content to reduce its size and remove duplicates."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove scripts and styles
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Extract text from relevant tags
        relevant_tags = ["div", "p", "table"]
        relevant_content = []

        for tag in relevant_tags:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                if text:  # Include only non-empty content
                    relevant_content.append(text)

        # Join extracted text into a single string
        reduced_content = "\n".join(relevant_content)

        # Remove consecutive duplicate lines
        return remove_consecutive_duplicates(reduced_content)

    except Exception as e:
        logger.error(f"An error occurred while preprocessing HTML: {e}")
        return None

def save_html_to_file(html_content, filename):
    """Save the HTML content to a file in the temp directory."""
    file_path = os.path.join(TEMP_DIR, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logger.info(f"HTML content saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save HTML content to file: {e}")

def website_scraping_main(startup_name):
    """Main function to find the startup URL, financial links, and scrape the website."""
    logger.info("Starting Web Scraping")
    
    # Delete all files in the temp directory before starting
    delete_temp_files()
    
    # 1. Search for Startup website
    startup_url = google_search(startup_name)
    if not startup_url:
        logger.error("No valid startup URL found.")
        return
    
    logger.info(f"Startup URL found: {startup_url}")
    
    # 2. Find financial links
    financial_links = find_financial_links(startup_url)
    logger.info(f"Financial links found: {financial_links}")
    
    # 3. Generate a timestamp for this session to be used in all files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 4. Scrape each financial link and save to a file
    for index, link in enumerate(financial_links, start=1):
        html_content = scrape_website(link)
        if html_content:
            # Pre-process the HTML to reduce token size
            reduced_content = preprocess_html(html_content)
            if reduced_content:
                # Use the same timestamp for all files
                filename = f"{startup_name.lower().replace(' ', '-')}_{timestamp}_{index}.txt"
                save_html_to_file(reduced_content, filename)
                logger.info(f"Pre-processed content saved to {filename}")
            else:
                logger.warning(f"Pre-processing failed for link: {link}")

        else:
            logger.error(f"Failed to scrape the website: {link}")

# Call the main function directly with a specific startup name
if __name__ == "__main__":
    website_scraping_main("N26")  # Example startup name