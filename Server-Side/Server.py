import socket
import threading
from Client import Client

MAX_PACKET = 1024
HOST = '0.0.0.0'
PORT = 1729
online_clients = []


def handle_client(client):
    try:
        # get client name
        client.name = client.get_message()
        online_clients.append(client)
        while True:
            message = client.receive_message()
            if not message:
                break
            print(f"Received message: {message}")
            client.send_message(message)
    finally:
        client.disconnect()
        online_clients.remove(client)


def server_loop(bind_ip, bind_port):
    # setting up server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print(f"[*] Listening on {bind_ip}:{bind_port}")

    # accepting clients requests indefinitely
    while True:
        client_sock, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_object = Client(client_sock, None, addr)
        client_handler = threading.Thread(target=handle_client, args=(client_object))
        client_handler.start()


if __name__ == "__main__":
    server_loop(HOST, PORT)
