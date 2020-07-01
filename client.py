import socket

PORT = 3000
SERVER = 'server-ip-here'
ADDR = (SERVER, PORT)

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
    msg = input()
    if(msg == '!DISCONNECT'):
        send(msg)
        break
    send(msg)