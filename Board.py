

class Board:

    def __init__(self):
        self.board = list()
        self.start_fields = [0, 10, 20, 30]
        self.target_fields = [39, 9, 19, 29]
        self.homes = [list()]*4

