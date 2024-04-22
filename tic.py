import socket

def print_board(board):
    for row in board:
        print(" ".join(row))

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
        conn.sendall(" ".join([cell if cell != " " else "_" for cell in row]).encode() + b"\n")

def play_game(conn1, conn2):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        for conn in (conn1, conn2):
            conn.sendall("CURRENT_BOARD\n".encode())
            send_board(conn, board)

        current_conn = conn1 if current_player == "X" else conn2
        current_conn.sendall("YOUR_TURN\n".encode())
        move = current_conn.recv(1024).decode().split(",")
        row, col = int(move[0]), int(move[1])

        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = current_player

            if check_win(board, current_player):
                for conn in (conn1, conn2):
                    conn.sendall("WINNER\n".encode())
                    conn.sendall(current_player.encode())
                return

            if all(cell != " " for row in board for cell in row):
                for conn in (conn1, conn2):
                    conn.sendall("TIE\n".encode())
                return

            current_player = "O" if current_player == "X" else "X"
        else:
            current_conn.sendall("INVALID_MOVE\n".encode())

def handle_connection(conn, player_number):
    conn.sendall("Welcome, Player {}!\n".format(player_number).encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 5002

    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Waiting for players...")

    conn1, addr1 = server_socket.accept()
    print("Player 1 connected.")
    conn2, addr2 = server_socket.accept()
    print("Player 2 connected.")

    handle_connection(conn1, 1)
    handle_connection(conn2, 2)
    print("Starting game...")

    play_game(conn1, conn2)

    conn1.close()
    conn2.close()
    server_socket.close()

if __name__ == "__main__":
    main()
