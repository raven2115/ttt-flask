import time
from multiprocessing import Process

from server.Server import Server
from client.Client import Client

def start_server():
    serwer = Server()
    serwer.listen()

def start_client(name, port, symbol):
    time.sleep(1)
    client = Client(name, port, symbol)
    client.run()

if __name__ == "__main__":
    processes = [
        Process(target=start_server),
        Process(target=start_client, args=("Klient1", 5000, "X")),
        Process(target=start_client, args=("Klient2", 5001, "O")),
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()