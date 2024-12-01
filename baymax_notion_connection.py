import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaymaxNotion:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_ids = {
            'tasks': 'your-tasks-database-id',
            'inbox': 'your-inbox-database-id'
        }

    def query_tasks_for_today(self):
        """Fetch tasks due today."""
        # Implement Notion API query logic for today's tasks
        return "Tasks for today are not yet implemented."

    def query_tasks_for_week(self):
        """Fetch tasks for the week."""
        # Implement Notion API query logic for weekly tasks
        return "Tasks for this week are not yet implemented."

    def create_inbox_entry(self, content):
        """Add a task or note to the inbox."""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties={
                    "Title": {"title": [{"text": {"content": content}}]},
                    "Status": {"select": {"name": "New"}}
                }
            )
            return f"Added to inbox: {content}"
        except Exception as e:
            return f"Error adding to inbox: {str(e)}"

    def process_command(self, command):
        """Process natural language commands dynamically."""
        command = command.lower()

        # Handle task queries
        if "show tasks" in command:
            if "this week" in command:
                return self.query_tasks_for_week()  # Fetch tasks for the week
            elif "today" in command:
                return self.query_tasks_for_today()  # Fetch tasks for today
            else:
                return "Error: Please specify 'today' or 'this week' for tasks."

        # Handle adding to inbox
        elif "add to inbox" in command:
            task_content = command.split("add to inbox:")[1].strip()
            if not task_content:
                return "Error: 'Add to inbox' command is incomplete or invalid."
            return self.create_inbox_entry(task_content)

        # Default case for unsupported commands
        return f"Unknown command: {command}"
