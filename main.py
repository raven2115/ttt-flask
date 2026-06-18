import time
from multiprocessing import Process

from server.server import Server
from client.client import Client

def start_server():
    server = Server()
    server.listen()

def start_client(name, port, symbol):
    time.sleep(1)

    client = Client(
        name=name,
        port=port,
        symbol=symbol
    )
    client.run()

if __name__ == "__main__":
    processes = [
        Process(target=start_server),
        Process(target=start_client, args=("Klient1", 5000, "X")),
        Process(target=start_client, args=("Klient2", 5001, "O"))
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()