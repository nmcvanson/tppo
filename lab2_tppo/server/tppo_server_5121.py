from flask import Flask, request, abort
from flask_socketio import SocketIO
import threading
from blinds import *
import os
import sys



app = Flask(__name__)
socketio = SocketIO(app)
mutex = threading.Lock()

device = Blinds()
current_shift_percent = device.get_shift_percentage()
current_flux_percent = device.get_luminous_flux_percentage()
current_ill = device.get_current_illumination()

@app.route('/blind/<string:param>')
def main(param):
    global mutex
    if (param == "shift_percent"):
        mutex.acquire()
        value = device.get_shift_percentage()
        mutex.release()
    elif (param == "flux_percent"):
        mutex.acquire()
        value = device.get_luminous_flux_percentage()
        mutex.release()
    elif (param == "current_ill"):
        mutex.acquire()
        value = device.get_current_illumination()
        mutex.release()
    else:
        abort(404)
        return "Not supported this parameters!!"
    return {param: value}

@app.route('/blind')   #Query String: http://host_ip/blind?<param>=<value>
def get_query_string():
    shift_percent = request.args.get('shift_percent')
    flux_percent = request.args.get('flux_percent')
    global mutex
    if (shift_percent):
        mutex.acquire()
        device.set_shift(shift_percent)
        mutex.release()
        return {"shift_percent":shift_percent}
    elif(flux_percent):
        mutex.acquire()
        device.set_luminous_flux(flux_percent)
        mutex.release()
        return {"flux_percent":flux_percent}
    else:
        abort(404)
        return "Not supported this parameters!!"

@socketio.on('connect')
def test_connect(auth):
    print("A new client has connected!")
    global notify_changes_thread
    if not notify_changes_thread.is_alive():
        notify_changes_thread.start()

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def notify_changes():
    global current_shift_percent
    global current_flux_percent
    global current_ill
    global socketio
    device_path = "../server/blinds.txt"
    cached_stamp = os.stat(device_path).st_mtime
    while(True):
        stamp = os.stat(device_path).st_mtime
        if(stamp != cached_stamp):
            cached_stamp = stamp
            mutex.acquire()
            shift_percent = device.get_shift_percentage()
            flux_percent = device.get_luminous_flux_percentage()
            illumination = device.get_current_illumination()
            mutex.release()

            if (current_shift_percent != shift_percent):
                current_shift_percent = shift_percent
                socketio.emit("notify changes", {"params": "shift_percent", "value": current_shift_percent}, broadcast=True)
            elif (current_flux_percent != flux_percent):
                current_flux_percent = flux_percent
                socketio.emit("notify changes",  {"params": "flux_percent", "value": current_flux_percent}, broadcast=True)

            elif (current_ill != illumination):
                current_ill = illumination
                socketio.emit("notify changes",  {"params": "illumination", "value": current_ill}, broadcast=True)

notify_changes_thread = threading.Thread(target=notify_changes)

if (__name__ == "__main__"):
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    print("[STARTING]: Server is starting ...")
    host, port = sys.argv[1], int(sys.argv[2])
    socketio.run(app, host=host,port=port, debug=False)   

