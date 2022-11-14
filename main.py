import socket
import threading

import rsa

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

choice = int(input("Choose:\n1.Host\n2.Connect\nYour response: "))

if choice==1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.7",9999))
    server.listen()

    client,_=server.accept()
elif choice==2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.7",9999))
else:
    print("Invalid choice!!!")
    exit(1)

def sending_message(c):
    while True:
        message=input("")
        print(LINE_UP, end=LINE_CLEAR)
        print(f"\rYou: {message}")
        c.send(message.encode())

def receiving_message(c):
    while True:
        print(f"Partner: {c.recv(1024).decode()}")

threading.Thread(target=sending_message,args=(client,)).start()
threading.Thread(target=receiving_message,args=(client,)).start()