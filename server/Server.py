import socket

import threading
import json

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5002

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        self.currentPlayer = "X"
        self.winner = None

    def reset_game(self):
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        self.currentPlayer = "X"
        self.winner = None

        self.broadcast()

    def broadcast(self):
        data = {
            "board": self.board,
            "currentPlayer": self.currentPlayer,
            "winner": self.winner,
            "clients": len(self.clients)
        }

        packet = json.dumps(data).encode()

        for client in self.clients:
            try:
                client.send(packet)
            except:
                pass

    def win_check(self, board, symbol):
        if board[0][0]==board[0][1]==board[0][2]==symbol:
            return True
        if board[1][0]==board[1][1]==board[1][2]==symbol:
            return True
        if board[2][0]==board[2][1]==board[2][2]==symbol:
            return True
        if board[0][0]==board[1][0]==board[2][0]==symbol:
            return True
        if board[0][1]==board[1][1]==board[2][1]==symbol:
            return True
        if board[0][2]==board[1][2]==board[2][2]==symbol:
            return True
        if board[0][0]==board[1][1]==board[2][2]==symbol:
            return True
        if board[0][2]==board[1][1]==board[2][0]==symbol:
            return True
        c = 0
        for lista in board:
            for element in lista:
                if element == "O" or element == "X":
                    c += 1
        if c == 9:
            return "REMIS"
        return False

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break

                move = json.loads(data)
                if move.get("action") == "reset":
                    self.reset_game()
                    continue
                row = move["row"]
                col = move["col"]
                symbol = move["symbol"]

                if self.board[row][col] == "" and symbol == self.currentPlayer:
                    self.board[row][col] = symbol
                    result = self.win_check(self.board, symbol)
                    if result is True:
                        self.winner = symbol
                    elif result == "REMIS":
                        self.winner = "REMIS"
                    else:
                        self.currentPlayer = "O" if self.currentPlayer == "X" else "X"
                    self.broadcast()
            except:
                break
        conn.close()

    def listen(self):
        self.s.bind((self.host, self.port))
        self.s.listen(2)
        print(f"Server działa {self.host}:{self.port}")

        while True:
            conn, addr = self.s.accept()
            print(f"Połączono: {addr}")
            self.clients.append(conn)
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()
