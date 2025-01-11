import logging
import os
import sys

# Ensure the module paths work whether executed directly or imported
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, ".."))

from .table_generator import start as generate_table_from_json


# File paths
json_file_path = os.path.join(current_dir, "../modules/data_sources/temp/unionized_data.json")  # Adjusted for relative path
test_json_file_path = os.path.join(current_dir, "tests/test_json_table.json")  # Adjusted for test file

# Use the test JSON file by default
json_file_path = test_json_file_path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Step 1: Generate the table from the JSON file
    logger.info("Step 1: Generating table from JSON...")
    try:
        table = generate_table_from_json(json_file_path)
        logger.info("Table generated successfully.")
        return table
    except Exception as e:
        logger.error(f"Failed to generate table: {e}")
        return

if __name__ == "__main__":
    main()