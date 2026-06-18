from abc import ABC, abstractmethod
import json
import socket


class Network(ABC):
    def __init__(self, name):
        self.name = name
        self.connected = False

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self):
        self.connected = False

    def send_json(self, sock, data):
        try:
            packet = json.dumps(data).encode()
            sock.send(packet)
        except Exception as e:
            self.log(f"Blad wysylania: {e}")

    def receive_json(self, sock, size=1024):
        try:
            data = sock.recv(size).decode()
            if not data:
                return None
            return json.loads(data)
        except:
            return None

    def log(self, message):
        print(f"[{self.name}] {message}")

    def info(self):
        return f"Klient: {self.name}"