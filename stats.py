class Stats:
    def __init__(self, wins=0):
        self.wins = wins

    def __add__(self, other):
        return Stats(self.wins + other.wins)

    def __str__(self):
        return f"Wygrane: {self.wins}"