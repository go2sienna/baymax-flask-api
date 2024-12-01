import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

class BaymaxNotion:
    def __init__(self):
        # Initialize Notion client with API key from environment variable
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_ids = {
            'inbox': '14ff4a0e-0321-8193-99e1-f25f9baeef57',  # Your Inbox DB ID
            'tasks': '14ff4a0e-0321-81a1-91ba-f86d5308dfc3',   # Your Tasks DB ID
            'bills': '14ff4a0e-0321-819d-b692-e2067927b019'    # Your Bills DB ID
        }

    def create_brain_dump(self, content):
        """Create a new Brain Dump entry in Notion"""
        try:
            properties = {
                "Inbox": {"title": [{"text": {"content": content}}]},  # Title field
                "Type": {"select": {"name": "Brain Dump"}},  # Select field for type
                "Date Logged": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}}  # Date field
            }

            response = self.notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties=properties
            )

            return f"Added to Brain Dump: {content}"

        except Exception as e:
            print(f"API Error: {str(e)}")
            return f"Error creating Brain Dump: {str(e)}"

    def sort_brain_dump(self, page_id, new_type):
        """Sort or convert brain dump to another type like 2Do, Project, etc."""
        try:
            # Ensure valid types are used for sorting
            valid_types = ["Brain Dump", "Bill", "Text", "Email", "Call", "2Do", "Project", "File"]
            if new_type not in valid_types:
                return f"Invalid type. Must be one of: {', '.join(valid_types)}"

            update_data = {
                "properties": {
                    "Type": {"select": {"name": new_type}}  # Update the type of task
                }
            }
            print(f"Sending update: {update_data}")

            response = self.notion.pages.update(
                page_id=page_id,
                **update_data
            )

            return f"Updated to type: {new_type}"

        except Exception as e:
            print(f"API Error: {str(e)}")
            return f"Error sorting: {str(e)}"

    def get_brain_dumps(self):
        """Fetch all brain dumps from the inbox database."""
        try:
            # Query to fetch all brain dumps
            response = self.notion.databases.query(
                database_id=self.database_ids['inbox'],
                filter={
                    "property": "Type",
                    "select": {
                        "equals": "Brain Dump"
                    }
                }
            )

            dumps = []
            for item in response['results']:
                content = item['properties']['Inbox']['title'][0]['text']['content']
                dumps.append({
                    'id': item['id'],
                    'content': content,
                    'date_logged': item['properties']['Date Logged']['date']['start']  # Date logged
                })
            return dumps

        except Exception as e:
            return f"Error fetching Brain Dumps: {str(e)}"

    def process_command(self, command):
        """Process commands from the user."""
        try:
            command = command.lower()

            # Handling brain dump creation
            if command.startswith("brain dump:") or command.startswith("dump:"):
                content = command.split(":", 1)[1].strip()
                return self.create_brain_dump(content)

            # Handling sorting of brain dump to a new type
            elif command.startswith("sort:"):
                parts = command.split(":", 1)[1].strip().split(" to ")
                if len(parts) != 2:
                    return "Invalid sort command. Format: sort: [page_id] to [type]"
                page_id = parts[0].strip()
                new_type = parts[1].strip()
                return self.sort_brain_dump(page_id, new_type)

            # Display all unsorted brain dumps
            elif command == "show brain dumps":
                dumps = self.get_brain_dumps()
                if not dumps:
                    return "No unsorted Brain Dumps found."
                return "\n".join([f"ID: {d['id']}\nContent: {d['content']}\nLogged On: {d['date_logged']}" for d in dumps])

            # Handling adding to inbox
            elif command.startswith("add to inbox:"):
                content = command.split(":", 1)[1].strip()
                return self.create_brain_dump(content)

            else:
                return "Try: 'brain dump:', 'add to inbox:', 'sort:', or 'show brain dumps'"

        except Exception as e:
            return f"Error processing command: {str(e)}"


# This block allows running the script with commands
if __name__ == "__main__":
    baymax = BaymaxNotion()

    # Example commands to run and test the functionality
    commands = [
        "brain dump: Test entry 1",  # Add a brain dump entry
        "add to inbox: Test bill payment",  # Add to inbox (same as brain dump)
        "sort: 14ff4a0e-0321-8193-99e1-f25f9baeef57 to 2Do",  # Sort the brain dump to 2Do (replace page_id with valid)
        "show brain dumps"  # Show all brain dumps
    ]

    # Loop through the commands to process them
    for cmd in commands:
        print(f"\nTesting: {cmd}")
        result = baymax.process_command(cmd)
        print(f"Result: {result}")
