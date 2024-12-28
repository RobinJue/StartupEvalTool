import os
import sys
from dotenv import load_dotenv
import logging
import subprocess

# Step 1
# Step 2
# Step 3
from modules.fetch_data import fetch_startup_data  # Import fetch_startup_data for step 3
# Step 4
from table.table_main import main as generate_and_process_table
# Step 5
# Step 6

# Get the current directory of the script (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to 'table_main.py' relative to the current directory
# table_main_path = os.path.join(current_dir, 'modules', 'table_main.py')  # Commented out the relative path

# Run the subprocess with the relative path
# subprocess.run(['python3', table_main_path], check=True)  # Commented out the subprocess run

# Add the root directory of the project to sys.path (adjusted for project structure)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)  # Insert at the beginning to ensure priority

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main(startup_name):
    logger.info("Main script accessed")
    
    if startup_name == "test":
        logger.info("Launching test mode")

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
        logger.info("Step 3: Fetching startup data...")
        fetch_startup_data(startup_name)
        logger.info("Startup data fetched successfully.")

        # Step 4: Execute table_main.py directly for generating and processing the table
        logger.info("Step 4: Executing table_main.py for generating and processing the table...")
        generate_and_process_table()  # Calling main() from table_main.py
        logger.info("Table processed successfully.")

        # Step 5: Update Google Sheets with processed data
        # logger.info("Updating Google Sheets with processed data...")
        # update_sheet(sheet_id, processed_data)
        # logger.info("Google Sheets updated successfully.")

        # Step 6: Export results to CSV
        # logger.info("Exporting results to CSV...")
        # output_file = os.path.join(output_dir, "output.csv")
        # export_to_csv(processed_data, output_file)
        # logger.info(f"Results exported successfully to {output_file}")

        logger.info(f"Main script ran successfully for startup: {startup_name}")

    except Exception as e:
        logger.error(f"An error occurred while processing {startup_name}: {e}", exc_info=True)

if __name__ == "__main__":
    # If no command-line argument is provided, default to 'N26'
    if len(sys.argv) < 2:
        logger.info("No startup name provided. Using 'N26' by default.")
        startup_name = "N26"
    else:
        # Read the startup name from command-line arguments
        startup_name = sys.argv[1]
    
    main(startup_name)