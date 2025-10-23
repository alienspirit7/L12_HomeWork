#!/usr/bin/env python3
"""
Test script for the get_recent_emails functionality
"""

from gmail_client import GmailMCPServer
import json

def test_get_recent_emails():
    """Test the new get_recent_emails method"""
    print("Testing get_recent_emails functionality...")
    print("=" * 80)

    # Initialize and authenticate
    server = GmailMCPServer()
    server.authenticate()

    # Test 1: Get last 3 emails
    print("\nTest 1: Getting last 3 emails")
    print("-" * 80)
    emails = server.get_recent_emails(max_results=3)
    print(f"Retrieved {len(emails)} emails")

    for i, email in enumerate(emails, 1):
        print(f"\nEmail #{i}:")
        print(f"  From: {email.get('from', 'Unknown')}")
        print(f"  Subject: {email.get('subject', 'No Subject')}")
        print(f"  Date: {email.get('date', 'Unknown')}")
        print(f"  Snippet: {email.get('snippet', '')[:100]}...")

    # Test 2: Get last 5 emails
    print("\n" + "=" * 80)
    print("\nTest 2: Getting last 5 emails")
    print("-" * 80)
    emails = server.get_recent_emails(max_results=5)
    print(f"Retrieved {len(emails)} emails")

    # Test 3: Default (10 emails)
    print("\n" + "=" * 80)
    print("\nTest 3: Getting default (10) emails")
    print("-" * 80)
    emails = server.get_recent_emails()
    print(f"Retrieved {len(emails)} emails")

    print("\n" + "=" * 80)
    print("\n✓ All tests completed successfully!")

if __name__ == '__main__':
    test_get_recent_emails()
