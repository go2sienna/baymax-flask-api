import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Placeholder for Notion functionality
class BaymaxNotion:
    def process_command(self, command):
        if "Add to inbox" in command:
            return f"Added to inbox: {command.replace('Add to inbox:', '').strip()}"
        elif "Show my tasks" in command:
            return f"Here are your tasks for this week."
        else:
            return f"Unknown command: {command}"

# Load .env variables
load_dotenv()

app = Flask(__name__)
baymax = BaymaxNotion()

@app.route('/baymax', methods=['POST'])
def baymax_endpoint():
    try:
        data = request.get_json(force=True)
        command = data.get("command", "")
        if not command:
            return jsonify({"error": "No command provided"}), 400
        response = baymax.process_command(command)
        return jsonify({"result": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
