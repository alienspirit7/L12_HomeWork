#!/usr/bin/env python3
"""
Test script to verify Gmail MCP Server setup
Run this after restarting Claude Code to ensure everything is configured correctly
"""

import sys
import json
import subprocess
from datetime import datetime, timedelta

def test_server_startup():
    """Test if the MCP server can start"""
    print("=" * 60)
    print("TEST 1: Server Startup")
    print("=" * 60)

    try:
        # Try importing the server module
        from gmail_client import GmailMCPServer
        print("✓ Gmail client module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import Gmail client: {e}")
        return False

def test_authentication():
    """Test Gmail authentication"""
    print("\n" + "=" * 60)
    print("TEST 2: Gmail Authentication")
    print("=" * 60)

    try:
        from gmail_client import GmailMCPServer
        server = GmailMCPServer()
        server.authenticate()
        print("✓ Gmail authentication successful")
        return True, server
    except FileNotFoundError as e:
        print(f"✗ Token file not found: {e}")
        print("  Make sure token.json exists in the project directory")
        return False, None
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False, None

def test_email_count(server):
    """Test basic email count functionality"""
    print("\n" + "=" * 60)
    print("TEST 3: Email Count (Last 7 Days)")
    print("=" * 60)

    try:
        # Calculate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        start_str = start_date.strftime('%Y/%m/%d')
        end_str = end_date.strftime('%Y/%m/%d')

        count = server.get_email_count(
            start_date=start_str,
            end_date=end_str
        )

        print(f"✓ Successfully retrieved email count")
        print(f"  Period: {start_str} to {end_str}")
        print(f"  Total emails: {count}")
        return True
    except Exception as e:
        print(f"✗ Email count test failed: {e}")
        return False

def test_recent_emails(server):
    """Test getting recent emails"""
    print("\n" + "=" * 60)
    print("TEST 4: Get Recent Emails")
    print("=" * 60)

    try:
        emails = server.get_recent_emails(max_results=5)
        print(f"✓ Successfully retrieved {len(emails)} recent emails")

        if emails:
            print("\n  Sample email:")
            email = emails[0]
            print(f"    From: {email.get('from', 'N/A')[:50]}")
            print(f"    Subject: {email.get('subject', 'N/A')[:50]}")
            print(f"    Date: {email.get('date', 'N/A')[:30]}")

        return True
    except Exception as e:
        print(f"✗ Recent emails test failed: {e}")
        return False

def test_gemini_setup(server):
    """Test Gemini API configuration"""
    print("\n" + "=" * 60)
    print("TEST 5: Gemini API Configuration")
    print("=" * 60)

    if server.gemini_model is not None:
        print("✓ Gemini API is configured and ready")
        return True
    else:
        print("⚠ Gemini API not configured")
        print("  Summarization features will not be available")
        print("  To enable: Set GEMINI_API_KEY in config.json or environment")
        return False

def test_mcp_config():
    """Test MCP configuration file"""
    print("\n" + "=" * 60)
    print("TEST 6: MCP Configuration File")
    print("=" * 60)

    import os
    config_path = os.path.expanduser("~/.config/claude-code/mcp.json")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        if 'gmail' in config.get('mcpServers', {}):
            print(f"✓ MCP config found at: {config_path}")
            print("  Gmail server is configured")

            gmail_config = config['mcpServers']['gmail']
            print(f"  Command: {gmail_config['command']}")
            print(f"  Server path: {gmail_config['args'][0]}")
            return True
        else:
            print(f"✗ Gmail server not found in MCP config")
            return False
    except FileNotFoundError:
        print(f"✗ MCP config not found at: {config_path}")
        return False
    except Exception as e:
        print(f"✗ Error reading MCP config: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🔍 Gmail MCP Server Setup Verification")
    print("=" * 60 + "\n")

    results = []

    # Test 1: Server startup
    results.append(("Server Startup", test_server_startup()))

    # Test 2: Authentication
    auth_success, server = test_authentication()
    results.append(("Authentication", auth_success))

    if not auth_success:
        print("\n❌ Cannot proceed with further tests - authentication failed")
        print_summary(results)
        return

    # Test 3: Email count
    results.append(("Email Count", test_email_count(server)))

    # Test 4: Recent emails
    results.append(("Recent Emails", test_recent_emails(server)))

    # Test 5: Gemini setup
    results.append(("Gemini API", test_gemini_setup(server)))

    # Test 6: MCP config
    results.append(("MCP Config", test_mcp_config()))

    # Print summary
    print_summary(results)

def print_summary(results):
    """Print test summary"""
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")

    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed! Your Gmail MCP server is ready to use.")
        print("\nNext step: Restart Claude Code to load the MCP server.")
    elif passed >= total - 1 and not results[-1][1]:
        print("\n⚠️  Setup is functional but Gemini API is not configured.")
        print("   You can still use all email extraction features.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
