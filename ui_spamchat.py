import PySimpleGUI as sg
import time 
import pywinauto
import random
import os
import logging


# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# # Create a file handler
# file_handler = logging.FileHandler("file.log")
# file_handler.setFormatter(formatter)

# # Get the logger (or create a custom logger)
# logger = logging.getLogger(__name__)  # Replace __name__ with your logger name if desired

# # Set the logger level (optional, defaults to WARNING)
# logger.setLevel(logging.DEBUG)  # Change to your desired level (e.g., INFO, WARNING)

# # Add the handler to the logger
# logger.addHandler(file_handler)

def reload_roblox():
    print("Apps are running:")
    new_app = []
    # logger.info("Apps are running:")  
    yourExeName = "RobloxPlayerBeta.exe"  

    proc = pywinauto.application.process_get_modules()
    for p in proc:
        if yourExeName in p[1]:
            print(f"Connect to process: {p[0]}")
            # logger.info(f"Connect to process: {p[0]}")
            new_app.append([pywinauto.Application().connect(process=p[0],timeout=15),time.time(),p[0]])
    print("Connect to Roblox success!")
    # logger.info("Connect to Roblox success!")
    return new_app

try:
    application = reload_roblox()
except Exception as e:
    # logger.error("Line 47: Error when connect to Roblox!")
    print(e)
    # logger.error(e)
    

layout = [  [sg.Text("Enter your messages below:")],
            [sg.Multiline('Message 1\nMessage 2\n...', size=(100,10), expand_x=True, expand_y=True, k='messages')],
            [sg.Spin([i for i in range(1,999)], initial_value=5, k='time_repeat'), sg.Text('Repeat interval (in seconds)')],
            [sg.Spin([i for i in range(5)], initial_value=0.005, k='sleep_key'), sg.Text('Sleep time keyboard (in seconds)')],
            [sg.Spin([i for i in range(5)], initial_value=0.05, k='sleep_chat'), sg.Text('Sleep chat (in seconds)')],
            [sg.Button('Start'), sg.Button('Stop'),sg.Button('Reload Roblox')] ]

# Create the Window
window = sg.Window('AutoSendChat', layout,resizable=True)

# Event Loop to process "events" and get the "values" of the inputs
messages = []

from time import sleep
def auto_spam_chat(roblox,message,index,sleep_time,sleep_chat=0,process_id=None):
    # print(process_id)
    global application
    try:
        roblox.RobLox.click()
        roblox.RobLox.click("{w down}")
        roblox.Roblox.type_keys("{w up}")
        roblox.RobLox.click("{w down}")
        roblox.Roblox.type_keys("{w up}")
        roblox.Roblox.type_keys(" ",with_spaces=True)
        sleep(sleep_chat)
        roblox.Roblox.type_keys("{/ down}")
        roblox.Roblox.type_keys("{/ up}")
        for m in message:
            sleep(sleep_time)
            roblox.Roblox.type_keys(m,with_spaces=True)
        sleep(sleep_chat)
        roblox.Roblox.type_keys("~")
    except Exception as e:
        print(e)
        print("Reconnect to Roblox!")
        application[index][0] = pywinauto.Application().connect(process=process_id,timeout=15)



index = 0
sl_time = 5
import keyboard

def reset_message():
    global messages
    messages = []
    print("Spam stopped!")

keyboard.add_hotkey("ctrl+p",lambda: reset_message())


while True:
        if messages:
            if application:
                if time.time() > application[index][1]+sl_time:
                    auto_spam_chat(application[index][0],random.choice(messages),index,float(values["sleep_key"]),float(values["sleep_chat"]),application[index][2])
                    if index >= len(application)-1:
                        index =0
                    else:    
                        index += 1
            event, values = window.read(timeout=10)
        else:
            event, values = window.read()

        # if user closes window or clicks cancel
        if event == "Start":
            try:
                sl_time = values["time_repeat"]
                messages = [mess for mess in values["messages"].split("\n")]
                print("Spam is running...")
                # logger.info("Spam is running...")
                
            except Exception as e:
                # logger.error("Line 111: Error when connect to Roblox!")
                # logger.error(e)
                print(e)

        if event == "Reload Roblox":
            try:
                os.system('cls')
            except Exception as e:
                # logger.error("Line 118: Error when connect to Roblox!")
                print(e)
            print("Reload app Roblox!")
            # logger.info("Reload app Roblox!")
            application = reload_roblox()
        
        if event == "Stop":
            
            messages = []
            try:
                os.system('cls')
            except Exception:
                pass
            print("Spam is stopped!")
            # logger.info("Spam is stopped!")
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

window.close()
    # logger.info("Exit program! Error")