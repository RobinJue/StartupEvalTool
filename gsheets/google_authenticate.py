import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pickle
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the required API scopes
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

def authenticate_google():
    """Authenticate with Google APIs and return the credentials."""
    creds = None
    try:
        # Check if token.pickle exists
        if os.path.exists('token.pickle'):
            logger.info("Loading credentials from token.pickle...")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, prompt user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                logger.info("Starting new authentication flow...")
                credentials_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "config", "credentials.json")
                )
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the new credentials for reuse
            logger.info("Saving new credentials to token.pickle...")
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        logger.info("Authentication successful.")
    except Exception as e:
        logger.error(f"An error occurred during authentication: {e}", exc_info=True)
        raise

    return creds