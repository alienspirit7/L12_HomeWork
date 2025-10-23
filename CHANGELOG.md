# Changelog

## [1.1.0] - 2025-10-23

### Added
- **New MCP Tool: `get_recent_emails`**
  - Retrieves the most recent emails from inbox without requiring date filters
  - Parameters: `max_results` (optional, default: 10, max: 100)
  - Returns full email data including from, to, subject, date, snippet, body, and attachments

- **New Method in GmailMCPServer class**
  - `get_recent_emails(max_results=10)` method in `gmail_client.py`
  - Integrates seamlessly with existing authentication and email parsing

- **Standalone Script Enhancement**
  - Updated `get_recent_emails.py` to use the new GmailMCPServer method
  - Now supports command-line argument to specify number of emails
  - Usage: `python get_recent_emails.py [count]`

- **Test Suite**
  - Added `test_recent_emails.py` for testing the new functionality
  - Tests retrieval of 3, 5, and 10 emails

### Changed
- **README.md Updates**
  - Added documentation for the new `get_recent_emails` tool
  - Added standalone script usage examples
  - Updated example commands section
  - Renumbered tools (get_recent_emails is now Tool #1)

- **server.py Updates**
  - Added `get_recent_emails` to TOOLS list
  - Added handler for `get_recent_emails` in `handle_tool_call()`

### Benefits
- Quick access to recent emails without needing to specify date ranges
- Useful for checking latest messages, notifications, or recent correspondence
- Works perfectly with Claude Code for natural language queries like "What are my last 3 emails?"

## [1.0.0] - Initial Release

### Features
- Email extraction with date and keyword filtering
- AI-powered email summarization using Google Gemini
- Excel export with Hebrew support
- Email count statistics
- Gmail API integration
