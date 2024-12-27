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
        json.loads(cleaned_content)  # Validate JSON
        return cleaned_content
    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"Failed to clean or validate JSON: {e}")
        return None

def extract_data_from_text(text_content):
    """Extract structured data from the text content using ChatGPT."""
    instructions = (
        "Extract the following structured data from the provided text content:\n"
        "%year%:{Revenue:, Gross Profit:, Gross Profit Margin:, Operating Income:, Operating Expenses:, Operating Margin:, Net Loss:, Net Income:, Free Cash Flow:, Customers:, Customer Growth:, Source Date:, Data Source:, Year founded:, Industry:\n"
        "year is the year of the financial data.\n"
        "Format the output in JSON as previously defined.\n"
        "Data Source is the URL you find on top. Source Date is the date from when the numbers are from.\n"
        "If no data is found, return Null values for the respective fields. If data is found, always only return numbers.\n"
        "This is important because we will use this data to preprocess in deterministic algorithms. So do not add any text except numbers or Null values. Only exception is industry, Source Date and Data Source."
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

def process_file(file_path):
    """
    Processes a single file: Extracts data and saves it back to the same file in JSON format.
    Args:
        file_path (str): Path to the file to process.
    Returns:
        dict: Extracted JSON data or None if an error occurs.
    """
    try:
        # Read the file content
        logger.info(f"Processing file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()

        # Extract raw output from ChatGPT
        raw_output = extract_data_from_text(text_content)

        # Clean the output and convert to JSON
        cleaned_json = clean_to_json(raw_output)
        if cleaned_json:
            json_data = json.loads(cleaned_json)
            logger.info("Successfully extracted and cleaned JSON data.")
            
            # Save the JSON data back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4)
            
            return json_data
        else:
            logger.error("Failed to extract valid JSON data.")
            return None

    except Exception as e:
        logger.error(f"An error occurred while processing {file_path}: {e}")
        return None