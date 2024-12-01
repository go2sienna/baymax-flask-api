import requests

# Replace this URL with your Render public URL when live
url = "http://127.0.0.1:10000/baymax"
headers = {'Content-Type': 'application/json'}

# Test commands
commands = [
    {"command": "Add to inbox: Schedule Gia's doctor appointment for next week"},
    {"command": "Add to inbox: ESWA water bill due on the 20th - $113.09"},
    {"command": "Show my tasks for this week"}
]

for cmd in commands:
    response = requests.post(url, json=cmd, headers=headers)
    print(f"\nCommand: {cmd['command']}")
    print("Response:", response.json())
