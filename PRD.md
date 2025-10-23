# Product Requirements Document (PRD)
## Gmail MCP Server for Claude CLI

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | Gmail MCP Server |
| **Version** | 1.0 |
| **Date** | October 23, 2025 |
| **Owner** | Development Team |
| **Status** | Completed |
| **Estimated Effort** | 3 hours |
| **Actual Effort** | 3 hours |

---

## 1. Executive Summary

### 1.1 Product Overview
Gmail MCP Server is a Model Context Protocol (MCP) server that enables Claude AI assistant to interact with Gmail accounts. It provides email extraction, AI-powered summarization using Google Gemini, and Excel export capabilities with Hebrew language support.

### 1.2 Business Objectives
- Enable AI-assisted email management and analysis
- Reduce time spent manually reviewing emails
- Provide intelligent summaries of email communications
- Support Hebrew language for Israeli users
- Integrate seamlessly with Claude CLI workflow

### 1.3 Target Users
- Students and educators managing course-related emails
- Professionals who need email analysis and reporting
- Users who prefer command-line interfaces
- Hebrew-speaking users requiring RTL text support

### 1.4 Success Metrics
- Successfully extract emails with <2 second response time
- Generate AI summaries with >95% accuracy
- Export Excel files with proper Hebrew formatting
- Zero security vulnerabilities in credential handling
- Seamless integration with Claude CLI (zero configuration errors)

---

## 2. Problem Statement

### 2.1 Current Challenges
1. **Email Overload**: Users receive numerous emails daily and struggle to identify important messages
2. **Manual Filtering**: Time-consuming manual search and filtering of emails by date, sender, or keywords
3. **Lack of Summaries**: No quick way to get overview of email communications over a period
4. **Export Limitations**: Gmail's native export doesn't support structured data with custom formatting
5. **Hebrew Support**: Limited tools support Hebrew text with proper RTL formatting
6. **AI Integration Gap**: No direct way for AI assistants to access and analyze Gmail data

### 2.2 User Pain Points
- "I need to find all homework emails from last month"
- "I want a summary of what my professors sent me this semester"
- "I need to export my emails to Excel for reporting"
- "Hebrew text appears broken in exported files"
- "I want my AI assistant to help me manage emails"

---

## 3. Product Goals

### 3.1 Primary Goals
1. **Email Extraction**: Enable filtered email retrieval from Gmail with date, recipient, and keyword filters
2. **AI Summarization**: Provide intelligent email summaries in Hebrew using Gemini AI
3. **Data Export**: Generate professional Excel reports with Hebrew support
4. **MCP Integration**: Seamless integration with Claude CLI via MCP protocol
5. **Security**: Secure handling of OAuth credentials and API keys

### 3.2 Secondary Goals
1. Provide email statistics (counts, top senders, top subjects)
2. Support attachment detection
3. Offer flexible configuration options
4. Maintain comprehensive documentation
5. Enable easy setup and authentication

### 3.3 Non-Goals (Out of Scope)
- Email sending/composing capabilities
- Email deletion or modification
- Multiple Gmail account support in v1.0
- Real-time email notifications
- Web interface or GUI
- Mobile support

---

## 4. User Stories & Use Cases

### 4.1 Primary User Stories

#### Story 1: Extract Course Emails
**As a** student
**I want to** extract all emails related to my courses for a specific date range
**So that** I can review assignments and announcements in one place

**Acceptance Criteria**:
- Can filter emails by date range (start and end date)
- Can filter by recipient email address
- Can search by keywords (e.g., "homework", "assignment")
- Results include email metadata (subject, sender, date, snippet)
- Retrieves up to 100 emails per query

#### Story 2: Generate Email Summary
**As a** busy professional
**I want to** get an AI-generated summary of my emails
**So that** I can quickly understand key communications without reading every email

**Acceptance Criteria**:
- Summary generated in Hebrew language
- Includes total email count and unique senders
- Identifies top 3 senders
- Highlights key topics and themes
- Summary is concise (3-5 sentences)

#### Story 3: Export to Excel
**As a** user who needs to report on emails
**I want to** export emails to Excel with proper formatting
**So that** I can share and analyze the data in spreadsheet format

**Acceptance Criteria**:
- Excel file includes: date, sender, recipient, subject, snippet, attachments flag
- Hebrew headers displayed correctly
- RTL text alignment for Hebrew content
- Auto-adjusted column widths
- Professional formatting with bold headers

#### Story 4: Connect to Claude CLI
**As a** Claude CLI user
**I want to** use natural language commands to access my Gmail
**So that** I can manage emails within my AI assistant workflow

