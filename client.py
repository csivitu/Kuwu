import socket
import subprocess

PORT = 3000
SERVER = 'server-ip-here'
ADDR = (SERVER, PORT)

def monitor_docker():
    result = subprocess.run(['docker','stats','--no-stream'], stdout=subprocess.PIPE)
    data = str(result.stdout, 'utf-8').split()
    data = data[16:]
    data = list(filter(lambda x: x != '/', data))

    return data

client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (64 - len(send_length))
    client.send(send_length)
    client.send(message)

while True:
    #msg = input()
    msg = monitor_docker()
    if(msg == '!DISCONNECT'):
        send(msg)
        break
    send(msg)

    