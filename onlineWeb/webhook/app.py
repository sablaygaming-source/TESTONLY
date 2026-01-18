import requests
import json
import threading
import sys

# Replace this with your ACTIVE Webhook URL from Make.com
MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/1s442riabjmpt3dubtwyv9hadn815ek1"
exit_event = threading.Event()

startProcess = False

# The data you want to send
payload = {
    "sender_name": "Ron",
    "recipient": "migelbonie@gmail.com",
    "message": "blank",
    "status": "Success"
}

headers = {
    "Content-Type": "application/json"
}

def fSendData():#2
    print("\n\nnow sending...")
    try:
        response = requests.post(
            MAKE_WEBHOOK_URL, 
            data=json.dumps(payload), 
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

def fAutomationTask(stop_event): #2
    """This function runs in the background (Thread A)"""
    global startProcess
    print("\n--- Background Automation Started ---")
    
    while not stop_event.is_set():#10
        # wait() returns True if the event was set (q was pressed)
        # and False if the timer just ran out normally

        #print(f"\ndebug before while dSec")

        dSec = 0
        while dSec < 60 : #11

            stop_event.wait(timeout=1)

            #print(f"\ndebug {dSec= }")    
            
            #standby
            if startProcess == False:#12
                while not startProcess :#14
                    pass #to stand by here
                #14
                print(f"\nstarting to count in 60 seconds")
                dSec = 0 
            #12
            dSec += 1
        #11

        fSendData()
            
    #10
    
    print("\nBackground thread safely stopped.")
    
    
#2

def fInputInfo(pPrompt):#2

    while True: #3
        ch = input(f"\npress b to back, enter {pPrompt}: ")
        if ch == '':#4
            print(f"\nblank input is not valid")
            continue
        #5
        return ch
    #3
#2
def fMain(): #2
    
    global exit_event
    global startProcess
    print("Initiating email blast via Make.com...")
    
    # Inside fMain, when you start the thread:
    background_thread = threading.Thread(target=fAutomationTask, args=(exit_event,))
    background_thread.start()
    

    # 3. Main Thread (Thread B) stays here in standby mode
    print("System is running..")

    vIndex = 0
    while True: #3
        print(f"\ninformation last email: {payload['recipient']}\nlast message {payload['message']}")
        ch= input(f"\ninput q to leave, main menu i input new send set ")
        
        if ch.lower() == 'q':#4            

            #set daemon = True to force it to close, and not finishing the function work
            # threading.Thread(target=fAutomationTask, daemon= True) 
            exit_event.set()
            background_thread.join()
            print("\nexiting prog...")
            sys.exit()    
            return
        
        elif ch.lower() == 'i': #4
            #input process    
            startProcess = False
            vEmail = fInputInfo("Email")
                
            if vEmail.lower() == 'b':#10
                
                continue        
            #10
            
            payload['recipient'] = vEmail
            
            vMessage = fInputInfo("Message")
                
            if vMessage.lower() == 'b':#10
                continue        
            #10
            
            payload['message'] = vMessage

            startProcess = True
        #4
    #3
#2

fMain()



"""
    import requests
import threading
import time
import sys

# Your Make.com URL
MAKE_WEBHOOK_URL = "https://hook.us1.make.com/your_id_here"

# This variable controls the loop
running = True

def automation_task():
    #This function runs in the background (Thread A)
    global running
    print("--- Background Automation Started ---")
    
    while running:
        try:
            payload = {"message": "Ron's Automated Update", "status": "Active"}
            requests.post(MAKE_WEBHOOK_URL, json=payload)
            print("\n[Auto] Data sent to Make.com")
        except Exception as e:
            print(f"\n[Error] {e}")
        
        # We check 'running' frequently so the app closes fast when you exit
        for _ in range(60): 
            if not running: break
            time.sleep(1)

# --- MAIN EXECUTION ---

# 1. Create the thread for the background task
background_thread = threading.Thread(target=automation_task)

# 2. Start the thread
background_thread.start()

# 3. Main Thread (Thread B) stays here in standby mode
print("System is running. Type 'exit' to stop the program.")

while True:
    user_input = input("Command: ").strip().lower()
    
    if user_input == 'exit':
        print("Stopping system... please wait.")
        running = False # This tells the background thread to stop
        background_thread.join() # Wait for the background thread to finish
        print("System Offline.")
        sys.exit() # Close the program
    else:
        print(f"Unknown command: {user_input}. Only 'exit' is supported.")

        
import requests
import time

MAKE_WEBHOOK_URL = "https://hook.us1.make.com/your_id_here"

def send_data():
    payload = {"message": "This is Ron sending a scheduled message", "sender": "Ron"}
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("Successfully sent to Make.com")
    except Exception as e:
        print(f"Error: {e}")

# The Loop
while True:
    send_data()
    print("Waiting for 1 minute...")
    time.sleep(60)  # 60 seconds = 1 minute


    # At the top of fMain
exit_event = threading.Event()

def fAutomationTask(stop_event):
    print("--- Background Automation Started ---")
    while not stop_event.is_set():
        # wait() returns True if the event was set (q was pressed)
        # and False if the timer just ran out normally
        event_triggered = stop_event.wait(timeout=60) 
        
        if not event_triggered: # Timer ran out, send data
            fSendData()
    print("Background thread safely stopped.")

# Inside fMain, when you start the thread:
background_thread = threading.Thread(target=fAutomationTask, args=(exit_event,))
background_thread.start()

# Inside your 'q' logic:
if ch.lower() == 'q':
    exit_event.set() # This "wakes up" the timer immediately!
    background_thread.join()
    sys.exit()
    
"""

