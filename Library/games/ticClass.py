import socket

class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.game_started = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print("Waiting for players...")
        print(f"Open 2 new terminals and type 'telnet {self.host} {self.port}' to begin")

        while len(self.connections) < 2:
            conn, addr = self.server_socket.accept()
            print(f"Player {len(self.connections) + 1} connected.")
            self.connections.append(conn)

            if len(self.connections) == 2:
                self.start_game()

    def handle_connection(self, conn, player_number):
        if self.game_started:
            conn.sendall("Game is full, try again later\n".encode())
            conn.close()
        else:
            instructions = f"Welcome, Player {player_number}!\nInstructions: When it's your turn, enter the row and column numbers separated by a comma (e.g., '1,2') to place your mark on the board.\n"
            conn.sendall(instructions.encode())

    def start_game(self):
        conn1, conn2 = self.connections

        self.handle_connection(conn1, 1)
        self.handle_connection(conn2, 2)
        print("Starting game... Socket will not be listening for other players")
        self.game_started = True

        self.play_game(conn1, conn2)

        conn1.close()
        conn2.close()
        self.server_socket.close()

    def play_game(self, conn1, conn2):
        try:
            board = [[" " for _ in range(3)] for _ in range(3)]
            current_player = "X"

            conn1.sendall("You are Xs\n".encode())
            conn2.sendall("You are Os\n".encode())

            while True:
                for conn in (conn1, conn2):
                    conn.sendall("CURRENT BOARD\n".encode())
                    self.send_board(conn, board)

                if current_player == "X":
                    current_conn = conn1
                    waiting_conn = conn2
                else:
                    current_conn = conn2
                    waiting_conn = conn1

                current_conn.sendall("Your turn...\n".encode())
                waiting_conn.sendall("Waiting for other player...\n".encode())

                valid_move = False
                while not valid_move:
                    try:
                        current_conn.sendall("Enter your move (row,col): ".encode())
                        move = current_conn.recv(1024).decode().strip()
                        if ',' in move:
                            row, col = map(int, move.split(","))
                            row -= 1
                            col -= 1
                            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
                                valid_move = True
                            else:
                                current_conn.sendall("Invalid move. Please try again.\n".encode())
                        else:
                            current_conn.sendall("Invalid input. Please enter row and column numbers separated by comma (e.g., '1,2').\n".encode())
                    except BrokenPipeError:
                        print("Player's connection was unexpectedly closed.")
                    except Exception as e:
                        print("An error occurred while processing a move:", e)
                        return

                board[row][col] = current_player

                if self.check_win(board, current_player):
                    winning_player = "Player 1" if current_player != "O" else "Player 2"
                    winning_message = "Congratulations! You won!"
                    current_conn.sendall(winning_message.encode())

                    for conn in (conn1, conn2):
                        if conn != current_conn:
                            conn.sendall("You lost! {} got 3 in a row!\n".format(winning_player).encode())

                    # Send the final board state to both players before closing the server
                    for conn in (conn1, conn2):
                        conn.sendall("FINAL BOARD\n".encode())
                        self.send_board(conn, board)

                    return

                if all(cell != " " for row in board for cell in row):
                    for conn in (conn1, conn2):
                        conn.sendall("Tie game!\n".encode())

                    # Send the final board state to both players before closing the server
                    for conn in (conn1, conn2):
                        conn.sendall("FINAL BOARD\n".encode())
                        self.send_board(conn, board)

                    return

                current_player = "O" if current_player == "X" else "X"

        except (ConnectionResetError, NameError):
            print("Player disconnected unexpectedly.")
            return
        except Exception as e:
            print("An error occurred during the game:", e)
            return

    def check_win(self, board, mark):
        for i in range(3):
            if all(cell == mark for cell in board[i]):
                return True
            if all(board[j][i] == mark for j in range(3)):
                return True
        if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
            return True
        return False

    def send_board(self, conn, board):
        for row in board:
            formatted_row = []
            for cell in row:
                if cell == " ":
                    formatted_row.append("_")
                else:
                    formatted_row.append(cell)

            joined_row = " ".join(formatted_row)
            joined_row += "\n"

            encoded_row = joined_row.encode()
            conn.sendall(encoded_row)

if __name__ == "__main__":
    server = TicTacToeServer("127.0.0.1", 5000)
    server.start()
