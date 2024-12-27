import os
from dotenv import load_dotenv
# from modules.gsheets_template import copy_template, update_sheet
# from modules.fetch_data import fetch_startup_data
# from modules.process_data import clean_and_estimate
# from modules.export_results import export_to_csv
from utils.logger import get_logger

# Load environment variables
load_dotenv()
logger = get_logger("Main")

def main(startup_name):
    print("main accessed")
    if startup_name == "test":
        print("launching test")
        
    """
    Main function to process the given startup name.
    Args:
        startup_name (str): The name of the startup to process.
    """
    try:
        logger.info(f"Starting processing for startup: {startup_name}")

        # Step 1: Load configuration from environment variables
        # logger.info("Loading configuration...")
        # template_id = os.getenv("SHEET_TEMPLATE_ID")
        # output_dir = "data/"
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        # Step 2: Copy Google Sheets template
        # logger.info("Copying Google Sheets template...")
        # sheet_id = copy_template(template_id)
        # logger.info(f"Template copied. New Sheet ID: {sheet_id}")

        # Step 3: Fetch data from external APIs & web search
        # logger.info("Fetching startup data...")
        # raw_data = fetch_startup_data(startup_name)
        # logger.info("Startup data fetched successfully.")

        # Step 4: Process data (cleaning, sorting, and estimations)
        # logger.info("Processing data...")
        # processed_data = clean_and_estimate(raw_data)
        # logger.info("Data processed successfully.")

        # Step 5: Update Google Sheets with processed data
        # logger.info("Updating Google Sheets with processed data...")
        # update_sheet(sheet_id, processed_data)
        # logger.info("Google Sheets updated successfully.")

        # Step 6: Export results to CSV
        # logger.info("Exporting results to CSV...")
        # output_file = os.path.join(output_dir, "output.csv")
        # export_to_csv(processed_data, output_file)
        # logger.info(f"Results exported successfully to {output_file}")

        # logger.info("Process completed successfully!")

        logger.info(f"Main script ran successfully for startup: {startup_name}")

    except Exception as e:
        logger.error(f"An error occurred while processing {startup_name}: {e}", exc_info=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <startup_name>")
        sys.exit(1)

    # Read the startup name from command-line arguments
    startup_name = sys.argv[1]
    main(startup_name)