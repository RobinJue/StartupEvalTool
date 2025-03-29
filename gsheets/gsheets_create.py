import os
import sys
import json
import logging
from datetime import datetime
from googleapiclient.discovery import build
from gsheets.google_authenticate import authenticate_google

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "credentials.json"))

def load_google_sheets_id():
    """
    Load the Google Sheets file ID from the credentials.json file.
    
    Returns:
        str: The Google Sheets file ID.
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)
            file_id = config.get("spreadsheet_id", None)  # Expecting "spreadsheet_id" to be added in credentials.json
            if not file_id:
                raise ValueError("Missing 'spreadsheet_id' in credentials.json")
            logger.info(f"Loaded Google Sheets file ID: {file_id}")
            return file_id
    except Exception as e:
        logger.error(f"Error loading Google Sheets ID: {e}")
        raise

def copy_google_sheets_file(new_name):
    """
    Copy a Google Sheets file to your Drive with a new name.

    Args:
        new_name (str): The new name for the copied file.

    Returns:
        str: The URL of the new file in Google Drive.
    """
    creds = authenticate_google()
    service = build('drive', 'v3', credentials=creds)

    try:
        file_id = load_google_sheets_id()  # Load dynamically

        logger.info(f"Copying file with ID {file_id} to a new file named {new_name}...")
        file_metadata = {'name': new_name}
        copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()

        new_file_id = copied_file['id']
        new_file_url = f"https://docs.google.com/spreadsheets/d/{new_file_id}"
        logger.info(f"File copied successfully. New file URL: {new_file_url}")

        return new_file_url
    except Exception as e:
        logger.error(f"An error occurred while copying the file: {e}", exc_info=True)
        return None

def main(startup_name):
    """Main function to copy the Google Sheets file for the given startup."""
    logger.info("Starting Google Sheets file copy process...")

    current_date = datetime.now().strftime("%Y-%m-%d")
    new_file_name = f"{current_date}_{startup_name}_Financial_Model"

    try:
        copied_file_url = copy_google_sheets_file(new_file_name)
        if copied_file_url:
            logger.info(f"New file created successfully: {copied_file_url}")
        else:
            logger.error("Failed to create a new file.")
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}", exc_info=True)

if __name__ == "__main__":
    startup_name = "StartupName"
    main(startup_name)
