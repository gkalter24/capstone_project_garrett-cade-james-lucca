class GameState:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.win_count = 4
        self.board = [[' ' for i in range(self.cols)] for j in range(self.rows)]
        self.cur_player = 'X'
        self.moves = 0

    def print_instructions(self):
        print("Welcome to Connect Four!")
        print("In this two player game, both players will alternate turns placing their chips in the board.")
        print("The first player to place 4 consecutive pieces in a row, either horizontally, vertically, or diagonally, wins!")
        print("If the board is filled without any player satisfying the win condition, the game will end in a draw.")

    def print_game(self):
        for p in range((self.cols * 2) + 1):
            print('-', end='')
        print()
        for i in range(self.rows):
            for j in range(self.cols):
                print(f'|{self.board[i][j]}', end='')
            print('|')
            for k in range((self.cols * 2) + 1):
                print('-', end='')
            print()
        print(' '+' '.join(str(i) for i in range(self.cols)))

    @staticmethod
    def main():
            game = GameState()
            game.print_instructions()
            game.print_game()

if __name__ == "__main__":
    GameState.main()
