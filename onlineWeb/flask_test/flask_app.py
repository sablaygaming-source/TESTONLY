import json
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This handles the "Locked Door" (CORS) issue

FILE_NAME = "users.json"

def save_to_json(new_user_data):
    # 1. Load existing data
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # 2. Add automatic fields
    new_user_data["id"] = str(uuid.uuid4())[:8]
    new_user_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. Save back to file
    data.append(new_user_data)
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)
    return new_user_data

# ROUTE 1: Serves your Frontend
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

# ROUTE 2: Handles the Sign Up
@app.route("/signup", methods=["POST"])
def signup():
    user_data = request.json
    # Simple check for required fields
    if not user_data.get("username") or not user_data.get("email"):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
        
    saved_user = save_to_json(user_data)
    return jsonify({"status": "success", "user": saved_user}), 201

if __name__ == "__main__":
    app.run(debug=True)