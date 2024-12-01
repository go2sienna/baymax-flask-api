import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from baymax_notion_connection import BaymaxNotion

# Load .env variables
load_dotenv()

app = Flask(__name__)
baymax = BaymaxNotion()

@app.route('/baymax', methods=['POST'])
def baymax_endpoint():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)
        
        command = data.get("command", "")
        if not command:
            return jsonify({"error": "No command provided"}), 400
            
        response = baymax.process_command(command)
        return jsonify({"result": response})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)