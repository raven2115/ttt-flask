import socket

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5002
        self.s = socket.socket()

    def listen(self):
        self.s.bind((self.host, self.port))
        print(f"[*] serwer dziala na {self.host}:{self.port}")
        self.s.listen(2)
        conn, addr = self.s.accept()
        print(f"[*] {addr}")

