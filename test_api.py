import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variable or default to local URL
API_URL = os.getenv('API_URL', 'http://127.0.0.1:5000/baymax')

def test_baymax_api():
    headers = {'Content-Type': 'application/json'}
    
    # Test commands
    commands = [
        {"command": "Add to inbox: Schedule Gia's doctor appointment for next week"},
        {"command": "Add to inbox: ESWA water bill due on the 20th - $113.09"},
        {"command": "Show my tasks for this week"}
    ]
    
    print(f"Testing API at: {API_URL}")
    
    for cmd in commands:
        try:
            print(f"\nTesting command: {cmd['command']}")
            response = requests.post(API_URL, json=cmd, headers=headers)
            print("Status Code:", response.status_code)
            print("Response:", response.json())
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    test_baymax_api()