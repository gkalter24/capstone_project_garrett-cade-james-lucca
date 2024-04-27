import socket

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'

    def send_board(self, conn):
        conn.sendall("Current Board:\n".encode())
        for row in self.board:
            formatted_row = " | ".join(row)
            conn.sendall(f"| {formatted_row} |\n".encode())
        conn.sendall("  0   1   2   3   4   5   6  \n".encode())

    def check_win(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] 
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] == self.current_player:  
                    for dx, dy in directions:
                        count = 1  
                        for step in range(1, 4):  
                            nx, ny = x + dx * step, y + dy * step
                            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.board[nx][ny] == self.current_player:
                                count += 1
                            else:
                                break 
                        if count == 4:  
                            return True
        return False

    def make_move(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] == ' ':
            for r in range(self.rows-1, -1, -1):
                if self.board[r][col] == ' ':
                    self.board[r][col] = self.current_player
                    return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def start_game(self, conn1, conn2):
        conn1.sendall("You are Xs\n".encode())
        conn2.sendall("You are Os\n".encode())

        connections = [conn1, conn2]
        while True:
            try:    
                self.send_board(conn1)
                self.send_board(conn2)

                current_conn = conn1 if self.current_player == 'X' else conn2
                waiting_conn = conn2 if current_conn == conn1 else conn1

                current_conn.sendall("Your turn...\n".encode())
                waiting_conn.sendall("Waiting for other player...\n".encode())

                valid_move = False
                while not valid_move:
                    current_conn.sendall("Enter your move (col): ".encode())
                    move = current_conn.recv(1024).decode().strip()
                    try:
                        col = int(move)
                        if 0 <= col < self.cols and self.board[0][col] == ' ':
                            if self.make_move(0, col):
                                valid_move = True
                            else:
                                current_conn.sendall("Invalid move. Try again.\n".encode())
                        else:
                            current_conn.sendall("Invalid column. Please choose a valid column between 0 and 6.\n".encode())
                    except ValueError:
                        current_conn.sendall("Invalid input. Please enter a numeric column number.\n".encode())

                if self.check_win():
                    self.send_board(conn1)
                    self.send_board(conn2)
                    winner_message = "Congratulations! You won, you got 4 in a row!\n"
                    current_conn.sendall(winner_message.encode())
                    waiting_conn.sendall("Sorry, you lost!\n".encode())
                    break
                if all(cell != ' ' for row in self.board for cell in row):
                    for conn in connections:
                        conn.sendall("Tie game!\n".encode())
                    break

                self.switch_player()

            except (BrokenPipeError, ConnectionResetError, socket.error) as e:
                print(f"Connection error: {e}")
                for conn in connections:
                    conn.close()
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                for conn in connections:
                    conn.close()
                break

