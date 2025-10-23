# Gmail MCP Server - Complete Setup Instructions for Claude CLI

**IMPORTANT:** Give this entire file to Claude CLI to automatically create all the necessary files for your Gmail MCP Server project.

---

## Project Overview

This project creates an MCP (Model Context Protocol) server that:
- Extracts emails from Gmail (default: elena.nur.study@gmail.com)
- Filters by date range and keywords
- Uses Gemini AI to generate intelligent summaries
- Exports data to Excel with Hebrew support
- Integrates with Claude AI assistant

---

## Instructions for Claude CLI

**Copy and paste this into Claude CLI:**

```
Please create a Gmail MCP Server project with the following structure and files. Create each file with the exact content specified below:

PROJECT STRUCTURE:
gmail-mcp-server/
├── server.py                 # Main MCP server
├── gmail_client.py          # Gmail API wrapper
├── auth.py                  # Gmail authentication
├── requirements.txt         # Python dependencies
├── config.json              # Configuration file
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore file
└── README.md               # Documentation

---

FILE 1: server.py
---

```python
#!/usr/bin/env python3
"""
Gmail MCP Server - Main Entry Point
Provides tools for extracting and summarizing Gmail emails
"""

import sys
import json
import asyncio
from gmail_client import GmailMCPServer

# MCP Tool Definitions
TOOLS = [
    {
        "name": "extract_lesson_emails",
        "description": "Extract lesson/exercise emails from Gmail with advanced filtering",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                },
                "recipient": {
                    "type": "string",
                    "description": "Target email (default: elena.nur.study@gmail.com)"
                },
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Keywords to search for"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum results (default: 100)"
                }
            },
            "required": ["start_date", "end_date"]
        }
    },
    {
        "name": "summarize_emails",
        "description": "Generate AI-powered summary of extracted emails using Gemini",
        "input_schema": {
            "type": "object",
            "properties": {
                "email_data": {
                    "type": "array",
                    "description": "Array of email objects to summarize"
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date of the period"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date of the period"
                }
            },
            "required": ["email_data"]
        }
    },
    {
        "name": "create_excel_file",
        "description": "Create professional Excel file with Hebrew support and formatting",
        "input_schema": {
            "type": "object",
            "properties": {
                "email_data": {
                    "type": "array",
                    "description": "Extracted email data"
                },
                "filename": {
                    "type": "string",
                    "description": "Output filename"
                },
                "sheet_name": {
                    "type": "string",
                    "description": "Excel sheet name"
                }
            },
            "required": ["email_data"]
        }
    },
    {
        "name": "get_email_count",
        "description": "Get count of emails matching specific criteria",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail search query"
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format"
                }
            }
        }
    }
]


