from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket


class Server:
    def __init__(self):
        self.host = None
        self.port = None

        self.connection = None

    def connect(self, host, port):
        self.host = host
        self.port = port

        # Connect to server.
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((self.host, self.port))

    def send(self, message):
        # Send message.
        message = message.encode('utf-8')
        self.connection.sendall(message)

        # Return response.
        response = self.connection.recv(1024)
        return response.decode()

    def disconnect(self):
        # Close connection.
        self.connection.close()
