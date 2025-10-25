# Gmail MCP Server

MCP (Model Context Protocol) server for extracting and analyzing emails from Gmail with AI-powered summarization.

> **📚 Documentation Guide**: New to this project? See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) to find the right guide for your needs!

## Features

✨ **Email Extraction**: Filter emails by date, recipient, and keywords
🤖 **AI Summaries**: Intelligent summaries using Google Gemini API
📊 **Excel Export**: Professional Excel files with Hebrew support
📁 **CSV Export**: Automatic CSV file generation in results folder
📈 **Statistics**: Email counts, top senders, and patterns

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Gmail API
4. Go to "Credentials" → "Create Credentials" → "OAuth client ID"
5. Choose "Desktop app"
6. Download credentials as `credentials.json`
7. Place in project root directory

### 3. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key
4. Add to config.json or .env file:

```bash
# Option 1: Edit config.json
{
  "gemini_api_key": "your-api-key-here"
}

# Option 2: Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

### 4. Authenticate Gmail

```bash
python auth.py
```

This opens a browser window for Gmail authentication. After approval, `token.json` is created.

### 5. Run MCP Server

```bash
python server.py
```

## Usage with Claude

> **📌 Quick Setup for Claude Code Users**: See [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) for a dedicated step-by-step guide!

### Configure Claude CLI

Create or edit the MCP configuration file at `~/.claude/mcp_config.json`:

```bash
# Create the config file
cat > ~/.claude/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/Users/alienspirit/Documents/25D/L12_HomeWork/server.py"],
      "cwd": "/Users/alienspirit/Documents/25D/L12_HomeWork"
    }
  }
}
EOF
```

**Important**: Update the paths to match your actual project location!

After creating the config file:
1. Exit Claude CLI (type `exit` or press Ctrl+D)
2. Restart Claude CLI: `claude`
3. The Gmail MCP server will be automatically loaded

### Configure Claude Code (Recommended for VS Code Users)

If you're using **Claude Code** (Claude's VS Code extension), follow these steps:

#### Step 1: Create MCP Configuration

Create the MCP config file at `~/.config/claude-code/mcp.json`:

```bash
# Create the config directory
mkdir -p ~/.config/claude-code

