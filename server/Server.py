import socket
import threading
import json

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5002
        self.s = socket.socket()

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.currentPlayer = "X"

    def boardControl(self, conn):
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            board = json.loads(data)
            print(board)

    def listen(self):
        self.s.bind((self.host, self.port))
        print(f"[*] serwer dziala na {self.host}:{self.port}")
        self.s.listen(2)
        conn, addr = self.s.accept()
        print(f"[*] {addr}")

        t = threading.Thread(target=self.boardControl, args=(conn,))
        t.start()
        t.join()

server = Server()