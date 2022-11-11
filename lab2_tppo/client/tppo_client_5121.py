import socketio
import requests
import sys


sio_client = socketio.Client()

def get_param(param):
    global host
    global port
    api_url = f"http://{host}:{port}/blind/{param}"
    return requests.get(api_url)

def set_param(param, value):
    global host
    global port
    api_url = f"http://{host}:{port}/blind?{param}={value}"
    return requests.get(api_url)

def check_cmd(cmd):
    invalid_cmd = False
    if cmd == []:
        print("Please, enter a command")
        invalid_cmd = True
    
    elif len(cmd) == 1:
        if cmd[0] not in ["get", "set"]:
            print("SyntaxError: Not supported this command!")
            invalid_cmd = True
        elif cmd[0] in ["get","set"]:
            print("SyntaxError: Put a parameter's name")
            invalid_cmd = True
    
    elif len (cmd) == 2:
        if cmd[0] == "set" and cmd[1] in ["shift_percent", "flux_percent", "current_ill"]:
            print(f"SyntaxError: Give a value for param {cmd[1]}")
            invalid_cmd = True
        elif cmd[0] != "get" or cmd[1] not in ["shift_percent", "flux_percent", "current_ill"]:
            print("SyntaxError: Not supported this command!")
            invalid_cmd = True
    elif len(cmd) == 3:
        if cmd[0] != "set":
            print("SyntaxError: Not supported this command!")
            invalid_cmd = True
        elif cmd[1] not in ["shift_percent", "flux_percent", "current_ill"]:
            print(f"SyntaxError: Not supported this parameter {cmd[1]}!")
            invalid_cmd = True
        elif not cmd[2].isdigit():
            print(f"SyntaxError: Give a value for param {cmd[1]}")
            invalid_cmd = True
    else: 
        invalid_cmd = False
    return invalid_cmd

@sio_client.event
def connect():
    global host
    global port
    print("[CONNECTED] Client connected to server successfully!")
    print("Please, enter a command")
    while(True):
        command = input()
        cmd = command.lower().split()
        if not check_cmd(cmd):
            if cmd[0] == "get":
                result = get_param(cmd[1]).json()
                if cmd[1] == "current_ill":
                    print(f"[SERVER]: Current illumination is {result[cmd[1]]} lx")
                else:
                    print(f"[SERVER]: Current {cmd[1]} is {result[cmd[1]]}%")
            if cmd[0] == "set":
                result = set_param(cmd[1], cmd[2]).json()
                if cmd[1] == "current_ill":
                    print(f"[SERVER]: {cmd[1]} was successful changed to {result[cmd[1]]} lx")
                else:
                    print(f"[SERVER]: {cmd[1]} was successful changed to {result[cmd[1]]}%")
            if cmd[0] == "exit":
                print("Disconnected!")
                break
                
@sio_client.on("notify changes")
def get_notice_changes(data):
    if data['params'] == "illumination":
        print(f"[SERVER]: {data['params']} has been changed to {data['value']} lx")
    else:
        print(f"[SERVER]: {data['params']} has been changed to {data['value']}%")

@sio_client.event
def disconnect():
    print("Disconnected!")

if (__name__ == "__main__"):
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    sio_client.connect(f"http://{host}:{port}")