from flask import Flask, render_template
import socket
import os

class Client:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.app = Flask(self.name, template_folder= os.path.dirname(os.path.abspath(__file__)) + "/templates")

        self.board = [
            ["", "5", ""],
            ["8", "R", ""],
            ["", "Q", ""]
        ]

        self.s = socket.socket()
        self.s.connect(("127.0.0.1", 5002))
        self.setup_board()

    def setup_board(self):
        @self.app.route('/')
        def index():
            return render_template("index.html", board=self.board)

        @self.app.route('/move', methods=['POST'])
        def move():
            print(f"DZIALA - {self.port}")
            return render_template("index.html", board=self.board)

    def run(self, debug=False):
        self.app.run(host="127.0.0.1", port=self.port, threaded=True, processes=1, debug=debug)

if __name__ == '__main__':
    client = Client("Main", 5000)
    client.run(True)
