from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import socket
import os
import threading
import json

from network import Network

class Client(Network):
    def __init__(self, name, port, symbol):
        super().__init__(name)
        self.port = port
        self.symbol = symbol

        self.currentPlayer = "X"
        self.winner = None
        self.clientsCount = 0

        self.winsX = 0
        self.winsO = 0

        self.app = Flask(self.name, template_folder=os.path.dirname(os.path.abspath(__file__)) + "/templates")

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 5002))
        threading.Thread(target=self.receive_board, daemon=True).start()

        self.setup_board()

    def __del__(self):
        try:
            self.disconnect()
            self.s.close()
        except:
            pass

    def connect(self):
        self.connected = True
        self.log("Client connected")

    def info(self):
        return f"Client {self.name}"

    def receive_board(self):
        while True:
            state = self.receive_json(self.s)

            if state is None:
                break

            self.winsX = state["winsX"]
            self.winsO = state["winsO"]
            self.board = state["board"]
            self.currentPlayer = state["currentPlayer"]
            self.winner = state["winner"]
            self.clientsCount = state["clients"]

    def setup_board(self):
        @self.app.route('/')
        def index():
            return render_template(
            "index.html",
            board=self.board,
            currentPlayer=self.currentPlayer,
            winner=self.winner,
            clients=self.clientsCount,
            symbol=self.symbol,
            winsX=self.winsX,
            winsO=self.winsO
        )

        @self.app.route('/move', methods=['POST'])
        def move():
            if self.winner:
                return redirect('/')
            move = request.form['move']
            row, col = map(int, move.split(","))
            data = {
                "row": row,
                "col": col,
                "symbol": self.symbol
            }
            self.send_json(self.s, data)
            return redirect('/')

        @self.app.route('/reset', methods=['POST'])
        def reset():
            self.send_json(self.s, {"action": "reset"})
            return redirect('/')

    def run(self, debug=False):
        self.connect()
        self.app.run(
            host="127.0.0.1",
            port=self.port,
            threaded=True,
            debug=debug
        )
