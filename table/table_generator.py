import pandas as pd
from datetime import datetime
import json
import os

# File paths
# json_file_path = "modules/data_sources/temp/unionized_data.json"  # actual JSON file from scraping data
json_file_path = "table/tests/test_json_table.json"  # test JSON file

def load_json_data(json_file_path):
    """
    Loads JSON data from a file and returns it as a dictionary.
    
    Args:
        json_file_path (str): Path to the JSON file.
        
    Returns:
        list: The loaded JSON data as a list of dictionaries.
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        raise ValueError(f"Error loading JSON data: {e}")

def find_founding_year(data):
    """
    Finds the most common founding year from the JSON data.
    If there is a tie for the most common founding year, the earliest year is used.
    
    Args:
        data (list): The JSON data as a list of dictionaries.
        
    Returns:
        int: The founding year of the company.
    """
    try:
        # Extract all founding years from the JSON data
        founding_years = []
        for record in data:
            for year_data in record.values():
                if year_data.get("Year founded"):
                    founding_years.append(year_data["Year founded"])
        
        if not founding_years:
            raise ValueError("No founding year found in the JSON data.")
        
        # Count the frequency of each founding year
        year_counts = {}
        for year in founding_years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        # Find the most common founding year(s)
        max_count = max(year_counts.values())
        common_years = [year for year, count in year_counts.items() if count == max_count]
        
        # If there's a tie, return the earliest year
        return min(common_years)
    except Exception as e:
        raise ValueError(f"Error finding founding year: {e}")

def generate_table_outline():
    """
    Generate an empty table with predefined features/columns.
    
    Returns:
        pd.DataFrame: A pandas DataFrame representing the empty table.
    """
    columns = [
        "Yr",              # Year
        "Rev",             # Revenue
        "GP",              # Gross Profit
        "GP Marg",         # Gross Profit Margin
        "Op Inc",          # Operating Income
        "Op Exp",          # Operating Expenses
        "Op Marg",         # Operating Margin
        "Net Loss",        # Net Loss
        "Net Inc",         # Net Income
        "FCF",             # Free Cash Flow
        "Cust",            # Customers
        "Cust Gr",         # Customer Growth
        "Src Dt",          # Source Date
        "Src"              # Data Source
    ]
    
    # Create an empty DataFrame with the specified columns
    empty_table = pd.DataFrame(columns=columns)
    
    return empty_table

def populate_years(table, start_year):
    """
    Populate the table with rows for each year from the start_year to the current year.
    
    Args:
        table (pd.DataFrame): The DataFrame to populate.
        start_year (int): The year to start populating from.
        
    Returns:
        pd.DataFrame: The DataFrame with populated years.
    """
    current_year = datetime.now().year
    years = list(range(start_year, current_year + 1))  # Generate a list of years
    
    # Create a DataFrame with these years
    year_data = pd.DataFrame({"Yr": years})
    
    # Merge the years with the table
    populated_table = pd.concat([year_data, table], axis=1)
    
    return populated_table

if __name__ == "__main__":
    # Load the JSON data
    try:
        json_data = load_json_data(json_file_path)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    # Find the founding year using the loaded data
    try:
        founding_year = find_founding_year(json_data)
        print(f"Founding Year: {founding_year}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    
    # Generate the empty table
    table = generate_table_outline()
    
    # Populate the table with years starting from the founding year
    table = populate_years(table, founding_year)
    
    # Display the table in the terminal
    print("Generated Table with Years:")
    print(table.to_markdown(index=False))