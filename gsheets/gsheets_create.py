import os
import pickle
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the required API scopes
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

def authenticate_google():
    """Authenticate with Google APIs and return the credentials."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "config", "credentials.json")
            )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def copy_google_sheets_file(file_id, new_name):
    """
    Copy a Google Sheets file to your Drive with a new name.

    Args:
        file_id (str): The ID of the file to copy.
        new_name (str): The new name for the copied file.

    Returns:
        str: The URL of the new file in Google Drive.
    """
    creds = authenticate_google()
    service = build('drive', 'v3', credentials=creds)

    try:
        # Copy the file
        file_metadata = {'name': new_name}
        copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()

        # Get the new file's URL
        new_file_id = copied_file['id']
        new_file_url = f"https://docs.google.com/spreadsheets/d/{new_file_id}"
        print(f"File copied successfully. New file URL: {new_file_url}")

        return new_file_url
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")
        return None

def main(startup_name):
    """Main function to copy the Google Sheets file for the given startup."""
    # Define the original Google Sheets file ID
    original_file_id = "1Q0leol-d9l51WqeKbSbOHJDLf_CjhmCcdNSf9lPIEnA"  # Replace with your actual template ID

    # Generate the new file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_file_name = f"{current_date}_{startup_name}_Financial_Model"

    # Copy the file
    copied_file_url = copy_google_sheets_file(original_file_id, new_file_name)
    if copied_file_url:
        print(f"New file created: {copied_file_url}")
    else:
        print("Failed to create a new file.")

if __name__ == "__main__":
    # Example startup name; replace this with a CLI input or hardcoded value
    startup_name = "StartupName"
    main(startup_name)