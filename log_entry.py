import os
from notion_client import Client
from datetime import datetime

class ConversationLogger:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_id = "152f4a0e-0321-81d7-bcf3-cbeee4c87875"

    def create_entry(self, conversation, categories=None):
        properties = {
            "Title": {"title": [{"text": {"content": f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
            "Full Conversation": {"rich_text": [{"text": {"content": conversation}}]},
            "Status": {"select": {"name": "Active"}}
        }
        
        if categories:
            properties["Categories"] = {"multi_select": [{"name": cat} for cat in categories]}

        return self.notion.pages.create(parent={"database_id": self.database_id}, properties=properties)