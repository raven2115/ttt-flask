from flask import Flask, render_template


class Client:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.app = Flask(self.name)
        self.setup_board()

    def setup_board(self):
        @self.app.route('/')
        def index():
            board = [
                ["", "", ""],
                ["", "", ""],
                ["", "", ""]
            ]
            return render_template("index.html", board=board)

    def run(self, debug = False):
        self.app.run(host="127.0.0.1", port=self.port,  threaded=True, processes=1, debug=debug)

if __name__ == '__main__':
    client = Client("Main", 5000)
    client.run(True)
