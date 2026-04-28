from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    return render_template("index.html", board=board)

if __name__ == '__main__':
    app.run(debug=True)