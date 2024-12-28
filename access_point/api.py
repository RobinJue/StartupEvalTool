import subprocess
import sys
from pathlib import Path

# Path to main.py
project_root = Path(__file__).resolve().parents[1]
main_script_path = project_root / "main.py"

def process_startup(startup_name):
    """
    Function to process the startup name by invoking main.py.
    Streams the output live to the server console.
    """
    try:
        # Run main.py as a subprocess
        process = subprocess.Popen(
            [sys.executable, str(main_script_path), startup_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Stream stdout live to the console
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()

        # Stream stderr live to the console
        for line in process.stderr:
            sys.stderr.write(line)
            sys.stderr.flush()

        # Wait for the process to complete
        process.wait()

        # Check return code
        if process.returncode == 0:
            print("Main script completed successfully.")
        else:
            print(f"Main script failed with return code {process.returncode}.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)