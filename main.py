import socket
import threading

import rsa

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
CHUNK_SIZE = 1024

ip_addr, port = "192.168.1.7", 9999

public_key, private_key = rsa.newkeys(CHUNK_SIZE)
public_key_partner = None

choice = int(input("Choose:\n1.Host\n2.Connect\nYour response: "))
client = None

if choice == 1:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_addr, port))
    server.listen()
    print(f"Server listening on {ip_addr}:{port}")
    client, client_details = server.accept()
    client.send(public_key._save_pkcs1_pem())
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(CHUNK_SIZE))

    if client_details is not None:
        print(f"New connection from {client_details[0]}:{client_details[1]}")
        client_details = None
elif choice == 2:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip_addr, port))
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(CHUNK_SIZE))
    client.send(public_key._save_pkcs1_pem())
else:
    print("Invalid choice!!!")
    exit(1)


def sending_message(c):
    while True:
        message = input("")
        print(LINE_UP, end=LINE_CLEAR)
        print(f"You: {message}")
        c.send(rsa.encrypt(message.encode(), public_key_partner))


def receiving_message(c):
    while True:
        print(f"Partner: {rsa.decrypt(c.recv(CHUNK_SIZE),private_key).decode()}")


threading.Thread(target=sending_message, args=(client,)).start()
threading.Thread(target=receiving_message, args=(client,)).start()
