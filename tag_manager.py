from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

class TagManager:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_API_KEY'))
        self.database_id = "152f4a0e-0321-81da-a50c-c904196bd984"
    
    def get_existing_topics(self):
        try:
            database = self.notion.databases.retrieve(database_id=self.database_id)
            if 'properties' in database and 'Topics' in database['properties']:
                options = database['properties']['Topics']['multi_select']['options']
                return [opt['name'] for opt in options]
            return []
        except Exception as e:
            print(f"Error getting topics: {str(e)}")
            return []

    def add_topic(self, new_topic):
        try:
            current_topics = self.get_existing_topics()
            if new_topic not in current_topics:
                database = self.notion.databases.update(
                    database_id=self.database_id,
                    properties={
                        "Topics": {
                            "multi_select": {
                                "options": [{"name": topic} for topic in current_topics + [new_topic]]
                            }
                        }
                    }
                )
                return True
            return False
        except Exception as e:
            print(f"Error adding topic: {str(e)}")
            return False