#!/usr/bin/env python3
"""
Simple script to retrieve recent emails from Gmail using the MCP server client
"""

from gmail_client import GmailMCPServer


def get_last_emails(count=3):
    """Retrieve the last N emails from Gmail"""
    # Initialize and authenticate
    server = GmailMCPServer()
    server.authenticate()

    # Get recent emails
    emails = server.get_recent_emails(max_results=count)

    if not emails:
        print("No messages found.")
        return

    print(f"Last {len(emails)} emails:\n")
    print("=" * 80)

    for i, email in enumerate(emails, 1):
        # Format and print
        print(f"\nEmail #{i}")
        print("-" * 80)
        print(f"From: {email.get('from', 'Unknown')}")
        print(f"To: {email.get('to', 'Unknown')}")
        print(f"Subject: {email.get('subject', 'No Subject')}")
        print(f"Date: {email.get('date', 'Unknown')}")
        print(f"\nSnippet: {email.get('snippet', '')}")
        print(f"\nBody (first 500 chars):")
        body = email.get('body', '')
        print(body[:500] if body else "(No text content)")
        print("=" * 80)


if __name__ == '__main__':
    import sys

    # Allow user to specify count via command line
    count = 3
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid count: {sys.argv[1]}, using default (3)")

    get_last_emails(count)
