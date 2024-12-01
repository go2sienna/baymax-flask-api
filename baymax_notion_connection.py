import os
from dotenv import load_dotenv
import openai
from notion_client import Client
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize clients
openai.api_key = os.getenv('OPENAI_API_KEY')
notion = Client(auth=os.getenv('NOTION_API_KEY'))

class BaymaxNotion:
    def __init__(self):
        # Initialize with all database IDs
        self.database_ids = {
            'inbox': '14ff4a0e-0321-818e-a643-cac8a69f106f',
            'tasks': '14ff4a0e-0321-81bf-8fa8-d94e1825dc23',
            'bills': '14ff4a0e-0321-8197-8330-d5eea6cbd03f',
            'assistance': '14ff4a0e-0321-81d4-982b-ce2eabdba3bb',
            'documents': '14ff4a0e-0321-8196-9192-fc4f9edc2806',
            'individuals': '14ff4a0e-0321-818d-ab23-f1a14a4e5cb3',
            'accounts': '14ff4a0e-0321-81df-ab53-d6795062899f'
        }

    def create_inbox_entry(self, content):
        """Create a new entry in the inbox"""
        try:
            response = notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties={
                    "Title": {"title": [{"text": {"content": content}}]},
                    "Entry Type": {"select": {"name": "Brain Dump"}},
                    "Status": {"select": {"name": "New"}},
                    "Priority": {"select": {"name": "Medium (This Month)"}}
                }
            )
            return f"Added to inbox: {content}"
        except Exception as e:
            return f"Error creating inbox entry: {str(e)}"

    def process_command(self, command):
        """Process natural language commands"""
        try:
            if command.lower().startswith("add to inbox:"):
                # Extract content after "Add to inbox:"
                content = command[13:].strip()  # Remove "Add to inbox:" and whitespace
                return self.create_inbox_entry(content)
            elif "show tasks" in command.lower():
                return self.query_tasks()
            else:
                return f"Processing command: {command}"

        except Exception as e:
            return f"Error processing command: {str(e)}"

    def query_tasks(self):
        """Query tasks"""
        try:
            response = notion.databases.query(
                database_id=self.database_ids['tasks']
            )
            tasks = response['results']
            return f"Found {len(tasks)} tasks"
        except Exception as e:
            return f"Error querying tasks: {str(e)}"