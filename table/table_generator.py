import pandas as pd
from datetime import datetime

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

def populate_years(table, start_year=2018):
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
    # Generate the empty table
    table = generate_table_outline()
    
    # Populate the table with years
    table = populate_years(table)
    
    # Display the table in the terminal
    print("Generated Table with Years:")
    print(table.to_markdown(index=False))