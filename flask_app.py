import json
import os
import uuid
import requests
from datetime import datetime, timezone, timedelta

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This handles the "Locked Door" (CORS) issue

#old URL
#MAKE_WEBHOOK_URL = 'https://hook.eu1.make.com/1s442riabjmpt3dubtwyv9hadn815ek1'

MAKE_WEBHOOK_URL = 'https://hook.eu1.make.com/1s442riabjmpt3dubtwyv9hadn815ek1'


FILE_NAME = "users.json"

# The data you want to send
mainData = []
mainIndex = ["BankTransaction","AccountId", "Code", "BankName" ,
            "Type", "Date","ContactName", "ContactNo", "Currency", 
            "Status"]
mainLen = 0
mainId = 0
headers = {
    "Content-Type": "application/json"
}

def fGetJson():#2
    global mainIndex
    global mainData
    global mainId
    if os.path.exists(FILE_NAME): #3
        with open(FILE_NAME) as vFile:#4
            try :#5
                mainData = json.load(vFile)
            except json.JSONDecodeError as error1 : #5
                print(f"\nRSM Error:{error1.message}")
            #5
        #4       
    #5
    if not mainData: #10
        mainId = 1
    else: #10

        mainId = mainData[len(mainData)]["AccountId"]
    #10

    return mainData
#2

def save_to_json(): #2
    global mainData

    with open(FILE_NAME, "w") as file: #7
        json.dump(mainData, file, indent=4)
    #7

#2

# ROUTE 1: Serves your Frontend
@app.route("/")
def index():#2
    return render_template("index.html")    
#2

@app.route('/api/BankTransaction', methods=['GET'])
def fBankTransaction(): #2
    
    print(f"\n\ndebug loading fBankTransaction ")
        
    try: #3
        global mainData
        fGetJson()

        return jsonify({"status": "success", "user": mainData}), 201
            
    except Exception as e: #3
        print(f"\n\ndebug fBankTransaction inside exception e \n\n") 
        return jsonify({
            "status": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "hint": "This is a server-side variable error (undefined or missing global)"
            }
        }), 500
    #3   

    #debug this original linecode
    #return jsonify({"status": "success", "user": mainData}), 201
#2

@app.route('/api/BankTransaction', methods=['POST'])
def fBankTransactionPost(): #2
    try: #3
        
        #global mainLen
        print(f"\n\ndebug loading fBankTransactionPost ")
        vData = request.json
        
        #disabled id creator, i will create my own using mainIndex
        #vData["AccountId"] = str(uuid.uuid4())[:8]
        ph_time = datetime.now(timezone.utc) + timedelta(hours=8)
        vData["Date"] = ph_time.strftime("%Y-%m-%d %H:%M:%S")
        
        mainData.append(vData)
        mainLen +=1

        #write to json file
        save_to_json() 
        print(f"\n\ndebug sucess fBankTransactionPost \n\n") 
        return jsonify({"status": "success"}), 201
            
    except Exception as e: #3
        print(f"\n\ndebug inside exception e \n\n") 
        return jsonify({
            "status": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "hint": "This is a server-side variable error (undefined or missing global)"
            }
        }), 500
    #3   
#2

if __name__ == "__main__":
    print(f"\n\n##################\ndebug RSM program is starting")
    app.run(debug=True)
    print(f"\n\n##################\ndebug RSM EXITING PROGRAM....")
