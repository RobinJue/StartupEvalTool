from table_generator import start as generate_table_from_json
#from table.data_forecast import forecast_missing_data
#from gsheets.export.export_to_gsheets import export_table_to_gsheets

# File paths
# json_file_path = "modules/data_sources/temp/unionized_data.json"  # actual JSON file from scraping data
json_file_path = "table/tests/test_json_table.json"  # test JSON file

def main():

    # Step 1: Generate the table from the JSON file
    print("Step 1: Generating table from JSON...")
    table = generate_table_from_json(json_file_path)

    # Step 2: Forecast missing data
    print("Step 2: Forecasting missing data...")
    # table_with_forecast = forecast_missing_data(table)

    # Step 3: Export the table to Google Sheets
    print("Step 3: Exporting table to Google Sheets...")
    # export_table_to_gsheets(table_with_forecast)

if __name__ == "__main__":
    main()