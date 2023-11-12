import socket
import threading
from Client import Client
import logging

# Configure the logging module
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# global variables
MAX_PACKET = 1024
HOST = '0.0.0.0'
PORT = 1729
online_clients = []


def handle_client(client):
    try:
        # get client name
        client.name = client.receive_message()
        online_clients.append(client)
        logging.info(f"Client {client.name} connected with address {client.address}")

        while True:
            message = client.receive_message()
            if not message:
                break
            logging.debug(f"Received message from {client.name}: {message}")
            message = message + "but echoed!"
            message = f"{str(len(message))}![0]"
            client.send_message(message)
    finally:
        logging.info(f"Client {client.name} disconnected.")
        client.disconnect()
        online_clients.remove(client)


def server_loop(bind_ip, bind_port):
    # setting up server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    logging.info(f"[*] Server listening on {bind_ip}: {bind_port}")

    # accepting clients requests indefinitely
    while True:
        client_sock, addr = server.accept()
        logging.info(f"[*] Accepted connection from {addr[0]}: {addr[1]}")
        client_object = Client(client_sock, None, addr)
        client_handler = threading.Thread(target=handle_client, args=(client_object,))
        client_handler.start()


if __name__ == "__main__":
    server_loop(HOST, PORT)
