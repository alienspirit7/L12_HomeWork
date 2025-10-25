# Changelog

## [1.2.0] - 2025-10-25

### Added
- **CSV Export Feature**
  - New `create_csv_file` MCP tool for manual CSV file creation
  - Automatic CSV export for all email extraction operations
  - CSV files automatically saved to `results/` folder with timestamps
  - Timestamp format: `YYYYMMDD_HHMMSS` prevents file overwrites

- **New Method in GmailMCPServer class**
  - `create_csv_file(email_data, filename='emails.csv')` method in `gmail_client.py`
  - Automatic results folder creation
  - UTF-8 encoding support for international characters

- **Results Folder Structure**
  - Created `results/` folder for CSV exports
  - Added `results/README.md` with folder documentation
  - Updated `.gitignore` to exclude CSV files while keeping folder structure

- **Automatic CSV Export Integration**
  - `extract_lesson_emails` automatically saves to `results/lesson_emails_YYYYMMDD_HHMMSS.csv`
  - `get_recent_emails` automatically saves to `results/recent_emails_YYYYMMDD_HHMMSS.csv`
  - Response messages include CSV file paths

### Changed
- **README.md Updates**
  - Added "CSV Export" feature to features list
  - Added CSV Export Details section
  - Updated tool documentation with CSV auto-save information
  - Added CSV files to security notes

- **PRD.md Updates**
  - Version updated to 1.2
  - Added CSV Export functional requirements (section 5.5)
  - Updated product overview with CSV export capability
  - Updated file structure diagram
  - Added document history entry

- **tasks.json Updates**
  - Version updated to 1.2
  - Added Phase 10: CSV Export Feature
  - Added 5 new tasks (TASK-025 through TASK-029)
  - Updated project summary (29 total tasks)

- **server.py Updates**
  - Added `create_csv_file` tool to TOOLS list
  - Modified `extract_lesson_emails` handler to auto-save CSV
  - Modified `get_recent_emails` handler to auto-save CSV
  - Enhanced response messages with file paths

- **gmail_client.py Updates**
  - Added `csv` module import
  - Added `_ensure_results_folder()` method
  - Added `create_csv_file()` method with 50 lines
  - CSV includes columns: Date, From, To, Subject, Snippet, Has Attachments, Labels

### Benefits
- Automatic data archival for all email extractions
- Easy data analysis with CSV format
- No file overwrites with automatic timestamping
- Organized storage in dedicated results folder
- UTF-8 encoding supports international characters

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
