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
            'inbox': '14ff4a0e-0321-8193-99e1-f25f9baeef57',
            'tasks': '14ff4a0e-0321-81a1-91ba-f86d5308dfc3',
            'bills': '14ff4a0e-0321-819d-b692-e2067927b019'
        }

    def create_brain_dump(self, content):
        """Create a new Brain Dump entry"""
        try:
            properties = {
                "Inbox": {"title": [{"text": {"content": content}}]},
                "Type": {"select": {"name": "Brain Dump"}},
                "Priority": {"rich_text": [{"text": {"content": "!"}}]},
                "Date Logged": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}}
            }
            response = self.notion.pages.create(
                parent={"database_id": self.database_ids['inbox']},
                properties=properties
            )
            return f"Added to Brain Dump: {content}"
        except Exception as e:
            return f"Error creating Brain Dump: {str(e)}"

    def sort_brain_dump(self, page_id, new_type):
        """Sort a Brain Dump into a specific type"""
        try:
            valid_types = ["2Do", "2Call", "2Pay", "2Email"]
            if new_type not in valid_types:
                return f"Invalid type. Must be one of: {', '.join(valid_types)}"

            self.notion.pages.update(
                page_id=page_id,
                properties={
                    "Type": {"select": {"name": new_type}}
                }
            )
            return f"Updated type to: {new_type}"
        except Exception as e:
            return f"Error sorting Brain Dump: {str(e)}"

    def get_brain_dumps(self):
        """Get all unsorted Brain Dumps"""
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

    def process_command(self, command):
        """Process natural language commands"""
        try:
            command = command.lower()
            
            if command.startswith("brain dump:") or command.startswith("dump:"):
                content = command.split(":", 1)[1].strip()
                return self.create_brain_dump(content)
                
            elif command.startswith("sort:"):
                # Format: "sort: [page_id] to [type]"
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
                
            else:
                return "Try: 'brain dump:', 'add to inbox:', 'sort:', or 'show brain dumps'"
                
        except Exception as e:
            return f"Error processing command: {str(e)}"