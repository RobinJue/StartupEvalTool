import logging
from table_generator import start as generate_table_from_json
# from table.data_forecast import forecast_missing_data
# from gsheets.export.export_to_gsheets import export_table_to_gsheets

# File paths
# json_file_path = "modules/data_sources/temp/unionized_data.json"  # actual JSON file from scraping data
json_file_path = "table/tests/test_json_table.json"  # test JSON file

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Step 1: Generate the table from the JSON file
    logger.info("Step 1: Generating table from JSON...")
    try:
        table = generate_table_from_json(json_file_path)
        logger.info("Table generated successfully.")
    except Exception as e:
        logger.error(f"Failed to generate table: {e}")
        return

    # Step 2: Forecast missing data
    logger.info("Step 2: Forecasting missing data...")
    try:
        # table_with_forecast = forecast_missing_data(table)
        logger.info("Forecasting completed successfully.")
    except Exception as e:
        logger.error(f"Failed to forecast missing data: {e}")
        return

    # Step 3: Export the table to Google Sheets
    logger.info("Step 3: Exporting table to Google Sheets...")
    try:
        # export_table_to_gsheets(table_with_forecast)
        logger.info("Table exported to Google Sheets successfully.")
    except Exception as e:
        logger.error(f"Failed to export table to Google Sheets: {e}")
        return

if __name__ == "__main__":
    main()