**Acceptance Criteria**:
- MCP server loads automatically when Claude CLI starts
- Can use natural language commands (e.g., "show me emails from last week")
- Tools are discoverable via Claude CLI
- Error messages are clear and actionable

### 4.2 Use Cases

#### Use Case 1: Weekly Email Review
1. User opens Claude CLI
2. User asks: "Extract emails from October 15-22, 2025"
3. System retrieves filtered emails from Gmail
4. User asks: "Summarize these emails"
5. System generates Hebrew summary with statistics
6. User reviews summary and key insights

#### Use Case 2: Semester Report
1. User asks: "Get all emails sent to elena.nur.study@gmail.com from September to December 2025"
2. System extracts 150 emails (processes in batches)
3. User asks: "Create an Excel file named 'semester_emails.xlsx'"
4. System generates Excel file with Hebrew headers
5. User opens Excel file for analysis and reporting

#### Use Case 3: Assignment Tracking
1. User asks: "Find emails with keywords 'assignment' or 'homework' from October 2025"
2. System searches with keyword filter
3. System returns 25 matching emails
4. User reviews subjects and dates
5. User identifies missing submissions

---

## 5. Functional Requirements

### 5.1 Email Extraction (extract_lesson_emails)

**Priority**: P0 (Must Have)

**Requirements**:
- **FR-1.1**: Support date range filtering with YYYY-MM-DD format
- **FR-1.2**: Support recipient email filtering (default: elena.nur.study@gmail.com)
- **FR-1.3**: Support keyword search with multiple keywords (OR logic)
- **FR-1.4**: Limit results with configurable max_results parameter (default: 100)
- **FR-1.5**: Return structured JSON with email metadata
- **FR-1.6**: Extract email body content (plain text)
- **FR-1.7**: Detect presence of attachments
- **FR-1.8**: Handle Gmail API errors gracefully

**Input Schema**:
```json
{
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "recipient": "elena.nur.study@gmail.com",
  "keywords": ["homework", "assignment"],
  "max_results": 100
}
```

**Output Schema**:
```json
[
  {
    "id": "email_id",
    "thread_id": "thread_id",
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email subject",
    "date": "Mon, 1 Oct 2025 10:00:00 +0000",
    "snippet": "Email preview text...",
    "body": "Full email body...",
    "labels": ["INBOX", "UNREAD"],
    "has_attachments": true
  }
]
```

### 5.2 Email Summarization (summarize_emails)

**Priority**: P0 (Must Have)

**Requirements**:
- **FR-2.1**: Integrate with Google Gemini API (gemini-1.5-flash model)
- **FR-2.2**: Generate summaries in Hebrew language
- **FR-2.3**: Include email statistics (total count, unique senders, attachments)
- **FR-2.4**: Identify top 5 senders and top 5 subjects
- **FR-2.5**: Keep summary concise (3-5 sentences)
- **FR-2.6**: Highlight key topics and patterns
- **FR-2.7**: Include timestamp of summary generation
- **FR-2.8**: Handle API failures gracefully

