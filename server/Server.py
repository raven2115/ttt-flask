import socket
import threading
import json
from network import Network
from board import Board
from stats import Stats


class Server(Network):

    def __init__(self):
        super().__init__("Server")
        self.__host = "127.0.0.1"
        self.__port = 5002
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = []

        self.board = Board()

        self.currentPlayer = "X"
        self.winner = None

        self.statsX = Stats()
        self.statsO = Stats()

    def __del__(self):
        try:
            self.s.close()
        except:
            pass

    def connect(self):
        self.connected = True
        self.log("Server connected")

    def info(self):
        return "Serwer"

    def reset_game(self):
        self.board.reset()

        self.currentPlayer = "X"
        self.winner = None

        self.broadcast()

    def broadcast(self):
        data = {
        "board": self.board.board,
        "currentPlayer": self.currentPlayer,
        "winner": self.winner,
        "clients": len(self.clients),
        "winsX": self.statsX.wins,
        "winsO": self.statsO.wins
        }

        disconnected = []

        for client in self.clients:
            try:
                self.send_json(client, data)
            except:
                disconnected.append(client)

        for client in disconnected:
            self.clients.remove(client)

    def win_check(self, board, symbol):
        if board[0][0] == board[0][1] == board[0][2] == symbol:
            return True
        if board[1][0] == board[1][1] == board[1][2] == symbol:
            return True
        if board[2][0] == board[2][1] == board[2][2] == symbol:
            return True
        if board[0][0] == board[1][0] == board[2][0] == symbol:
            return True
        if board[0][1] == board[1][1] == board[2][1] == symbol:
            return True
        if board[0][2] == board[1][2] == board[2][2] == symbol:
            return True
        if board[0][0] == board[1][1] == board[2][2] == symbol:
            return True
        if board[0][2] == board[1][1] == board[2][0] == symbol:
            return True

        if len(self.board) == 9:
            return "REMIS"

        return False

    def handle_client(self, conn):
        while True:
            try:
                move = self.receive_json(conn)
                if move is None:
                    break

                if move.get("action") == "reset":
                    self.reset_game()
                    continue

                row = move["row"]
                col = move["col"]
                symbol = move["symbol"]

                if self.board.board[row][col] == "" and symbol == self.currentPlayer:
                    self.board.board[row][col] = symbol
                    result = self.win_check(self.board.board, symbol)
                    if result is True:
                        self.winner = symbol
                        if symbol == "X":
                            self.statsX = self.statsX + Stats(1)
                        if symbol == "O":
                            self.statsO = self.statsO + Stats(1)
                        print(self.statsX)
                        print(self.statsO)
                    elif result == "REMIS":
                        self.winner = "REMIS"
                    else:
                        if self.currentPlayer == "X":
                            self.currentPlayer = "O"
                        else:
                            self.currentPlayer = "X"
                    self.broadcast()
            except:
                break
        conn.close()

    def listen(self):
        self.connect()
        self.s.bind((self.__host, self.__port))
        self.s.listen(2)
        self.log(f"Server dziala {self.__host}:{self.__port}")
        while True:
            conn, addr = self.s.accept()
            self.log(f"Polaczono: {addr}")
            self.clients.append(conn)
            t = threading.Thread(target=self.handle_client,args=(conn,))
            t.start()
