import json
import os
import uuid
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.responses import FileResponse # <--- Add this import

app = FastAPI()

# ... keep your CORS and other code here ...

# ADD THIS FUNCTION to serve the HTML file
@app.get("/")
def read_index():
    # This tells FastAPI: "When someone visits the home page, send index.html"
    return FileResponse('index.html')

# Keep your @app.post("/signup") below this


# Allow your Frontend to talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_NAME = "users.json"

# Data model for incoming requests
class UserRequest(BaseModel):
    username: str
    fullname: str
    email: str

def save_to_json(new_user_data):
    # 1. Load existing data or start fresh
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # 2. Add automatic fields
    new_user_data["id"] = str(uuid.uuid4())[:8] # Short unique ID
    new_user_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. Save back to file
    data.append(new_user_data)
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)
    return new_user_data

@app.post("/signup")
def signup(user: UserRequest):
    user_dict = user.dict()
    saved_user = save_to_json(user_dict)
    return {"status": "success", "user": saved_user}

@app.get("/")
def health_check():
    return {"message": "Server is running"}