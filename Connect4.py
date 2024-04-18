class GameState:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.win_count = 4
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.cur_player = 'X'