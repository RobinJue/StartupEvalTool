import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
from datetime import datetime
from googleapiclient.discovery import build
from gsheets.google_authenticate import authenticate_google

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def copy_google_sheets_file(file_id, new_name):
    """
    Copy a Google Sheets file to your Drive with a new name.

    Args:
        file_id (str): The ID of the file to copy.
        new_name (str): The new name for the copied file.

    Returns:
        str: The URL of the new file in Google Drive.
    """
    creds = authenticate_google()
    service = build('drive', 'v3', credentials=creds)

    try:
        logger.info(f"Copying file with ID {file_id} to a new file named {new_name}...")
        # Copy the file
        file_metadata = {'name': new_name}
        copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()

        # Get the new file's URL
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

    # Define the original Google Sheets file ID
    original_file_id = "1Q0leol-d9l51WqeKbSbOHJDLf_CjhmCcdNSf9lPIEnA"  # Replace with your actual template ID

    # Generate the new file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_file_name = f"{current_date}_{startup_name}_Financial_Model"

    try:
        # Copy the file
        logger.info(f"Copying template file for startup: {startup_name}")
        copied_file_url = copy_google_sheets_file(original_file_id, new_file_name)
        if copied_file_url:
            logger.info(f"New file created successfully: {copied_file_url}")
        else:
            logger.error("Failed to create a new file.")
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}", exc_info=True)

if __name__ == "__main__":
    # Example startup name; replace this with a CLI input or hardcoded value
    startup_name = "StartupName"
    main(startup_name)