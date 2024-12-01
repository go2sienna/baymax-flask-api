import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime, timedelta

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
       try:
           properties = {
               "Inbox": {"title": [{"text": {"content": content}}]},
               "Type": {"select": {"name": "Brain Dump"}},
               "Date Logged": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}}
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
       try:
           valid_types = ["Brain Dump", "Bill", "Text", "email", "call", "Do", "Project", "File"]
           if new_type not in valid_types:
               return f"Invalid type. Must be one of: {', '.join(valid_types)}"

           update_data = {
               "properties": {
                   "Type": {"select": {"name": new_type}}
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
               
           else:
               return "Try: 'brain dump:', 'add to inbox:', 'sort:', or 'show brain dumps'"
               
       except Exception as e:
           return f"Error processing command: {str(e)}"

if __name__ == "__main__":
   baymax = BaymaxNotion()
   
   # Test commands
   commands = [
       "brain dump: Test entry 1",
       "add to inbox: Test bill payment",
       "show brain dumps"
   ]
   
   for cmd in commands:
       print(f"\nTesting: {cmd}")
       result = baymax.process_command(cmd)
       print(f"Result: {result}")