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
    print("Starting client:", client, "on port:", port)
    client1 = Client(client, port)
    client1.run()

if __name__ == "__main__":
    processes = [Process(target=start_server), Process(target=start_client, args=("Klient1", 5000)), Process(target=start_client, args=("Klient2", 5001)),]

    for p in processes:
        p.start()

    for p in processes:
        p.join()