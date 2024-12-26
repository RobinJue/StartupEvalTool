print("api accessed")
import subprocess
import sys
from pathlib import Path

# Example API key (Replace this with your actual environment variable)
api_key = "your_api_key_here_1234567890"

# Function to censor API key
def censor_api_key(api_key):
    """
    Censors the API key, keeping only the last 4 characters visible.
    """
    if len(api_key) > 4:
        return "#" * (len(api_key) - 4) + api_key[-4:]
    return api_key  # In case the API key is less than or equal to 4 characters

# Censoring the API key before using it
censored_api_key = censor_api_key(api_key)
print(f"Censored API Key: {censored_api_key}")

# Path to main.py
project_root = Path(__file__).resolve().parents[1]
main_script_path = project_root / "main.py"

def process_startup(startup_name):
    """
    Function to process the startup name by invoking main.py.
    Expects the startup name as an argument.
    """
    try:
        # Run main.py as a subprocess and pass the startup name
        process = subprocess.run(
            [sys.executable, str(main_script_path), startup_name],
            capture_output=True,
            text=True,
        )

        # Handle subprocess output and errors
        if process.returncode == 0:
            print(f"Success:\n{process.stdout}")
        else:
            print(f"Error:\n{process.stderr}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


# Example of calling the function with a startup name
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python api.py <startup_name>")
        sys.exit(1)

    startup_name = sys.argv[1]
    process_startup(startup_name)