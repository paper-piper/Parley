import socket
from threading import Thread

# Constants
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1729
MAX_PACKET = 1024
online_clients = []


def connect_to_server():
    """
    Establishes a connection to the server.
    :return a connected socket:
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server's address
    server_address = (SERVER_HOST, SERVER_PORT)
    print(f"Connecting to {SERVER_HOST} port {SERVER_PORT}")
    sock.connect(server_address)

    return sock


def send_username(sock, username):
    """ Sends the username to the server after connection. """
    try:
        # Send data
        print(f"Sending username {username}")
        sock.send(username.encode())
    except socket.error as e:
        print(f"Failed to send username. Error: {e}")


def send_message(sock, username):
    """ Sends messages to the server based on user input. """
    try:
        while True:
            # Wait for the user to input a message
            message = input(f"{username}> ")
            # Send the message
            sock.send(message.encode())
            # Stop if the message is 'quit'
            if message.lower() == 'quit':
                break
    except socket.error as e:
        print(f"Failed to send message. Error: {e}")
    finally:
        print("Closing the connection.")
        sock.close()


def receive_message(sock):
    """
    Receives messages from the server.
    :param sock:
    :return:
    Messages protocol:
    [message content length]![message type][message content]
    0. message from user
    1. Add online user
    2. Remove disconnected user

    """
    len_str = ""
    while (char := sock.recv(1).decode()) != "!":
        len_str += char
    msg_len = int(len_str)
    msg_type = sock.recv(1).decode()
    msg_content = sock.recv(msg_len).decode()
    if msg_type == 0:
        display_user_message(msg_content)
    elif msg_type == 1:
        add_online_user(msg_content)
    elif msg_type == 2:
        remove_online_user(msg_content)


def display_user_message(message):
    print(message)


def add_online_user(username):
    online_clients.append(username)


def remove_online_user(username):
    online_clients.remove(username)


def main():
    # Connect to the server
    client_socket = connect_to_server()

    # Send the username to the server and get the username
    username = input("Enter your username: ")
    send_username(client_socket, username)

    # Start the thread for receiving messages
    receive_thread = Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    # Function to send messages with the username
    send_message(client_socket, username)


if __name__ == "__main__":
    main()
