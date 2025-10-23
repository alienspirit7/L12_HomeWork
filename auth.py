"""
Gmail Authentication Module
Handles OAuth 2.0 authentication for Gmail API
"""

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """
    Authenticate with Gmail API using OAuth 2.0
    Returns credentials object
    """
    creds = None

    # Check if token.json exists (contains user's access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


if __name__ == '__main__':
    """Run authentication flow"""
    print("Starting Gmail authentication...")
    creds = authenticate_gmail()
    print("✓ Authentication successful!")
    print("Token saved to token.json")