# Create the config file
cat > ~/.config/claude-code/mcp.json << 'EOF'
{
  "mcpServers": {
    "gmail": {
      "command": "python3",
      "args": [
        "/Users/alienspirit/Documents/25D/L12_HomeWork/server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/alienspirit/Documents/25D/L12_HomeWork",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
EOF
```

**Important**: Update the paths to match your actual project location!

#### Step 2: Set Environment Variable (Optional)

If you want to use an environment variable for your Gemini API key:

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

Or keep using the `config.json` file in your project (no environment variable needed).

#### Step 3: Restart Claude Code

1. Completely quit VS Code (Cmd+Q on macOS)
2. Reopen VS Code
3. Open Claude Code

#### Step 4: Verify Setup

Run the test script to verify everything is configured correctly:

```bash
python3 test_mcp_setup.py
```

You should see all tests pass:
```
✓ PASS   - Server Startup
✓ PASS   - Authentication
✓ PASS   - Email Count
✓ PASS   - Recent Emails
✓ PASS   - Gemini API
✓ PASS   - MCP Config
```

#### Step 5: Use in Claude Code

After restarting, you can use Gmail tools directly in Claude Code:

```
How many emails did I get from Google in the last 2 weeks?
Get my 10 most recent emails
Extract all emails from October 2025
```

Claude Code will use the MCP tools automatically, and you'll see tool names prefixed with `mcp__gmail__` (like `mcp__gmail__get_email_count`).

### Configure Claude Desktop (Alternative)

If you're using Claude Desktop app instead of Claude CLI, edit the config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/full/path/to/your/project/server.py"],
      "cwd": "/full/path/to/your/project"
    }
  }
}
```

### Quick Standalone Script

To quickly get recent emails without using Claude, run:

```bash
# Get last 3 emails (default)
python get_recent_emails.py

# Get specific number of emails
python get_recent_emails.py 5
python get_recent_emails.py 10
```

### Example Commands

**Get recent emails (auto-saves to CSV):**
```
Show me my last 3 emails
What are my 5 most recent emails?
```

**Extract lesson emails (auto-saves to CSV):**
```
Show me all lesson emails from October 2025
Extract emails from last week with keyword "assignment"
```

**Get summary:**
```
Summarize my emails from last month
```

**Create Excel report:**
```
Extract homework emails and create an Excel file
```

**Create CSV file:**
```
Create a CSV file from extracted emails
Export emails to CSV format
```

## Available Tools

### 1. get_recent_emails

Get the most recent emails from your inbox without date filtering. **Automatically saves results to CSV file in results/ folder.**

**Parameters:**
- `max_results` (optional): Number of recent emails to retrieve (default: 10, max: 100)

**Output:**
- JSON response with email data
- CSV file: `results/recent_emails_YYYYMMDD_HHMMSS.csv`

**Example:**
```
Show me my last 5 emails
Get my 3 most recent emails
```

### 2. extract_lesson_emails

Extract emails with advanced filtering. **Automatically saves results to CSV file in results/ folder.**

**Parameters:**
- `start_date` (required): YYYY-MM-DD
- `end_date` (required): YYYY-MM-DD
- `recipient` (optional): Email address (default: elena.nur.study@gmail.com)
- `keywords` (optional): Array of keywords
- `max_results` (optional): Max emails to return (default: 100)

**Output:**
- JSON response with email data
- CSV file: `results/lesson_emails_YYYYMMDD_HHMMSS.csv`

### 3. summarize_emails

Generate AI-powered summary using Gemini.

**Parameters:**
- `email_data` (required): Array of email objects
- `start_date` (optional): Period start
- `end_date` (optional): Period end

### 4. create_excel_file

Create Excel file with Hebrew support.

**Parameters:**
- `email_data` (required): Array of email objects
- `filename` (optional): Output filename
- `sheet_name` (optional): Excel sheet name

### 4.5. create_csv_file

Create CSV file and save to results folder with timestamp.

**Parameters:**
- `email_data` (required): Array of email objects
- `filename` (optional): Output filename (default: emails.csv)

**Output:**
- CSV file saved to: `results/[filename]_YYYYMMDD_HHMMSS.csv`
- Includes: Date, From, To, Subject, Snippet, Has Attachments, Labels

**Example:**
```
Create a CSV file from these emails
Export the extracted emails to CSV
```

### 5. get_email_count

Count emails matching criteria.

**Parameters:**
- `query` (optional): Gmail search query
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD

## Gmail Search Syntax

- `from:sender@email.com` - From specific sender
- `to:recipient@email.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `has:attachment` - Has attachments
- `after:2025/10/01` - After date
- `before:2025/10/31` - Before date
- `is:unread` - Unread emails
- `is:important` - Important emails

## Troubleshooting

**Authentication Error:**
- Delete `token.json` and run `python auth.py` again
- Ensure `credentials.json` is in project root

**Gemini API Error:**
- Verify API key in config.json or .env
- Check free tier limits at [AI Studio](https://aistudio.google.com)

**No Emails Found:**
- Check date format (YYYY-MM-DD)
- Verify recipient email address
- Test with broader date range

## CSV Export Details

All email extraction operations automatically save results to CSV files in the `results/` folder:

- **Automatic timestamping**: Files include timestamp to prevent overwrites
- **Location**: All CSV files saved to `results/` folder
- **Format**: Standard CSV with UTF-8 encoding
- **Columns**: Date, From, To, Subject, Snippet, Has Attachments, Labels

**Example files:**
- `results/recent_emails_20251025_143022.csv`
- `results/lesson_emails_20251025_143045.csv`
- `results/emails_20251025_143100.csv`

## Security Notes

⚠️ **Never commit these files to Git:**
- `credentials.json`
- `token.json`
- `config.json`
- `.env`
- `results/*.csv` (contains your email data)

Already added to `.gitignore`

## Cost Information

**Gmail API**: Free (no cost)
**Gemini API**: Free tier includes:
- 15 requests per minute
- 1500 requests per day
- Perfect for personal use

## Support

For issues or questions:
1. Check Gmail API logs
2. Verify Gemini API quota
3. Review error messages in console

## License

MIT License - feel free to modify and use!
