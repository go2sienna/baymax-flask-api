import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class BaymaxNotion:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_ids = {
            'inbox': '14ff4a0e-0321-818e-a643-cac8a69f106f',
            'tasks': '14ff4a0e-0321-81bf-8fa8-d94e1825dc23',
            'bills': '14ff4a0e-0321-8197-8330-d5eea6cbd03f',
            'individuals': '14ff4a0e-0321-818d-ab23-f1a14a4e5cb3',
            'assistance': '14ff4a0e-0321-81d4-982b-ce2eabdba3bb',
            'documents': '14ff4a0e-0321-8196-9192-fc4f9edc2806'
        }

    def create_inbox_entry(self, content, entry_type="Brain Dump", due_date=None, priority=None):
        """Create a new entry with improved formatting"""
        try:
            properties = {
                "Inbox": {"title": [{"text": {"content": content}}]},
                "Type": {"select": {"name": entry_type}},
                "Date Logged": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}},
            }

            # Handle priority (!!!)
            if priority:
                priority_map = {
                    "high": "!!!",
                    "medium": "!!",
                    "low": "!"
                }
                properties["Priority"] = {"rich_text": [{"text": {"content": priority_map.get(priority.lower(), "!")}}]}

            # Format due date
            if due_date:
                formatted_date = self.format_date(due_date)
                if formatted_date:
                    properties["Due Date"] = {"date": {"start": formatted_date}}

            response = self.notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties=properties
            )
            return f"Added to inbox: {content}"
        except Exception as e:
            return f"Error creating entry: {str(e)}"

    def format_date(self, date_string):
        """Smart date formatting for various input formats"""
        try:
            # Handle various date formats
            formats = [
                "%m/%d", "%m/%d/%y", "%m/%d/%Y",  # 11/12, 11/12/23, 11/12/2023
                "%b %d", "%B %d",  # Dec 11, December 11
                "%Y-%m-%d"  # 2023-12-11
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_string, fmt)
                    # Add current year if not specified
                    if fmt in ["%m/%d", "%b %d", "%B %d"]:
                        date_obj = date_obj.replace(year=datetime.now().year)
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None

    def query_bills_for_week(self):
        """Query bills due this week with improved formatting"""
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            response = self.notion.databases.query(
                database_id=self.database_ids['bills'],
                filter={
                    "and": [
                        {"property": "Due Date", "date": {"on_or_after": start_of_week.strftime('%Y-%m-%d')}},
                        {"property": "Due Date", "date": {"on_or_before": end_of_week.strftime('%Y-%m-%d')}},
                        {"property": "Type", "select": {"equals": "Bill"}}
                    ]
                }
            )

            if not response["results"]:
                return "No bills due this week."

            bills = []
            for bill in response["results"]:
                title = bill["properties"]["Inbox"]["title"][0]["text"]["content"]
                due_date = bill["properties"]["Due Date"]["date"]["start"]
                amount = bill["properties"].get("Amount", {}).get("number", "Amount not specified")
                bills.append(f"- {title}: Due {due_date} (${amount})")

            return "Bills due this week:\n" + "\n".join(bills)
        except Exception as e:
            return f"Error fetching bills: {str(e)}"

    def process_command(self, command):
        """Process natural language commands"""
        try:
            command = command.lower()
            
            if "show bills" in command or "upcoming bills" in command:
                return self.query_bills_for_week()
                
            elif "add to inbox" in command:
                # Extract content after "add to inbox:"
                content = command.split("add to inbox:")[1].strip()
                if not content:
                    return "Error: 'Add to inbox' command is incomplete."
                
                # Determine type and priority
                entry_type = "Brain Dump"
                priority = None
                
                if "bill" in content.lower():
                    entry_type = "Bill"
                elif "call" in content.lower():
                    entry_type = "Call"
                elif "email" in content.lower():
                    entry_type = "Email"
                
                if "urgent" in content.lower() or "high priority" in content.lower():
                    priority = "high"
                
                return self.create_inbox_entry(content, entry_type, priority=priority)
                
            else:
                return f"Processing command: {command}"
                
        except Exception as e:
            return f"Error processing command: {str(e)}"