**Input Schema**:
```json
{
  "email_data": [/* array of email objects */],
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

**Output Schema**:
```json
{
  "period": "2025-10-01 to 2025-10-31",
  "statistics": {
    "total_emails": 50,
    "unique_senders": 10,
    "emails_with_attachments": 15,
    "top_senders": [["sender@example.com", 20]],
    "top_subjects": [["Homework Assignment", 5]]
  },
  "ai_summary": "Hebrew summary text...",
  "generated_at": "2025-10-23T16:30:00"
}
```

### 5.3 Excel Export (create_excel_file)

**Priority**: P0 (Must Have)

**Requirements**:
- **FR-3.1**: Create XLSX format files using openpyxl library
- **FR-3.2**: Include Hebrew headers: תאריך, שולח, נמען, נושא, תקציר, יש קבצים מצורפים
- **FR-3.3**: Apply RTL (right-to-left) text alignment
- **FR-3.4**: Format dates as YYYY-MM-DD HH:MM
- **FR-3.5**: Auto-adjust column widths (max 50 characters)
- **FR-3.6**: Apply bold formatting to headers
- **FR-3.7**: Support custom filename and sheet name
- **FR-3.8**: Display attachment status in Hebrew (כן/לא)

**Input Schema**:
```json
{
  "email_data": [/* array of email objects */],
  "filename": "emails.xlsx",
  "sheet_name": "Emails"
}
```

**Output**: String with created filename

### 5.4 Email Count (get_email_count)

**Priority**: P1 (Should Have)

**Requirements**:
- **FR-4.1**: Support Gmail search query syntax
- **FR-4.2**: Support date range filtering
- **FR-4.3**: Return estimated count from Gmail API
- **FR-4.4**: Handle empty results gracefully

**Input Schema**:
```json
{
  "query": "is:unread",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31"
}
```

**Output**: Integer count

### 5.5 Authentication

**Priority**: P0 (Must Have)

**Requirements**:
- **FR-5.1**: Support OAuth 2.0 flow for Gmail API
- **FR-5.2**: Request read-only scope: `gmail.readonly`
- **FR-5.3**: Store credentials in credentials.json (from Google Cloud Console)
- **FR-5.4**: Generate and store access token in token.json
- **FR-5.5**: Automatically refresh expired tokens
- **FR-5.6**: Provide standalone auth script (auth.py)
- **FR-5.7**: Open browser for user consent
- **FR-5.8**: Handle authentication errors with clear messages

### 5.6 MCP Integration

**Priority**: P0 (Must Have)

**Requirements**:
- **FR-6.1**: Implement MCP protocol (stdin/stdout JSON communication)
- **FR-6.2**: Support `tools/list` method to expose available tools
- **FR-6.3**: Support `tools/call` method to execute tool functions
- **FR-6.4**: Return responses in MCP-compliant JSON format
- **FR-6.5**: Handle errors and return error responses
- **FR-6.6**: Load automatically when Claude CLI starts
- **FR-6.7**: Support configuration via ~/.claude/mcp_config.json

---

## 6. Non-Functional Requirements

### 6.1 Performance

**NFR-1: Response Time**
- Email extraction: <2 seconds for up to 100 emails
- AI summarization: <5 seconds per summary
- Excel export: <1 second for up to 1000 rows

**NFR-2: Throughput**
- Support up to 100 email extractions per request
- Process batches efficiently without timeout

**NFR-3: API Quotas**
- Stay within Gmail API quota (1 billion units/day)
- Stay within Gemini API free tier (15 req/min, 1500 req/day)

### 6.2 Security

**NFR-4: Credential Protection**
- Never expose credentials.json in logs or responses
- Never commit sensitive files to version control
- Store API keys in gitignored files (config.json or .env)

**NFR-5: OAuth Security**
- Use OAuth 2.0 with read-only scope
- Store tokens securely in token.json (gitignored)
- Automatically refresh tokens when expired

**NFR-6: Data Privacy**
- Only request read-only access to Gmail
- Never store email content permanently
- Never transmit email data to third parties (except Gemini for summarization)

### 6.3 Reliability

**NFR-7: Error Handling**
- Gracefully handle Gmail API errors (rate limits, network issues)
- Gracefully handle Gemini API errors (quota exceeded)
- Provide clear error messages to users
- Never crash on malformed email data

**NFR-8: Availability**
- Dependent on Gmail API availability (99.9% SLA)
- Dependent on Gemini API availability
- No additional downtime from server code

### 6.4 Usability

**NFR-9: Documentation**
- Comprehensive README with setup instructions
- Clear API documentation for all tools
- Troubleshooting guide for common issues
- Code comments for maintainability

**NFR-10: Setup Time**
- Complete setup in <10 minutes (excluding OAuth consent)
- Clear step-by-step instructions
- Minimal dependencies (6 Python packages)

### 6.5 Maintainability

**NFR-11: Code Quality**
- Modular architecture (server.py, gmail_client.py, auth.py)
- Clear separation of concerns
- Consistent coding style
- Type hints where applicable

**NFR-12: Configuration**
- Centralized configuration in config.json
- Environment variable support via .env
- Configurable defaults (recipient, max_results)

### 6.6 Compatibility

**NFR-13: Platform Support**
- macOS (primary)
- Linux (secondary)
- Windows (tertiary, via WSL)

**NFR-14: Python Version**
- Python 3.8+ required
- Compatible with modern Python versions (3.11+)

**NFR-15: Claude CLI Integration**
- Compatible with Claude CLI MCP protocol
- Works with Claude Desktop as alternative

---

## 7. Technical Architecture

### 7.1 System Components

```
┌─────────────────┐
│   Claude CLI    │
│   (User Input)  │
└────────┬────────┘
         │ stdin/stdout (JSON)
         ↓
┌─────────────────┐
│   server.py     │
│  MCP Protocol   │
│   Handler       │
└────────┬────────┘
         │ Function Calls
         ↓
┌─────────────────┐
│ gmail_client.py │
│ Business Logic  │
└────┬────────┬───┘
     │        │
     ↓        ↓
