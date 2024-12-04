import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion client with error checking
try:
    notion = Client(auth=os.getenv('NOTION_API_KEY'))
    print("Successfully connected to Notion API")
except Exception as e:
    print(f"Error connecting to Notion: {str(e)}")
    exit()

def create_conversation_logs_database(parent_page_id):
    database = {
        "parent": {
            "type": "page_id",
            "page_id": parent_page_id
        },
        "title": [{"type": "text", "text": {"content": "Conversation Logs"}}],
        "properties": {
            "Title": {"title": {}},  # Required by Notion
            "Date": {"date": {}},
            "Key Takeaways": {"rich_text": {}},
            "Action Items": {"rich_text": {}},
            "Categories": {
                "multi_select": {
                    "options": [
                        {"name": "Financial", "color": "blue"},
                        {"name": "Household", "color": "green"},
                        {"name": "Medical", "color": "red"},
                        {"name": "School", "color": "yellow"},
                        {"name": "System", "color": "purple"}
                    ]
                }
            },
            "Family Member": {
                "multi_select": {
                    "options": [
                        {"name": "SF"}, {"name": "Mika"}, 
                        {"name": "Gia"}, {"name": "Ani"},
                        {"name": "Ava"}, {"name": "Dai"},
                        {"name": "CBF"}, {"name": "Kai"},
                        {"name": "Oni"}, {"name": "Bumi"},
                        {"name": "Momo"}, {"name": "Noli"}
                    ]
                }
            },
            "Related Tasks": {
                "relation": {
                    "database_id": "14ff4a0e-0321-81cf-b7fd-c1ea84e7463f",
                    "single_property": {}
                }
            },
            "Full Conversation": {"rich_text": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Active", "color": "green"},
                        {"name": "Completed", "color": "blue"},
                        {"name": "Needs Follow-up", "color": "yellow"}
                    ]
                }
            }
        }
    }
    
    return notion.databases.create(**database)

# Your parent page ID
parent_page_id = "14ef4a0e03218095b3eec69f9310dfbb"

# Try to create database
try:
    response = create_conversation_logs_database(parent_page_id)
    print(f"Database created successfully! ID: {response['id']}")
except Exception as e:
    print(f"Error creating database: {str(e)}")