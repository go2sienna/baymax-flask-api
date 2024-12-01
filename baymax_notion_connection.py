import os
from dotenv import load_dotenv
from notion_client import Client
import openai

# Load environment variables
load_dotenv()

# Initialize OpenAI and Notion clients
openai.api_key = os.getenv("OPENAI_API_KEY")
notion = Client(auth=os.getenv("NOTION_API_KEY"))

class BaymaxNotion:
    def __init__(self):
        self.database_ids = {
            'inbox': 'your-inbox-database-id',
            'tasks': 'your-tasks-database-id',
            # Add more database IDs as needed
        }

    def query_tasks(self, filter_params=None):
        """Query tasks with optional filters."""
        try:
            response = notion.databases.query(
                database_id=self.database_ids['tasks'],
                filter=filter_params
            )
            tasks = response['results']
            return [task['properties']['Title']['title'][0]['text']['content'] for task in tasks]
        except Exception as e:
            return f"Error querying tasks: {str(e)}"

    def create_inbox_entry(self, content, entry_type="Brain Dump"):
        """Create a new entry in the inbox."""
        try:
            response = notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties={
                    "Title": {"title": [{"text": {"content": content}}]},
                    "Entry Type": {"select": {"name": entry_type}},
                    "Status": {"select": {"name": "New"}}
                }
            )
            return f"Added to inbox: {content}"
        except Exception as e:
            return f"Error creating inbox entry: {str(e)}"

    def process_command(self, command):
        """Process natural language commands."""
        if "show tasks" in command.lower():
            # Optional filter example for tasks this week
            filter_params = {
                "property": "Due Date",
                "date": {"on_or_after": "2024-12-01"}  # Adjust date logic if needed
            }
            tasks = self.query_tasks(filter_params)
            return f"Your tasks for this week: {', '.join(tasks)}" if tasks else "No tasks found."

        elif "add to inbox" in command.lower():
            try:
                content = command.split("add to inbox:", 1)[1].strip()
                return self.create_inbox_entry(content)
            except IndexError:
                return "Error: 'Add to inbox' command is incomplete or invalid."

        else:
            return f"Unknown command: {command}"
