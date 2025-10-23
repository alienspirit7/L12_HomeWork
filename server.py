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
