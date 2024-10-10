import socket


class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(0.5)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            raise e

    def receive_messages(self):
        messages = []
        try:
            data = self.client_socket.recv(1024).decode()
            messages.append(data)
            print(f"Received message: {data}")
        finally:
            self.client_socket.close()
        return messages
