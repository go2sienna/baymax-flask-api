import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class BaymaxNotion:
    def __init__(self):
        # Initialize Notion client
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))

        # Define database IDs
        self.database_ids = {
            'tasks': 'your-tasks-database-id',  # Replace with your Notion Tasks database ID
            'inbox': 'your-inbox-database-id'   # Replace with your Notion Inbox database ID
        }

    def create_inbox_entry(self, content):
        """Create a new inbox entry in Notion."""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.database_ids["inbox"]},
                properties={
                    "Title": {"title": [{"text": {"content": content}}]},
                    "Status": {"select": {"name": "New"}}
                }
            )
            return f"Added to inbox: {content}"
        except Exception as e:
            return f"Error adding to inbox: {str(e)}"

    def query_tasks_for_today(self):
        """Fetch tasks due today."""
        try:
            today_date = datetime.now().strftime('%Y-%m-%d')
            response = self.notion.databases.query(
                database_id=self.database_ids['tasks'],
                filter={
                    "property": "Due Date",
                    "date": {
                        "equals": today_date
                    }
                }
            )

            if not response["results"]:
                return "No tasks found for today."

            tasks = [task["properties"]["Title"]["title"][0]["text"]["content"] for task in response["results"]]
            return f"Tasks for today: {', '.join(tasks)}"
        except Exception as e:
            return f"Error fetching tasks for today: {str(e)}"

    def query_tasks_for_week(self):
        """Fetch tasks due this week."""
        try:
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            response = self.notion.databases.query(
                database_id=self.database_ids['tasks'],
                filter={
                    "and": [
                        {
                            "property": "Due Date",
                            "date": {
                                "on_or_after": start_of_week.strftime('%Y-%m-%d')
                            }
                        },
                        {
                            "property": "Due Date",
                            "date": {
                                "on_or_before": end_of_week.strftime('%Y-%m-%d')
                            }
                        }
                    ]
                }
            )

            if not response["results"]:
                return "No tasks found for this week."

            tasks = [task["properties"]["Title"]["title"][0]["text"]["content"] for task in response["results"]]
            return f"Tasks for this week: {', '.join(tasks)}"
        except Exception as e:
            return f"Error fetching tasks for this week: {str(e)}"

    def process_command(self, command):
        """Process natural language commands dynamically."""
        command = command.lower()

        # Handle task queries
        if "show tasks" in command:
            if "this week" in command:
                return self.query_tasks_for_week()
            elif "today" in command:
                return self.query_tasks_for_today()
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
