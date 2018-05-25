import socket
import subprocess
from flask import Flask, render_template
app = Flask(__name__)

proc = None

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=['GET', 'POST'])
def start_talkingraspi():
    global proc
    print(" > Start Pi home surveillance!")
    proc = subprocess.Popen(["python", "pi_surveillance.py", "-c", "conf.json"])
    print(" > Process id {}".format(proc.pid))
    return "Started!"


@app.route("/stop", methods=['GET', 'POST'])
def stop_talkingraspi():
    global proc
    print(" > Stop Pi home surveillance!talkingraspi!")
    # subprocess.call(["kill", "-9", "%d" % proc.pid])
    proc.kill()
    print(" > Process {} killed!".format(proc.pid))
    return "Stopped!"


@app.route("/status", methods=['GET', 'POST'])
def status_talkingraspi():
    global proc
    if proc is None:
        print(" > Pi home surveillance is resting")
        return "Resting!"
    if proc.poll() is None:
        print(" > Pi home surveillance!Talking raspi is running (Process {})!".format(proc.pid))
        return "Running!"
    else:
        print(" > Pi home surveillance is resting")
        return "Stopped!"

if __name__ == "__main__":
    print ("Connect to http://{}:5555 to controll Pi Home surveillance !!".format(get_ip_address()))
    app.run(host="192.168.0.100", port=5555)
