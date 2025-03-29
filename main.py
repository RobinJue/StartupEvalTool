import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from dotenv import load_dotenv
import logging
from datetime import datetime

# Apply global logger configuration
from utils.logger_config import configure_logger
configure_logger()

# Step 1
# Step 2
from gsheets.gsheets_create import copy_google_sheets_file
# Step 3
from modules.fetch_data import fetch_startup_data
# Step 4
from table.table_main import main as generate_table
# Step 5
from gsheets.export_results import export_data_to_gsheets
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

        if True:
            # Step 1: Load configuration from environment variables
            logger.info("Step 1: Loading configuration...")
            template_id = os.getenv("SHEET_TEMPLATE_ID")  # Ensure this variable is defined in your .env
            if not template_id:
                logger.error("SHEET_TEMPLATE_ID not found in environment variables.")
                return
            
            current_date = datetime.now().strftime("%Y-%m-%d")
            new_sheet_name = f"{current_date}_{startup_name}_Financial_Model"

        # Step 2: Copy Google Sheets template
        logger.info("Step 2: Copying Google Sheets template...")
        try:
            sheet_url = copy_google_sheets_file(template_id, new_sheet_name)
            logger.info(f"Template copied successfully. New Sheet URL: {sheet_url}")
        except Exception as e:
            logger.error(f"Failed to copy Google Sheets template: {e}")
            return

        # Step 3: Fetch data from external APIs & web search
        if True:
            
            logger.info("Step 3: Fetching startup data...")
            fetch_startup_data(startup_name)
            logger.info("Startup data fetched successfully.")

        # Step 4: Execute table_main.py directly for generating and processing the table
        logger.info("Step 4: Executing table_main.py for generating and processing the table...")
        table = generate_table()
        logger.info("Table processed successfully.")

        # Step 5: Update Google Sheets with processed data
        if True:
            logger.info("Updating Google Sheets with processed data...")
            export_data_to_gsheets(sheet_url, table)
            logger.info("Google Sheets updated successfully.")

        # Step 6: Export results to CSV
        # logger.info("Exporting results to CSV...")
        # output_file = os.path.join(output_dir, "output.csv")
        # export_to_csv(processed_data, output_file)
        # logger.info(f"Results exported successfully to {output_file}")

        logger.info(f"Main script ran successfully for startup: {startup_name}")

    except Exception as e:
        logger.error(f"An error occurred while processing {startup_name}: {e}", exc_info=True)
    logger.info("End of main.py reached.")

if __name__ == "__main__":
    # If no command-line argument is provided, default to 'N26'
    if len(sys.argv) < 2:
        logger.info("No startup name provided. Using 'N26' by default.")
        startup_name = "N26"
    else:
        # Read the startup name from command-line arguments
        startup_name = sys.argv[1]
    
    main(startup_name)