from flask import Flask, render_template, request, redirect
import socket
import os
import threading
import json

class Client:
    def __init__(self, name, port, symbol):
        self.name = name
        self.port = port
        self.symbol = symbol

        self.app = Flask(
            self.name,
            template_folder=os.path.dirname(os.path.abspath(__file__)) + "/templates"
        )

        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 5002))

        threading.Thread(target=self.receive_board, daemon=True).start()
        self.setup_board()

    def receive_board(self):
        while True:
            try:
                data = self.s.recv(1024).decode()
                if data:
                    self.board = json.loads(data)
                    print("Plansza (client):")
                    print(self.board)
            except:
                break

    def setup_board(self):

        @self.app.route('/')
        def index():
            return render_template("index.html", board=self.board)

        @self.app.route('/move', methods=['POST'])
        def move():
            move = request.form['move']
            row, col = map(int, move.split(","))

            data = {
                "row": row,
                "col": col,
                "symbol": self.symbol
            }

            self.s.send(json.dumps(data).encode())
            return redirect('/')

    def run(self, debug=False):
        self.app.run(
            host="127.0.0.1",
            port=self.port,
            threaded=True,
            debug=debug
        )
