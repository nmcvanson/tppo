import sys
import socket
import threading
from blinds import *
import os

class Server():
    def __init__(self, host, post, device):
        self.host = host
        self.port = port
        self.SIZE = 1024
        self.FORMAT = "utf-8"
        self.device = device
        self.clients = []

    def setup_socket(self):
        print("[STARTING]: Server is starting ...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"[LISTENING]: Server is listening on {host}:{port}")

    def response_get(self, params):
        if params == "Shift_Percent":
            msg = f"Current {params}: {self.device.get_shift_percentage()}%"
        elif params == "Luminous_Flux_Percent":
            msg = f"Current {params}: {self.device.get_luminous_flux_percentage()}%"
        elif params == "Current_Illumination":
            msg = f"Current {params}: {self.device.get_current_illumination()} lx"
        return msg

    def response_set(self, params, values):
        if params == "Shift_Percent":
            self.device.set_shift(values)
        elif params == "Luminous_Flux_Percent":
            self.device.set_luminous_flux(values)
        return f"{params} was successful changed to {values}%"

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            recv_data = conn.recv(self.SIZE).decode(self.FORMAT)
            recv_data = recv_data.title().split()
            lock.acquire()
            if recv_data:
                if recv_data == ["Exit"]:
                    print(f"Closing connection to {addr}")
                    connected = False
                    self.clients.remove(conn)
                    conn.close()
                elif recv_data[0] == "Get":
                    msg = self.response_get(params = recv_data[1])
                    conn.send(msg.encode(self.FORMAT))
                elif recv_data[0] == "Set":
                    msg = self.response_set(params = recv_data[1], values = recv_data[2])
                    conn.send(msg.encode(self.FORMAT))
            lock.release()

    def notify_changes(self):
        device_path = "../server/blinds.txt"
        cached_stamp = os.stat(device_path).st_mtime
        while True:
            stamp = os.stat(device_path).st_mtime
            if(stamp != cached_stamp):
                cached_stamp = stamp
                lock.acquire()
                shift_percentage = device.get_shift_percentage()
                luminous_flux_percentage = device.get_luminous_flux_percentage()
                current_illumination = device.get_current_illumination()
                lock.release()
                if (blinds_params['current_shift'] != shift_percentage):
                    blinds_params['current_shift'] = shift_percentage
                    for client in self.clients:
                        client.send(f"Shift percentage has been changed to {shift_percentage}%".encode(self.FORMAT))
                elif (blinds_params['current_luminous_flux'] != luminous_flux_percentage):
                    blinds_params['current_luminous_flux'] = luminous_flux_percentage
                    for client in self.clients:
                        client.send(f"Luminous fluxpercentage has been changed to {luminous_flux_percentage}%".encode(self.FORMAT))
                elif (blinds_params['current_illumination'] != current_illumination):
                    blinds_params['current_illnation'] = current_illumination
                    for client in self.clients:
                        client.send(f"Current illumination has been changed to {current_illumination} lx".encode(self.FORMAT))
    
    def check_conn(self, conn):
        connExists = False
        for client in self.clients:
            if (str(conn) == str(client)):
                connExists = True
                break
        return connExists

    def run(self):
        self.setup_socket()
        notify_thread = threading.Thread(target=self.notify_changes)
        notify_thread.daemon = True
        notify_thread.start()
        while True:
            conn, addr = self.sock.accept()
            if (self.check_conn(conn) == False):
                self.clients.append(conn)
            cli_thread = threading.Thread(target=self.handle_client, args= (conn, addr))
            cli_thread.daemon = True
            cli_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")

lock = threading.Lock()
device = Blinds()
shift_percentage = device.get_shift_percentage()
luminous_flux_percentage = device.get_luminous_flux_percentage()
current_illumination = device.get_current_illumination()
blinds_params = {
    "current_shift": shift_percentage,
    "current_luminous_flux": luminous_flux_percentage,
    "current_illumination": current_illumination
}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    host, port = sys.argv[1], int(sys.argv[2])
    server = Server(host, port, device)
    server.run()