import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load the environment variables
env_path = "config/settings.env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=api_key, timeout=60.0)  # Set a timeout of 60 seconds for API requests

def clean_to_json(content):
    """
    Cleans the input to extract everything between the first '{' and the last '}'.
    """
    try:
        start_index = content.index("{")
        end_index = content.rindex("}") + 1
        cleaned_content = content[start_index:end_index]
        # Validate the JSON structure
        json.loads(cleaned_content)  # Raise error if not valid JSON
        return cleaned_content
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to clean or validate JSON: %s", e)
        return None

def process_file_and_extract_data(file_name):
    """
    Process the given file: Extract data, delete the file, and return the JSON.
    Args:
        file_name (str): Path to the file to process.
    Returns:
        str: Extracted JSON data or None if an error occurs.
    """
    try:
        # Read the text content from the file
        logger.info(f"Processing file: {file_name}")
        with open(file_name, "r", encoding="utf-8") as file:
            text_content = file.read()

        # Extract data using ChatGPT
        raw_output = extract_data_from_text(text_content)

        # Clean the output to JSON
        cleaned_json = clean_to_json(raw_output)
        if cleaned_json:
            logger.info("Successfully extracted and cleaned JSON data.")
        else:
            logger.error("Failed to extract valid JSON data.")

        # Delete the file after processing
        os.remove(file_name)
        logger.info(f"Deleted file: {file_name}")

        return cleaned_json

    except FileNotFoundError:
        logger.error(f"The file {file_name} does not exist. Please ensure the file is in the correct location.")
    except Exception as e:
        logger.error(f"An error occurred while processing {file_name}: {e}")
    return None

def extract_data_from_text(text_content):
    """Extract structured data from the text content using ChatGPT."""
    instructions = (
        "Extract the following structured data from the provided text content:\n"
        "- Year, Revenue, Gross Profit, Gross Profit Margin, Operating Income, Operating Expenses,\n"
        "  Operating Margin, Net Loss, Net Income, Free Cash Flow, Customers, Customer Growth.\n"
        "- Add metadata such as Year Founded and Industry.\n"
        "- Format the output in JSON as previously defined.\n"
        "If no data is found, return empty values for the respective fields."
    )
    logger.info("Sending data to OpenAI API...")
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert data extractor."},
            {"role": "user", "content": f"{instructions}\n\n{text_content}"}
        ],
        model="gpt-4o",
    )
    logger.info("Received response from OpenAI API.")
    return response.choices[0].message.content

# Example Usage
if __name__ == "__main__":
    # Hardcoded file path for testing
    text_file_path = os.path.join(
        os.path.dirname(__file__), "data_sources", "temp", "n26_20241227_091827_3.txt"
    )
    json_output = process_file_and_extract_data(text_file_path)
    if json_output:
        print("Extracted JSON Data:")
        print(json_output)