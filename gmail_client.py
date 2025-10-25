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
import csv


class GmailMCPServer:
    def __init__(self):
        self.gmail_service = None
        self.gemini_model = None
        self._setup_gemini()
        self._ensure_results_folder()

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

    def _ensure_results_folder(self):
        """Create results folder if it doesn't exist"""
        if not os.path.exists('results'):
            os.makedirs('results')

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = Credentials.from_authorized_user_file('token.json')
        self.gmail_service = build('gmail', 'v1', credentials=creds)

    def get_recent_emails(self, max_results=10):
        """
        Get the most recent emails from inbox (without date filtering)

        Args:
            max_results: Number of recent emails to retrieve (default: 10)

        Returns:
            List of email data dictionaries
        """
        results = self.gmail_service.users().messages().list(
            userId='me',
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

    def create_csv_file(self, email_data, filename='emails.csv'):
        """
        Create CSV file with email data

        Args:
            email_data: List of email dictionaries
            filename: Output filename (default: emails.csv)

        Returns:
            Full path to the created CSV file
        """
        # Ensure results folder exists
        self._ensure_results_folder()

        # Add timestamp to filename if not specified with full path
        if not filename.startswith('results/'):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            filename = f'results/{base_name}_{timestamp}.csv'

        # Write CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date', 'From', 'To', 'Subject', 'Snippet', 'Has Attachments', 'Labels']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write data rows
            for email in email_data:
                # Format date
                date_str = email.get('date', '')
                try:
                    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = date_str

                # Format labels
                labels = ', '.join(email.get('labels', []))

                # Write row
                writer.writerow({
                    'Date': formatted_date,
                    'From': email.get('from', ''),
                    'To': email.get('to', ''),
                    'Subject': email.get('subject', ''),
                    'Snippet': email.get('snippet', ''),
                    'Has Attachments': 'Yes' if email.get('has_attachments') else 'No',
                    'Labels': labels
                })

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
