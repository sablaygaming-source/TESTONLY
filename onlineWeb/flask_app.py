import json
import os
import uuid
import requests
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This handles the "Locked Door" (CORS) issue

MAKE_WEBHOOK_URL = 'https://hook.eu1.make.com/1s442riabjmpt3dubtwyv9hadn815ek1'


FILE_NAME = "users.json"

# The data you want to send
payload = {
    "sender_name": "Ron",
    "recipient": "migelbonie@gmail.com",
    "message": "",
    "data": {},
    "status": "Success"
}

headers = {
    "Content-Type": "application/json"
}

def save_to_json(new_user_data):
    global payload
    # 2. Add automatic fields
    new_user_data["id"] = str(uuid.uuid4())[:8]
    new_user_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload["data"] = new_user_data.copy()
    return new_user_data

# ROUTE 1: Serves your Frontend
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

# ROUTE 2: Handles the Sign Up
@app.route("/signup", methods=["POST"])
def signup(): #2
    global payload
    user_data = request.json
    # Simple check for required fields
    if not user_data.get("username") or not user_data.get("email"):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
        
    saved_user = save_to_json(user_data)
    
    fSendData()
    return jsonify({"status": "success", "user": payload}), 201
#2

def fSendData():#2
    print("\n\nnow sending...")
    global payload
    try:
        response = requests.post(
            MAKE_WEBHOOK_URL, 
            json=payload, 
            headers=headers
        )

        if response.status_code == 200:
            print(f"✅ Success! Make.com is now sending the email to {payload['recipient']}")
        else:
            print(f"❌ Failed. Error code: {response.status_code}")
            # If you see 410, remember to click 'Re-determine data structure' in Make
            print("Response Text:", response.text)

    except Exception as e:
        print(f"Connection Error: {e}")

#2


if __name__ == "__main__":
    app.run(debug=True)