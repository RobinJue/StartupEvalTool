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

def export_data_to_gsheets(sheet_url, data_frame):
    """
    Export a Pandas DataFrame to a specific Google Sheets tab and cell.

    Args:
        sheet_url (str): The URL of the Google Sheets file.
        data_frame (pd.DataFrame): The Pandas DataFrame to export.
    """
    logger.info("Starting export process...")

    # Extract the Google Sheets ID from the URL
    try:
        sheet_id = sheet_url.split('/')[5]
        logger.info(f"Extracted Sheet ID: {sheet_id}")
    except IndexError:
        logger.error("Invalid Google Sheets URL.")
        return

    # Define the tab name and starting cell
    tab_name = "Income_Statements"
    start_cell = "B3"  # Start in B3 instead of B2

    creds = authenticate_google()
    service = build('sheets', 'v4', credentials=creds)

    try:
        # Sanitize the DataFrame
        sanitized_data_frame = data_frame.fillna('')  # Replace NaN with an empty string

        # Format specific columns as percentages
        if 'GP Marg' in sanitized_data_frame.columns:
            sanitized_data_frame['GP Marg'] = sanitized_data_frame['GP Marg'].apply(
                lambda x: f"{x}%" if x != '' else x)
        if 'Op Marg' in sanitized_data_frame.columns:
            sanitized_data_frame['Op Marg'] = sanitized_data_frame['Op Marg'].apply(
                lambda x: f"{x}%" if x != '' else x)
        if 'Cust Gr' in sanitized_data_frame.columns:
            sanitized_data_frame['Cust Gr'] = sanitized_data_frame['Cust Gr'].apply(
                lambda x: f"{x}%" if x != '' else x)

        # Convert DataFrame to a list of lists excluding the header row
        data = sanitized_data_frame.values.tolist()
        logger.info(f"Prepared data for export. Rows to upload: {len(data)}")

        # Define the range in the target Google Sheets
        range_name = f"{tab_name}!{start_cell}"

        # Prepare the body for the API request
        body = {'values': data}

        logger.info(f"Exporting data to Google Sheet ID {sheet_id}, tab {tab_name}, starting at {start_cell}...")
        # Make the API call to update the sheet
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        logger.info("Data export successful.")
    except Exception as e:
        logger.error(f"An error occurred while exporting data to Google Sheets: {e}", exc_info=True)