import socket
import sys

# Function to print the Tic Tac Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Function to check if any player has won
def check_win(board, mark):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(cell == mark for cell in board[i]):
            return True
        if all(board[j][i] == mark for j in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False

# Function to handle the main game logic
def play_game(conn1, conn2):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        # Send current state of the board to both players
        for conn in (conn1, conn2):
            conn.sendall("CURRENT_BOARD".encode())
            conn.sendall(str(board).encode())

        # Receive move from the current player
        current_conn = conn1 if current_player == "X" else conn2
        current_conn.sendall("YOUR_TURN".encode())
        move = current_conn.recv(1024).decode().split(",")
        row, col = int(move[0]), int(move[1])

        # Check if the move is valid
        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = current_player

            # Check if the current player wins
            if check_win(board, current_player):
                for conn in (conn1, conn2):
                    conn.sendall("WINNER".encode())
                    conn.sendall(current_player.encode())
                return

            # Check for a tie
            if all(cell != " " for row in board for cell in row):
                for conn in (conn1, conn2):
                    conn.sendall("TIE".encode())
                return

            # Switch to the other player
            current_player = "O" if current_player == "X" else "X"
        else:
            current_conn.sendall("INVALID_MOVE".encode())

# Function to handle each player's connection
def handle_connection(conn, player_number):
    conn.sendall("Welcome, Player {}!".format(player_number).encode())
    while True:
        # Receive the command from the player
        command = conn.recv(1024).decode()

        # Start the game when both players are connected
        if command == "START_GAME":
            return

# Main function to handle server setup and connections
def main():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 60005

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(2)
    print("Waiting for players...")

    # Accept the connections from two players
    conn1, addr1 = server_socket.accept()
    print("Player 1 connected.")
    conn2, addr2 = server_socket.accept()
    print("Player 2 connected.")

    # Start the game
    handle_connection(conn1, 1)
    handle_connection(conn2, 2)
    print("Starting game...")

    # Play the game
    play_game(conn1, conn2)

    # Close the connections and the server socket
    conn1.close()
    conn2.close()
    server_socket.close()

if __name__ == "__main__":
    main()
