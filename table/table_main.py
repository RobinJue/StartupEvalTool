from table.table_generator import generate_table_from_json
from table.data_forecast import forecast_missing_data
#from gsheets.export.export_to_gsheets import export_table_to_gsheets

def main():
    # Step 1: Generate the table from the JSON file
    # Use table_generator to synthesize the table from the unionized JSON data.
    # The table should be structured and ready for processing.
    print("Step 1: Generating table from JSON...")
    # table = generate_table_from_json()

    # Step 2: Forecast missing data
    # Use data_forecast to fill in or forecast the missing data points in the table.
    # The table should now have additional data points based on forecasts.
    print("Step 2: Forecasting missing data...")
    # table_with_forecast = forecast_missing_data(table)

    # Step 3: Export the table to Google Sheets
    # Use the export functionality to upload the processed table to Google Sheets.
    print("Step 3: Exporting table to Google Sheets...")
    # export_table_to_gsheets(table_with_forecast)

if __name__ == "__main__":
    main()