import socket
import threading

import rsa

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

public_key,private_key=rsa.newkeys(1024)

public_key_partner=None

choice = int(input("Choose:\n1.Host\n2.Connect\nYour response: "))
client = None

if choice==1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.7",9999))
    server.listen()

    client,_=server.accept()
    client.send(public_key._save_pkcs1_pem())
    public_key_partner=rsa.PublicKey.load_pkcs1(client.recv(1024))

    if client is not None:
        print(client)
elif choice==2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.7",9999))
    public_key_partner=rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key._save_pkcs1_pem())
else:
    print("Invalid choice!!!")
    exit(1)

def sending_message(c):
    while True:
        message=input("")
        print(LINE_UP, end=LINE_CLEAR)
        print(f"\rYou: {message}")
        c.send(rsa.encrypt(message.encode(),public_key_partner))

def receiving_message(c):
    while True:
        print(f"Partner: {rsa.decrypt(c.recv(1024),private_key).decode()}")

threading.Thread(target=sending_message,args=(client,)).start()
threading.Thread(target=receiving_message,args=(client,)).start()