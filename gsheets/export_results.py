import os
import sys
import logging
from googleapiclient.discovery import build

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the root directory of the project to sys.path (adjusted for project structure)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'code')))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from utils.logger_config import configure_logger
from gsheets.gsheets_create import authenticate_google

# Apply global logger configuration
configure_logger()

# Setup logging
import logging
logger = logging.getLogger(__name__)

def export_to_gsheets(sheet_id, table_data, sheet_name="Income Statements", start_cell="B3"):
    """
    Exports data to the specified Google Sheet tab and starting cell.
    
    Args:
        sheet_id (str): The ID of the target Google Sheet.
        table_data (list of lists): Data to be inserted (each sub-list represents a row).
        sheet_name (str): The name of the tab in the Google Sheet.
        start_cell (str): The starting cell (default: "B3").
    """
    try:
        # Authenticate with Google Sheets API
        creds = authenticate_google()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Locate the tab (sheet_name)
        range_name = f"{sheet_name}!{start_cell}"

        # Prepare the data for Google Sheets
        body = {
            "range": range_name,
            "values": table_data
        }

        # Use the `update` method to write the data
        result = sheet.values().update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        logger.info(f"Successfully updated sheet: {result.get('updatedRange')}")
    except Exception as e:
        logger.error(f"Failed to export data to Google Sheets: {e}", exc_info=True)

if __name__ == "__main__":
    print("Execute from main!")