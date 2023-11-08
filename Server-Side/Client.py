import socket


class Client:
    def __init__(self, socket, name, address):
        self.socket = socket
        self.name = name
        self.address = address
        # Any future properties can also be added here

    def send_message(self, message):
        """
        Sends a message to the client.
        """
        self.socket.sendall(message.encode('utf-8'))

    def receive_message(self):
        """
        Receives a message from the client.
        """
        return self.socket.recv(1024).decode('utf-8')

    def disconnect(self):
        """
        Disconnect the client from the server.
        """
        print(f"Client {self.name} at {self.address} disconnected.")
        self.socket.close()

    # You can add additional methods relevant to client behavior here.
    # For example, methods for handling client status (active, idle, etc.),
    # serialization for storing client information, etc.
