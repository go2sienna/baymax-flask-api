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
            'inbox': '14ff4a0e-0321-8193-99e1-f25f9baeef57',  # Your Inbox DB ID
            'tasks': '14ff4a0e-0321-81a1-91ba-f86d5308dfc3',   # Your Tasks DB ID
            'bills': '14ff4a0e-0321-819d-b692-e2067927b019'    # Your Bills DB ID
        }

    def create_brain_dump(self, content):
        """Create a new Brain Dump entry"""
        try:
            properties = {
                "Inbox": {"title": [{"text": {"content": content}}]},
                "Type": {"select": {"name": "Brain Dump"}},
                "Date Logged": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}},
                "Priority": {"select": {"name": "!"}}  # Default priority
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
        """Sort a Brain Dump into a specific type"""
        try:
            # Valid types for the "Type" field
            valid_types = ["Brain Dump", "Bill", "Text", "Email", "Call", "Do", "Project", "File"]
            
            # Ensure the new_type is valid
            if new_type not in valid_types:
                return f"Invalid type. Must be one of: {', '.join(valid_types)}"

            update_data = {
                "properties": {
                    "Type": {"select": {"name": new_type}}
                }
            }
            print(f"Sending update: {update_data}")
            
            # Send update request to Notion API
            response = self.notion.pages.update(
                page_id=page_id,
                **update_data
            )
            
            # If response contains 'object' key, update was successful
            if 'object' in response and response['object'] == 'page':
                return f"Updated to type: {new_type}"
            else:
                return f"Failed to update type. Response: {response}"
        except Exception as e:
            # Log API errors for easier debugging
            print(f"API Error: {str(e)}")
            return f"Error sorting: {str(e)}"

    def get_brain_dumps(self):
        """Fetch all Brain Dump entries"""
        try:
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
                    'content': content
                })
            return dumps
        except Exception as e:
            return f"Error fetching Brain Dumps: {str(e)}"

    def auto_sort_brain_dumps(self):
        """Auto-sort brain dumps based on content analysis"""
        try:
            dumps = self.get_brain_dumps()
            for dump in dumps:
                content = dump['content'].lower()

                # Medical/Appointment patterns
                if any(word in content for word in ['doctor', 'medical', 'ortho', 'appointment', 'appt']):
                    person = next((name for name in ['gia', 'ava', 'ani'] if name in content), None)

                    # Update page based on identified person
                    self.notion.pages.update(
                        page_id=dump['id'],
                        properties={
                            "Type": {"select": {"name": "medical"}},
                            "Tags": {"multi_select": [
                                {"name": "health"},
                                {"name": person} if person else {"name": "family"},
                                {"name": "appointment"}
                            ]}
                        }
                    )
            return "Auto-sorting complete"
        except Exception as e:
            return f"Error auto-sorting: {str(e)}"

    def process_command(self, command):
        """Process commands from the user"""
        try:
            command = command.lower()

            if command.startswith("brain dump:") or command.startswith("dump:"):
                content = command.split(":", 1)[1].strip()
                return self.create_brain_dump(content)

            elif command.startswith("sort:"):
                parts = command.split(":", 1)[1].strip().split(" to ")
                if len(parts) != 2:
                    return "Invalid sort command. Format: sort: [page_id] to [type]"
                return self.sort_brain_dump(parts[0].strip(), parts[1].strip())

            elif command == "show brain dumps":
                dumps = self.get_brain_dumps()
                if not dumps:
                    return "No unsorted Brain Dumps found."
                return "\n".join([f"ID: {d['id']}\nContent: {d['content']}\n" for d in dumps])

            elif command.startswith("add to inbox:"):
                content = command.split(":", 1)[1].strip()
                return self.create_brain_dump(content)

            elif command == "auto sort brain dumps":
                return self.auto_sort_brain_dumps()

            else:
                return "Try: 'brain dump:', 'add to inbox:', 'sort:', 'auto sort brain dumps', or 'show brain dumps'"

        except Exception as e:
            return f"Error processing command: {str(e)}"

# Initialize the BaymaxNotion instance and process commands
if __name__ == "__main__":
    baymax = BaymaxNotion()

    # Test commands
    commands = [
        "brain dump: Test entry 1",
        "add to inbox: Test bill payment",
        "show brain dumps",
        "auto sort brain dumps"
    ]

    for cmd in commands:
        print(f"\nTesting: {cmd}")
        result = baymax.process_command(cmd)
        print(f
