import socket
import threading
import sys


class Client:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.SIZE = 1024
        self.FORMAT = "utf-8"
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    def _input_and_send_loop(self):
        try:
            while True:
                command = input() 
                cmd = command.title().split()
                if not self.check_cmd(cmd):
                    self._socket.send(command.encode(self.FORMAT))
                    if cmd == ["Exit"]:
                        print(f"Closing connection!")
                        self.connected = False
                        self._socket.close()
                        sys.exit()

        except:  
            self.connected = False
            sys.exit()

    def check_cmd(self, cmd):
        self.invalid_cmd = False
        if cmd == []:
            print("Please, enter a command")
            self.invalid_cmd = True
        
        elif len(cmd) == 1:
            if cmd[0] not in ["Get", "Set", "Exit"]:
                print("SyntaxError: Not supported this command!")
                self.invalid_cmd = True
            elif cmd[0] in ["Get","Set"]:
                print("SyntaxError: Put a parameter's name")
                self.invalid_cmd = True
        
        elif len (cmd) == 2:
            if cmd[0] == "Set" and cmd[1] in ["Shift_Percent", "Flux_Percent", "Current_Ill"]:
                print(f"SyntaxError: Give a value for param {cmd[1]}")
                self.invalid_cmd = True
            elif cmd[0] != "Get" or cmd[1] not in ["Shift_Percent", "Flux_Percent", "Current_Ill"]:
                print("SyntaxError: Not supported this command!")
                self.invalid_cmd = True
        elif len(cmd) == 3:
            if cmd[0] != "Set":
                print("SyntaxError: Not supported this command!")
                self.invalid_cmd = True
            elif cmd[1] not in ["Shift_Percent", "Flux_Percent", "Current_Ill"]:
                print(f"SyntaxError: Not supported this parameter {cmd[1]}!")
                self.invalid_cmd = True
            elif not cmd[2].isdigit():
                print(f"SyntaxError: Give a value for param {cmd[1]}")
                self.invalid_cmd = True
        else: 
            self.invalid_cmd = False
        return self.invalid_cmd

    def connect(self):
        self._socket.connect((self._host, self._port))
        self.connected = True
        print(f"[CONNECTED] Client connected to server at {self._host}:{self._port}")
        threading.Thread(target=self._input_and_send_loop).start()
        try: 
            while self.connected:
                msg = self._socket.recv(self.SIZE).decode(self.FORMAT)
                if msg:
                    print(f"[SERVER] {msg}")
                else:
                    sys.exit()
        except:
            sys.exit()

        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    host, port = sys.argv[1:3]
    client = Client(host, int(port))
    client.connect()