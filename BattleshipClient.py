import socket
import sys


class BattleshipClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to server.")
        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit()

    def start(self):
        self.connect()
        while True:
            data = self.client_socket.recv(1024).decode()
            if data == "setup":
                self.setup_board()
                self.send_board_setup()
            elif data == "end":
                print("Game over.")
                sys.exit()
            else:
                self.print_board()
                self.get_player_move()

    def setup_board(self):
        # Implement player board setup logic
        pass

    def send_board_setup(self):
        # Implement sending the player's board setup to the server
        pass

    def print_board(self):
        try:
            board = self.client_socket.recv(1024).decode()
            print("Your Board:")
            print(board)
        except Exception as e:
            print(f"Error printing board: {e}")

    def get_player_move(self):
        move = input("Enter your move (x,y): ")
        self.send_move(move)

    def send_move(self, move):
        try:
            self.client_socket.send(move.encode())
        except Exception as e:
            print(f"Error sending move: {e}")