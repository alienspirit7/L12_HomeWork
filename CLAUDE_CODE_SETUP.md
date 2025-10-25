# Gmail MCP Server - Claude Code Setup Guide

Quick setup guide for using the Gmail MCP Server with **Claude Code** (VS Code extension).

## Prerequisites

Before starting, ensure you have:
- ✅ Gmail API credentials (`credentials.json` and `token.json`)
- ✅ Gemini API key (in `config.json` or as environment variable)
- ✅ Python dependencies installed (`pip install -r requirements.txt`)
- ✅ Successfully authenticated with Gmail (`python auth.py`)

## Setup Steps

### 1. Create MCP Configuration Directory

```bash
mkdir -p ~/.config/claude-code
```

### 2. Create MCP Configuration File

**macOS/Linux:**
```bash
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

**Windows (PowerShell):**
```powershell
$config = @'
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": [
        "C:\\path\\to\\your\\project\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\your\\project",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
'@
$config | Out-File -FilePath "$env:USERPROFILE\.config\claude-code\mcp.json" -Encoding utf8
```

**IMPORTANT**: Update the paths to match your actual project location!

### 3. Configure Gemini API Key

Choose one of these options:

**Option A: Environment Variable (Recommended)**
```bash
# macOS/Linux - Add to ~/.zshrc or ~/.bashrc
echo 'export GEMINI_API_KEY="your-gemini-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Windows - Add to System Environment Variables
setx GEMINI_API_KEY "your-gemini-api-key-here"
```

**Option B: Use config.json (Already Set Up)**

The project's `config.json` file already contains the Gemini API key, so no additional setup needed.

### 4. Verify Configuration

Run the test script to ensure everything is set up correctly:

```bash
cd /Users/alienspirit/Documents/25D/L12_HomeWork
python3 test_mcp_setup.py
```

**Expected Output:**
```
🔍 Gmail MCP Server Setup Verification
============================================================

✓ PASS   - Server Startup
✓ PASS   - Authentication
✓ PASS   - Email Count
✓ PASS   - Recent Emails
✓ PASS   - Gemini API
✓ PASS   - MCP Config

Results: 6/6 tests passed

✅ All tests passed! Your Gmail MCP server is ready to use.

Next step: Restart Claude Code to load the MCP server.
```

### 5. Restart Claude Code

1. **Completely quit VS Code**
   - macOS: `Cmd + Q`
   - Windows: `Alt + F4`
   - Linux: `Ctrl + Q`

2. **Reopen VS Code**

3. **Open Claude Code** in the sidebar

4. The Gmail MCP server will load automatically

### 6. Test the MCP Server

Try these commands in Claude Code:

```
How many emails did I get from Google in the last 2 weeks?
Get my 10 most recent emails
Extract all emails from October 2025
```

You should see Claude Code using tools prefixed with `mcp__gmail__`, such as:
- `mcp__gmail__get_email_count`
- `mcp__gmail__get_recent_emails`
- `mcp__gmail__extract_lesson_emails`

## Available MCP Tools

Once configured, Claude Code will have access to these Gmail tools:

### 1. **get_recent_emails**
Get the most recent emails from inbox without date filtering.

**Example:**
```
Show me my last 5 emails
Get my 3 most recent emails
```

### 2. **extract_lesson_emails**
Extract emails with advanced filtering by date, recipient, and keywords.

**Example:**
```
Extract all emails from October 2025
Show me emails from last week with keyword "homework"
```

### 3. **get_email_count**
Count emails matching specific criteria.

**Example:**
```
How many emails did I get from Google in the last week?
Count emails with attachments from last month
```

### 4. **summarize_emails**
Generate AI-powered summary using Gemini.

**Example:**
```
Summarize my emails from last month
Give me a summary of recent emails
```

### 5. **create_excel_file**
Create Excel file with Hebrew support and formatting.

**Example:**
```
Create an Excel file from these emails
Export to Excel with Hebrew headers
```

### 6. **create_csv_file**
Create CSV file and save to results folder.

**Example:**
```
Export these emails to CSV
Create a CSV file from the extracted emails
```

## Troubleshooting

### MCP Tools Not Showing Up

**Problem:** Claude Code doesn't recognize the MCP tools.

**Solutions:**
1. Verify config file exists: `cat ~/.config/claude-code/mcp.json`
2. Check file paths are correct (absolute paths)
3. Ensure you completely quit and restarted VS Code (not just reloaded window)
4. Check VS Code Output panel for error messages

### Authentication Errors

**Problem:** "Token file not found" or authentication fails.

**Solutions:**
1. Run `python auth.py` to re-authenticate
2. Ensure `token.json` exists in project root
3. Check `credentials.json` is in the correct location

### Gemini API Errors

**Problem:** Summarization features don't work.

**Solutions:**
1. Verify API key in `config.json` or environment variable
2. Check API key is valid at https://aistudio.google.com
3. Verify you haven't exceeded free tier limits (1500 requests/day)

### Python Path Issues

**Problem:** "Module not found" errors.

**Solutions:**
1. Use `python3` instead of `python` in the config (macOS/Linux)
2. Ensure PYTHONPATH in config points to project directory
3. Verify dependencies are installed: `pip install -r requirements.txt`

### Test Script Failures

**Problem:** `test_mcp_setup.py` shows failures.

**Solutions:**
1. Run each test individually to identify the issue
2. Check the specific error messages in the output
3. Verify all prerequisites are met (credentials, token, API keys)

## Configuration File Location

The MCP configuration file location varies by platform:

- **macOS/Linux**: `~/.config/claude-code/mcp.json`
- **Windows**: `%USERPROFILE%\.config\claude-code\mcp.json`

## Updating Configuration

If you move the project or change settings:

1. Edit the MCP config file:
   ```bash
   nano ~/.config/claude-code/mcp.json
   ```

2. Update the paths:
   ```json
   {
     "mcpServers": {
       "gmail": {
         "command": "python3",
         "args": [
           "/new/path/to/server.py"
         ],
         "env": {
           "PYTHONPATH": "/new/path/to/project"
         }
       }
     }
   }
   ```

3. Save and restart VS Code completely

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit** these files to version control:
   - `credentials.json` (Gmail OAuth credentials)
   - `token.json` (Gmail access token)
   - `config.json` (contains Gemini API key)
   - `.env` (environment variables)
   - `results/*.csv` (contains your email data)

2. **Already protected** by `.gitignore` in this project

3. **Use environment variables** for API keys in production

4. **Regularly rotate** your API keys

## Additional Resources

- **Gmail API Documentation**: https://developers.google.com/gmail/api
- **Gemini API Documentation**: https://ai.google.dev/docs
- **Claude Code Documentation**: https://docs.anthropic.com/claude-code
- **MCP Protocol**: https://modelcontextprotocol.io

## Support

If you encounter issues:

1. **Run the test script**: `python3 test_mcp_setup.py`
2. **Check logs**: Look at VS Code's Output panel (View → Output → Claude Code)
3. **Verify setup**: Follow each step in this guide carefully
4. **Review error messages**: They often contain helpful diagnostic information

## Quick Reference

**Config File**: `~/.config/claude-code/mcp.json`
**Test Script**: `python3 test_mcp_setup.py`
**Project Path**: `/Users/alienspirit/Documents/25D/L12_HomeWork`

**Restart VS Code**: Cmd+Q (macOS), Alt+F4 (Windows), Ctrl+Q (Linux)

---

**Last Updated**: October 25, 2025
**Version**: 1.0
