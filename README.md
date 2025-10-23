# Gmail MCP Server

MCP (Model Context Protocol) server for extracting and analyzing emails from Gmail with AI-powered summarization.

## Features

✨ **Email Extraction**: Filter emails by date, recipient, and keywords
🤖 **AI Summaries**: Intelligent summaries using Google Gemini API
📊 **Excel Export**: Professional Excel files with Hebrew support
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

### Example Commands

**Extract lesson emails:**
```
Show me all lesson emails from October 2025
```

**Get summary:**
```
Summarize my emails from last month
```

**Create Excel report:**
```
Extract homework emails and create an Excel file
```

## Available Tools

### 1. extract_lesson_emails

Extract emails with advanced filtering.

**Parameters:**
- `start_date` (required): YYYY-MM-DD
- `end_date` (required): YYYY-MM-DD
- `recipient` (optional): Email address (default: elena.nur.study@gmail.com)
- `keywords` (optional): Array of keywords
- `max_results` (optional): Max emails to return (default: 100)

### 2. summarize_emails

Generate AI-powered summary using Gemini.

**Parameters:**
- `email_data` (required): Array of email objects
- `start_date` (optional): Period start
- `end_date` (optional): Period end

### 3. create_excel_file

Create Excel file with Hebrew support.

**Parameters:**
- `email_data` (required): Array of email objects
- `filename` (optional): Output filename
- `sheet_name` (optional): Excel sheet name

### 4. get_email_count

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

## Security Notes

⚠️ **Never commit these files to Git:**
- `credentials.json`
- `token.json`
- `config.json`
- `.env`

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
