import os
import time
from multiprocessing import Process

from server.Server import Server
from client.Client import Client

def start_server():
    print("Starting server")
    server = Server()
    server.listen()

def start_client(client, port):
    time.sleep(1)
    os.chdir('client')
    client1 = Client(client, port)
    client1.run()
    print("Starting client: " + str(client) + " on port: " + str(port))

if __name__ == "__main__":
    processes = []
    processes.append(Process(target=start_server, args=()))
    processes.append(Process(target=start_client, args=("Klient1", 5000)))
    processes.append(Process(target=start_client, args=("Klient2", 5001)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()