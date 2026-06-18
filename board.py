class Board:
    def __init__(self):
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

    def reset(self):
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

    def __len__(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell != "":
                    count += 1
        return count