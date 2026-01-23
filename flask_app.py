import json
import os
import uuid
import requests
from datetime import datetime, timezone, timedelta
from threading import Thread, Lock
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

import time 

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

#setup of timer
timer_data = {'time': 'None', 'running': False}
timer_lock = Lock()


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

        print(f"\ndebug fGetJson false {len(mainData)=}")
        mainLen = len(mainData)        
        mainId = mainData[mainLen -1 ]["AccountId"]
        mainId = fStrToNum(mainId)
    #10

    return mainData
#2

#convert string to number
def fStrToNum(pNum):#2

    try :#3
        n = int(pNum)
    except ValueError as e1 :#3
        print(f"\n\ndebug not a valid number the {pNum}")
        n= 0
    #3
    return n
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
    #initial mainData
    fGetJson()
    return render_template("index.html")    
#2

#use in initial and refresh client
@app.route('/api/BankTransaction', methods=['GET'])
def fBankTransaction(): #2
    
    print(f"\n\ndebug loading fBankTransaction ")
        
    try: #3
        global mainData
        
        return jsonify({"status": "success", "user": mainData}), 201
            
    except Exception as e: #3
        print(f"\n\ndebug fBankTransaction inside exception e {e=}\n\n") 
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

#came from submit button client
@app.route('/api/BankTransaction', methods=['POST'])
def fBankTransactionPost(): #2
    try: #3
        global mainData
        global mainLen
        global mainId

        #global mainLen
        print(f"\n\ndebug loading fBankTransactionPost ")
        vData = request.json
        
        #disabled id creator, i will create my own using mainIndex
        #vData["AccountId"] = str(uuid.uuid4())[:8]
        
        #updates the mainId
        mainId +=1
        #now save id and date
        vData["AccountId"] = str(mainId)        
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

@app.route('/kabisoteako/me', methods = ['GET'])
def fRefreshTable():#2
    global mainData
    return jsonify({"status": "success", "user": mainData}), 201
#2

#thread library use this function to process
def run_timer():
    global timer_data
    global timer_lock
    while True:
        with timer_lock:
            #print(f"\ndebug run_timer {timer_data=}")
            if timer_data['running']:
                vTime = datetime.now()
                timer_data['time'] = vTime.strftime("%Y/%m/%d = %H:%M:%S")
                #print(f"\ndebug run_timer {timer_data=}")
        time.sleep(1)

@app.route('/api/timer123/start', methods=['POST'])
def start_timer():
    global timer_data
    with timer_lock:
        timer_data['running'] = True
        
        print(f"\ndebug start_timer {timer_data=}")

    return jsonify({'status': 'started'}), 201

#the route value is the address use
#this is use every time the timer updates, client get time here
@app.route('/api/timer123', methods=['GET'])
def get_timer():
    global timer_data
    global timer_lock
    print(f"\ndebug get_timer {timer_data=}")
    with timer_lock:
        return jsonify({"status": "ok", "user": timer_data}),200


@app.route('/api/timer123/stop', methods=['POST'])
def stop_timer():
    global timer_data
    global timer_lock
    with timer_lock:
        timer_data['running'] = False
    return jsonify({'status': 'stopped'}), 201


# Start background thread
timer_thread = Thread(target=run_timer, daemon=True)
timer_thread.start()


if __name__ == "__main__": #3
    print(f"\n\n##################\ndebug RSM program is starting")
    
    app.run(debug=True)
    print(f"\n\n##################\ndebug RSM EXITING PROGRAM....")
#3