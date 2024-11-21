import socket
from data_model import Status

class SocketClient:
    def __init__(self, host, port, timeout=0.5):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(0.5)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            raise e

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except Exception as e:
            raise e

    def receive_messages(self):
        messages = []
        try:
            data = self.client_socket.recv(1024).decode()
            messages.append(data)
        finally:
            self.client_socket.close()
        return messages

def request_for_response(host, port, request_text, timeout=0.5):
    response = ""
    try:
        client = SocketClient(host, port)
        client.connect()
        client.send_message(request_text)
        responses = client.receive_messages()
        response = ''.join(responses)
    except Exception as e:
        return "", Status.TLE if str(e) == "timed out" else Status.RE
    return response, Status.AC