┌─────────┐  ┌──────────┐
│ Gmail   │  │  Gemini  │
│  API    │  │   API    │
└─────────┘  └──────────┘
```

### 7.2 Technology Stack

**Core Languages**:
- Python 3.8+

**Libraries**:
- `google-auth-oauthlib` - OAuth 2.0 authentication
- `google-api-python-client` - Gmail API client
- `google-generativeai` - Gemini AI integration
- `openpyxl` - Excel file generation
- `python-dotenv` - Environment variable support

**APIs**:
- Gmail API v1 (read-only scope)
- Google Gemini API (gemini-1.5-flash model)

**Protocols**:
- Model Context Protocol (MCP) for Claude CLI integration

### 7.3 Data Flow

**Email Extraction Flow**:
1. Claude CLI → MCP request → server.py
2. server.py → extract_lesson_emails() → gmail_client.py
3. gmail_client.py → Gmail API search query
4. Gmail API → returns message IDs
5. gmail_client.py → fetches full message details (batch)
6. gmail_client.py → parses email structure
7. gmail_client.py → returns JSON array
8. server.py → MCP response → Claude CLI

**Summarization Flow**:
1. User provides email_data array
2. gmail_client.py → calculates statistics
3. gmail_client.py → formats prompt for Gemini
4. gmail_client.py → Gemini API request
5. Gemini API → returns Hebrew summary
6. gmail_client.py → combines stats + summary
7. Returns comprehensive summary object

### 7.4 File Structure

```
L12_HomeWork/
├── server.py              # MCP protocol handler (150 lines)
├── gmail_client.py        # Core business logic (350 lines)
├── auth.py                # OAuth authentication (50 lines)
├── requirements.txt       # Dependencies (6 packages)
├── config.json            # Configuration + API key
├── credentials.json       # Gmail OAuth credentials
├── token.json             # Generated access token (auto-created)
├── .env.example           # Environment template
├── .gitignore            # Security protection
├── README.md             # User documentation
├── PRD.md                # This document
└── PROJECT_SETUP_LOG.md  # Setup history
```

---

## 8. Configuration & Setup

### 8.1 Prerequisites

1. **Python 3.8+** installed
2. **Gmail account** with API access enabled
3. **Google Cloud Project** with Gmail API enabled
4. **Gemini API key** from Google AI Studio
5. **Claude CLI** installed

### 8.2 Setup Steps

**Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Configure Gmail API**
- Create project in Google Cloud Console
- Enable Gmail API
- Create OAuth 2.0 credentials (Desktop app)
- Download credentials.json

**Step 3: Configure Gemini API**
- Visit Google AI Studio
- Generate API key
- Add to config.json or .env

**Step 4: Authenticate Gmail**
```bash
python auth.py
```

**Step 5: Configure Claude CLI**
- Create ~/.claude/mcp_config.json
- Add server configuration with full paths
- Restart Claude CLI

### 8.3 Configuration Files

**config.json**:
```json
{
  "gemini_api_key": "your-api-key",
  "gmail_credentials_path": "credentials.json",
  "default_recipient": "elena.nur.study@gmail.com",
  "default_max_results": 100
}
```

**~/.claude/mcp_config.json**:
```json
{
  "mcpServers": {
    "gmail": {
      "command": "python",
      "args": ["/full/path/to/server.py"],
      "cwd": "/full/path/to/project"
    }
  }
}
```

---

## 9. Testing & Quality Assurance

### 9.1 Test Scenarios

**Test 1: Email Extraction**
- Extract emails with valid date range → Success
- Extract with invalid date format → Error message
- Extract with no results → Empty array
- Extract with max_results=10 → Returns ≤10 emails

**Test 2: AI Summarization**
- Summarize 50 emails → Hebrew summary generated
- Summarize with no API key → Error message
- Summarize empty array → Error message
- Verify statistics accuracy → Counts match

**Test 3: Excel Export**
- Export 100 emails → File created successfully
- Verify Hebrew headers → Displayed correctly
- Verify RTL alignment → Text aligned right
- Open in Excel → No formatting issues

**Test 4: MCP Integration**
- Start Claude CLI → Server loads automatically
- List tools → 4 tools shown
- Execute tool → Correct response
- Invalid tool call → Error response

**Test 5: Authentication**
- Run auth.py → Browser opens
- Grant permissions → token.json created
- Use expired token → Auto-refresh successful
- Invalid credentials → Clear error message

### 9.2 Quality Criteria

- ✅ Zero security vulnerabilities
- ✅ All 4 MCP tools functional
- ✅ Hebrew text displayed correctly
- ✅ Error handling for all edge cases
- ✅ Documentation complete and accurate
- ✅ Setup time <10 minutes
- ✅ Response times within SLA

---

## 10. Risks & Mitigations

### 10.1 Technical Risks

**Risk 1: Gmail API Rate Limits**
- **Impact**: High - Users cannot extract emails
- **Probability**: Low - Free tier quota is generous
- **Mitigation**: Implement exponential backoff, respect rate limits

**Risk 2: Gemini API Quota Exceeded**
- **Impact**: Medium - Summarization fails
- **Probability**: Low - 1500 req/day sufficient for personal use
- **Mitigation**: Graceful degradation, clear error message

**Risk 3: OAuth Token Expiration**
- **Impact**: Medium - User must re-authenticate
- **Probability**: Low - Auto-refresh implemented
- **Mitigation**: Automatic token refresh, clear re-auth instructions

**Risk 4: MCP Protocol Changes**
- **Impact**: High - Integration breaks
- **Probability**: Low - Protocol is stable
- **Mitigation**: Monitor Claude CLI updates, version compatibility

### 10.2 Security Risks

**Risk 5: Credential Exposure**
- **Impact**: Critical - Account compromise
- **Probability**: Low - .gitignore protection
- **Mitigation**: Multiple layers: .gitignore, documentation warnings, file permissions

**Risk 6: API Key Leakage**
- **Impact**: High - Unauthorized API usage
- **Probability**: Low - Stored in gitignored files
- **Mitigation**: Environment variables, secure storage, key rotation support

### 10.3 Usability Risks

**Risk 7: Complex Setup**
- **Impact**: Medium - Users cannot complete setup
- **Probability**: Low - Comprehensive documentation
- **Mitigation**: Step-by-step guide, troubleshooting section, video tutorial (future)

**Risk 8: Hebrew Encoding Issues**
- **Impact**: Medium - Text displays incorrectly
- **Probability**: Low - UTF-8 and RTL support implemented
- **Mitigation**: Extensive testing, explicit encoding settings

---

## 11. Future Enhancements

### Phase 2 (Future Release)

**Feature 1: Attachment Download**
- Download email attachments to local directory
- Support filtering by attachment type
- Estimated effort: 2 hours

**Feature 2: Multiple Accounts**
- Support multiple Gmail accounts
- Account switching via configuration
- Estimated effort: 3 hours

**Feature 3: Email Threading**
- Group related emails by conversation thread
- Thread statistics and analysis
- Estimated effort: 4 hours

**Feature 4: Advanced Filters**
- Label-based filtering
- Importance and star flags
- Read/unread status
- Estimated effort: 2 hours

**Feature 5: Custom Gemini Prompts**
- User-configurable summary prompts
- Multiple summary styles (brief, detailed, technical)
- Estimated effort: 1 hour

**Feature 6: Scheduled Reports**
- Automated daily/weekly email reports
- Configurable schedule via cron
- Estimated effort: 3 hours

**Feature 7: PDF Export**
- Alternative export format to Excel
- Professional PDF formatting
- Estimated effort: 2 hours

**Feature 8: Email Sending**
- Compose and send emails via MCP
- Requires write scope upgrade
- Estimated effort: 4 hours

---

## 12. Success Metrics & KPIs

### 12.1 Adoption Metrics
- Number of successful setups
- Number of active users (weekly)
- Average number of tool calls per user

### 12.2 Performance Metrics
- Average email extraction time
- Average summarization time
- API error rate (<1%)
- Token refresh success rate (>99%)

### 12.3 Quality Metrics
- Setup success rate (>90%)
- User-reported bugs (target: <5 per month)
- Documentation completeness score (100%)

### 12.4 User Satisfaction
- Setup difficulty rating (target: 4/5)
- Feature usefulness rating (target: 4.5/5)
- Would recommend to others (target: >80%)

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - Communication protocol between AI assistants and tools |
| **OAuth 2.0** | Open standard for access delegation, used for Gmail API authentication |
| **Gemini** | Google's generative AI model for text generation and analysis |
| **RTL** | Right-to-Left text direction, required for Hebrew and Arabic languages |
| **XLSX** | Excel file format (Office Open XML Workbook) |
| **Token** | Access token for Gmail API, stored in token.json after authentication |
| **Scope** | Gmail API permission level (gmail.readonly = read-only access) |
| **Snippet** | Short preview text of email content (first ~150 characters) |

---

## 14. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | - | - | 2025-10-23 |
| Tech Lead | - | - | 2025-10-23 |
| Security Review | - | - | 2025-10-23 |
| QA Lead | - | - | 2025-10-23 |

---

## 15. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-23 | Development Team | Initial PRD creation after project completion |

---

**End of Product Requirements Document**
