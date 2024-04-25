import socket

def check_win(board, mark):
    for i in range(3):
        if all(cell == mark for cell in board[i]):
            return True
        if all(board[j][i] == mark for j in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False

def send_board(conn, board):
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

def play_game(conn1, conn2):
    try:
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "X"

        conn1.sendall("You are Xs\n".encode())
        conn2.sendall("You are Os\n".encode())

        while True:
            for conn in (conn1, conn2):
                conn.sendall("CURRENT BOARD\n".encode())
                send_board(conn, board)

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
                except Exception as e:
                    print("An error occurred while processing a move:", e)
                    return

            board[row][col] = current_player

            if check_win(board, current_player):
                winning_player = "Player 1" if current_player != "O" else "Player 2"
                winning_message = "Congratulations! You won!"
                current_conn.sendall(winning_message.encode())

                for conn in (conn1, conn2):
                    if conn != current_conn:
                        conn.sendall("You lost! {} got 3 in a row!\n".format(winning_player).encode())

                # Send the final board state to both players before closing the server
                for conn in (conn1, conn2):
                    conn.sendall("FINAL BOARD\n".encode())
                    send_board(conn, board)

                return

            if all(cell != " " for row in board for cell in row):
                for conn in (conn1, conn2):
                    conn.sendall("Tie game!\n".encode())

                # Send the final board state to both players before closing the server
                for conn in (conn1, conn2):
                    conn.sendall("FINAL BOARD\n".encode())
                    send_board(conn, board)

                return

            current_player = "O" if current_player == "X" else "X"
    except Exception as e:
        print("An error occurred during the game:", e)
        return


def handle_connection(conn, player_number, game_started):
    if game_started:
        conn.sendall("Game is full, try again later\n".encode())
        conn.close()
    else:
        instructions = "Welcome, Player {}!\nInstructions: When it's your turn, enter the row and column numbers separated by a comma (e.g., '1,2') to place your mark on the board.\n".format(player_number)
        conn.sendall(instructions.encode())


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 5000

    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Waiting for players...")
    print("Open 2 new terminals and type 'telnet 127.0.0.1 {}' to begin".format(port))

    conn1, addr1 = server_socket.accept()
    print("Player 1 connected.")
    conn2, addr2 = server_socket.accept()
    print("Player 2 connected.")

    game_started = False

    handle_connection(conn1, 1, game_started)
    handle_connection(conn2, 2, game_started)
    print("Starting game... Socket will not be listening for other players")

    game_started = True  # Set game_started to True after both players have connected

    play_game(conn1, conn2)

    conn1.close()
    conn2.close()
    server_socket.close()

if __name__ == "__main__":
    main()















