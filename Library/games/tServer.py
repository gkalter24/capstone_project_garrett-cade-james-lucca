import socket

class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.games = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print("Tic Tac Toe server started. Waiting for players...")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Player {len(self.get_all_players()) + 1} connected.")
            if len(self.games) == 0 or len(self.games[-1].players) == 2:
                new_game = TicTacToeGame()
                self.games.append(new_game)
            else:
                new_game = self.games[-1]
            new_game.add_player(conn)

    def get_all_players(self):
        return [player for game in self.games for player in game.players]

    def close(self):
        self.server_socket.close()


class TicTacToeGame:
    def __init__(self):
        self.players = []
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def add_player(self, conn):
        self.players.append(conn)
        player_number = len(self.players)
        conn.sendall(f"Welcome, Player {player_number}!\n".encode())
        if player_number == 2:
            self.start_game()


    def start_game(self):
        self.players[0].sendall("You are Xs\n".encode())
        self.players[1].sendall("You are Os\n".encode())

        while True:
            self.send_board_to_players()
            current_conn = self.players[0] if self.current_player == 'X' else self.players[1]
            waiting_conn = self.players[1] if current_conn == self.players[0] else self.players[0]

            current_conn.sendall("Your turn...\n".encode())
            waiting_conn.sendall("Waiting for other player...\n".encode())

            move = self.get_valid_move(current_conn)
            row, col = map(int, move.split(","))
            self.board[row - 1][col - 1] = self.current_player

            if self.check_win(self.board, self.current_player):
                self.send_board_to_players()
                winning_player = "Player 1" if self.current_player != "O" else "Player 2"
                winning_message = f"Congratulations! {winning_player} won!\n"
                current_conn.sendall(winning_message.encode())
                waiting_conn.sendall(f"Sorry, {winning_player} won!\n".encode())
                break

            if all(cell != " " for row in self.board for cell in row):
                for conn in self.players:
                    conn.sendall("Tie game!\n".encode())
                break

            self.current_player = "O" if self.current_player == "X" else "X"

    def send_board_to_players(self):
        board_str = "CURRENT BOARD\n"
        for row in self.board:
            formatted_row = " ".join(cell if cell != " " else "_" for cell in row)
            board_str += formatted_row + "\n"
        for conn in self.players:
            conn.sendall(board_str.encode())

    def get_valid_move(self, conn):
        while True:
            conn.sendall("Enter your move (row,col): ".encode())
            move = conn.recv(1024).decode().strip()
            if ',' in move:
                row, col = map(int, move.split(","))
                if 1 <= row <= 3 and 1 <= col <= 3 and self.board[row - 1][col - 1] == " ":
                    return move
                else:
                    conn.sendall("Invalid move. Please try again.\n".encode())
            else:
                conn.sendall("Invalid input. Please enter row and column numbers separated by comma (e.g., '1,2').\n".encode())

    def check_win(self, board, mark):
        for i in range(3):
            if all(cell == mark for cell in board[i]) or all(board[j][i] == mark for j in range(3)):
                return True
        if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
            return True
        return False

if __name__ == "__main__":
    server = TicTacToeServer("127.0.0.1", 5002)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer closed.")
    finally:
        server.close()