def handle_tool_call(tool_name, arguments):
    """Handle MCP tool calls"""
    server = GmailMCPServer()
    server.authenticate()
    
    if tool_name == 'extract_lesson_emails':
        result = server.extract_lesson_emails(
            start_date=arguments['start_date'],
            end_date=arguments['end_date'],
            recipient=arguments.get('recipient'),
            keywords=arguments.get('keywords'),
            max_results=arguments.get('max_results', 100)
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    elif tool_name == 'summarize_emails':
        result = server.summarize_emails_with_gemini(
            email_data=arguments['email_data'],
            start_date=arguments.get('start_date'),
            end_date=arguments.get('end_date')
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    elif tool_name == 'create_excel_file':
        filename = server.create_excel_file(
            email_data=arguments['email_data'],
            filename=arguments.get('filename', 'emails.xlsx'),
            sheet_name=arguments.get('sheet_name', 'Emails')
        )
        return f"Excel file created: {filename}"
    
    elif tool_name == 'get_email_count':
        count = server.get_email_count(
            query=arguments.get('query'),
            start_date=arguments.get('start_date'),
            end_date=arguments.get('end_date')
        )
        return f"Email count: {count}"
    
    else:
        return f"Unknown tool: {tool_name}"


async def main():
    """Main MCP server loop"""
    # Read stdin for MCP protocol messages
    for line in sys.stdin:
        try:
            request = json.loads(line)
            
            if request.get('method') == 'tools/list':
                # Return available tools
                response = {
                    "tools": TOOLS
                }
                print(json.dumps(response))
                sys.stdout.flush()
            
            elif request.get('method') == 'tools/call':
                # Execute tool call
                tool_name = request['params']['name']
                arguments = request['params'].get('arguments', {})
                
                result = handle_tool_call(tool_name, arguments)
                
                response = {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
                print(json.dumps(response))
                sys.stdout.flush()
        
        except Exception as e:
            error_response = {
                "error": str(e)
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == '__main__':
    asyncio.run(main())
```

---

FILE 2: gmail_client.py
---

```python
"""
Gmail Client - Core functionality for Gmail MCP Server
Handles Gmail API operations, email extraction, and Gemini summarization
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime
import json
import os
import google.generativeai as genai
from collections import Counter
import base64


class GmailMCPServer:
    def __init__(self):
        self.gmail_service = None
        self.gemini_model = None
        self._setup_gemini()
        
    def _setup_gemini(self):
        """Initialize Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    api_key = config.get('gemini_api_key')
            except:
                pass
        
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            print("Warning: Gemini API key not found. Summary feature disabled.")
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = Credentials.from_authorized_user_file('token.json')
        self.gmail_service = build('gmail', 'v1', credentials=creds)
    
    def extract_lesson_emails(self, start_date, end_date, recipient=None, 
                             keywords=None, max_results=100):
        """
        Extract lesson/exercise emails with filtering
        """
        # Build Gmail query
        query_parts = []
        query_parts.append(f'after:{start_date}')
        query_parts.append(f'before:{end_date}')
        
        if recipient:
            query_parts.append(f'to:{recipient}')
        else:
            query_parts.append('to:elena.nur.study@gmail.com')
        
        if keywords:
            keyword_query = ' OR '.join(keywords)
            query_parts.append(f'({keyword_query})')
        
        query = ' '.join(query_parts)
        
        # Search Gmail
        results = self.gmail_service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        # Extract email data
        email_data = []
        for msg in messages:
            email = self.gmail_service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            email_data.append(self._parse_email(email))
        
        return email_data
    
    def _parse_email(self, email):
        """Parse email and extract metadata"""
        headers = {h['name']: h['value'] 
                   for h in email['payload']['headers']}
        
        body = self._get_email_body(email['payload'])
        
        return {
            'id': email['id'],
            'thread_id': email['threadId'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'snippet': email.get('snippet', ''),
            'body': body,
            'labels': email.get('labelIds', []),
            'has_attachments': self._has_attachments(email)
        }
    
    def _get_email_body(self, payload):
        """Extract email body from payload"""
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        
        return ''
    
    def _has_attachments(self, email):
        """Check if email has attachments"""
        if 'payload' in email and 'parts' in email['payload']:
            for part in email['payload']['parts']:
                if part.get('filename'):
                    return True
        return False
    
    def summarize_emails_with_gemini(self, email_data, start_date=None, end_date=None):
        """
        Use Gemini API to generate intelligent summary of emails
        """
        if not self.gemini_model:
            return "Gemini API not configured. Cannot generate summary."
        
        # Prepare statistics
        stats = self._calculate_email_stats(email_data)
        
        # Create prompt for Gemini
        prompt = f"""
You are analyzing email data. Generate a SHORT, concise summary (3-5 sentences maximum) in Hebrew.

Email Statistics:
- Period: {start_date} to {end_date}
- Total emails: {stats['total_emails']}
- Unique senders: {stats['unique_senders']}
- Emails with attachments: {stats['emails_with_attachments']}

Top Senders:
{self._format_top_senders(stats['top_senders'])}

Top Subjects:
{self._format_top_subjects(stats['top_subjects'])}

Email Snippets (sample):
{self._format_sample_snippets(email_data[:5])}

Generate a brief summary in Hebrew that includes:
1. Total number of emails received
2. Main senders (top 3)
3. Key topics/themes identified
4. Any notable patterns

Keep it SHORT and actionable. Use Hebrew.
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            summary = response.text
            
            # Combine stats with AI summary
            full_summary = {
                'period': f"{start_date} to {end_date}",
                'statistics': stats,
                'ai_summary': summary,
                'generated_at': datetime.now().isoformat()
            }
            
            return full_summary
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _calculate_email_stats(self, email_data):
        """Calculate basic statistics from email data"""
        if not email_data:
            return {
                'total_emails': 0,
                'unique_senders': 0,
                'emails_with_attachments': 0,
                'top_senders': [],
                'top_subjects': []
            }
        
        senders = []
        subjects = []
        attachment_count = 0
        
        for email in email_data:
            # Parse sender
            from_field = email.get('from', '')
            if '<' in from_field and '>' in from_field:
                sender_email = from_field.split('<')[1].split('>')[0]
            else:
                sender_email = from_field
            senders.append(sender_email)
            
            subjects.append(email.get('subject', 'No Subject'))
            
            if email.get('has_attachments'):
                attachment_count += 1
        
        sender_counts = Counter(senders)
        subject_counts = Counter(subjects)
        
        return {
            'total_emails': len(email_data),
            'unique_senders': len(set(senders)),
            'emails_with_attachments': attachment_count,
            'top_senders': sender_counts.most_common(5),
            'top_subjects': subject_counts.most_common(5)
        }
    
    def _format_top_senders(self, top_senders):
        """Format top senders for prompt"""
        return '\n'.join([f"- {sender}: {count} emails" for sender, count in top_senders[:5]])
    
    def _format_top_subjects(self, top_subjects):
        """Format top subjects for prompt"""
        return '\n'.join([f"- {subject}: {count} times" for subject, count in top_subjects[:5]])
    
    def _format_sample_snippets(self, emails):
        """Format sample email snippets"""
        snippets = []
        for email in emails:
            snippet = email.get('snippet', '')[:100]
            snippets.append(f"- {snippet}...")
        return '\n'.join(snippets)
    
    def create_excel_file(self, email_data, filename='emails.xlsx', 
                         sheet_name='Emails'):
        """Create Excel file with Hebrew support and formatting"""
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name
        
        # Headers in Hebrew
        headers = ['תאריך', 'שולח', 'נמען', 'נושא', 'תקציר', 'יש קבצים מצורפים']
        
        # Write headers with formatting
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, size=12)
            cell.alignment = Alignment(horizontal='right')
        
        # Write data
        for row_idx, email in enumerate(email_data, start=2):
            date_str = email.get('date', '')
            try:
                date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = date_str
            
            ws.cell(row=row_idx, column=1, value=formatted_date)
            ws.cell(row=row_idx, column=2, value=email.get('from', ''))
            ws.cell(row=row_idx, column=3, value=email.get('to', ''))
            ws.cell(row=row_idx, column=4, value=email.get('subject', ''))
            ws.cell(row=row_idx, column=5, value=email.get('snippet', ''))
            ws.cell(row=row_idx, column=6, value='כן' if email.get('has_attachments') else 'לא')
            
            for col in range(1, 7):
                ws.cell(row=row_idx, column=col).alignment = Alignment(horizontal='right')
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        wb.save(filename)
        return filename
    
    def get_email_count(self, query=None, start_date=None, end_date=None):
        """Get count of emails matching criteria"""
        query_parts = []
        
        if query:
            query_parts.append(query)
        if start_date:
            query_parts.append(f'after:{start_date}')
        if end_date:
            query_parts.append(f'before:{end_date}')
        
        final_query = ' '.join(query_parts) if query_parts else ''
        
        results = self.gmail_service.users().messages().list(
            userId='me',
            q=final_query
        ).execute()
        
        return results.get('resultSizeEstimate', 0)
```

---

FILE 3: auth.py
---

```python
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
```

---

FILE 4: requirements.txt
---

```
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.0.0
google-generativeai>=0.3.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
```

---

FILE 5: config.json
---

```json
{
  "gemini_api_key": "",
  "gmail_credentials_path": "credentials.json",
  "default_recipient": "elena.nur.study@gmail.com",
  "default_max_results": 100
}
```

---

FILE 6: .env.example
---

```
# Gemini API Key (get from https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-api-key-here

# Optional: Gmail credentials path
GMAIL_CREDENTIALS_PATH=credentials.json
```

---

FILE 7: .gitignore
---

```
# Environment variables
.env
config.json

# Gmail credentials and tokens
credentials.json
token.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Excel outputs
*.xlsx
*.xls

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

FILE 8: README.md
---

```markdown
# Gmail MCP Server

MCP (Model Context Protocol) server for extracting and analyzing emails from Gmail with AI-powered summarization.

## Features

✨ **Email Extraction**: Filter emails by date, recipient, and keywords  
🤖 **AI Summaries**: Intelligent summaries using Google Gemini API  
📊 **Excel Export**: Professional Excel files with Hebrew support  
📈 **Statistics**: Email counts, top senders, and patterns

## Quick Start

### 1. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

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

\`\`\`bash
# Option 1: Edit config.json
{
  "gemini_api_key": "your-api-key-here"
}

# Option 2: Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
\`\`\`

### 4. Authenticate Gmail

\`\`\`bash
python auth.py
\`\`\`

This opens a browser window for Gmail authentication. After approval, `token.json` is created.

### 5. Run MCP Server

\`\`\`bash
python server.py
\`\`\`

## Usage with Claude

### Configure Claude Desktop

Edit Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

\`\`\`json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/full/path/to/gmail-mcp-server/server.py"]
    }
  }
}
\`\`\`

### Example Commands

**Extract lesson emails:**
\`\`\`
Show me all lesson emails from October 2025
\`\`\`

**Get summary:**
\`\`\`
Summarize my emails from last month
\`\`\`

**Create Excel report:**
\`\`\`
Extract homework emails and create an Excel file
\`\`\`

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
\`\`\`

---

After creating all files:

1. Run: \`pip install -r requirements.txt\`
2. Get Gmail credentials from Google Cloud Console
3. Get Gemini API key from Google AI Studio
4. Run: \`python auth.py\` to authenticate
5. Configure Claude Desktop to use the server

That's it! Your Gmail MCP Server is ready to use.
```

Please create all these files in a directory called 'gmail-mcp-server' with the exact structure and content specified above.
```

---

## How to Use This File

1. **Save this file** to your computer as `GMAIL_MCP_SETUP_INSTRUCTIONS.md`

2. **Open your terminal** and navigate to where you want to create the project:
   \`\`\`bash
   cd ~/Documents  # or wherever you want
   mkdir gmail-mcp-server
   cd gmail-mcp-server
   \`\`\`

3. **Run Claude CLI** and paste the instructions:
   \`\`\`bash
   claude
   \`\`\`
   
   Then paste the entire content from the code block above (starting with "Please create a Gmail MCP Server...")

4. **Claude CLI will create all files** automatically in the correct structure

5. **Follow the setup steps** in the generated README.md

---

## What Gets Created

✅ **server.py** - Main MCP server entry point  
✅ **gmail_client.py** - Core Gmail and Gemini functionality  
✅ **auth.py** - Gmail authentication script  
✅ **requirements.txt** - Python dependencies  
✅ **config.json** - Configuration template  
✅ **.env.example** - Environment variables template  
✅ **.gitignore** - Protect sensitive files  
✅ **README.md** - Complete documentation  

---

## After Claude CLI Creates Files

### Next Steps:

1. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. **Get Gmail API credentials** from Google Cloud Console

3. **Get Gemini API key** from https://aistudio.google.com/app/apikey

4. **Add your API key:**
   \`\`\`bash
   # Edit config.json and add your Gemini API key
   {
     "gemini_api_key": "AIzaSyC..."
   }
   \`\`\`

5. **Authenticate Gmail:**
   \`\`\`bash
   python auth.py
   \`\`\`

6. **Test the server:**
   \`\`\`bash
   python server.py
   \`\`\`

That's it! 🎉
