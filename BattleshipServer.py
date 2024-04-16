import socket
import threading

class BattleshipGame:
    def __init__(self):
        self.board_size = 10
        self.ships_count = 5
        self.board = self.create_board()
        self.player_boards = {}  # Store player boards and ship positions
        self.hits = []

    def create_board(self):
        return [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def set_player_board(self, player_socket, board_setup):
        # Parse the board setup data and store it for the player
        # Example implementation:
        # Store player's board setup as a list of tuples (x, y) representing ship positions (ships with dimensions of 1x1)
        try:
            ships = [tuple(map(int, ship.split(","))) for ship in board_setup.split(";")]
            if len(ships) != self.ships_count:
                raise ValueError("Invalid number of ships")
            self.player_boards[player_socket] = ships
        except Exception as e:
            print(f"Error setting up board for player: {e}")

    def get_player_board(self, player_socket):
        # Return the board for the specified player
        if player_socket in self.player_boards:
            return self.player_boards[player_socket]
        else:
            return []

    def is_valid_move(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_hit(self, x, y, player_socket):
        # Check if the specified position is occupied by a ship of the given player
        player_board = self.get_player_board(player_socket)
        return (x, y) in player_board

    def handle_move(self, x, y, player_socket):
        # Handle a move from a player
        try:
            if not self.is_valid_move(x, y):
                return False, "Invalid move, out of board bounds."
            
            if (x, y) in self.hits:
                return False, "Already guessed this position."

            if self.is_hit(x, y, player_socket):
                self.hits.append((x, y))
                self.board[y][x] = 'X'
                return True, "Hit!"
            else:
                self.hits.append((x, y))
                self.board[y][x] = '*'
                return False, "Miss!"
        except Exception as e:
            return False, f"Error handling move: {e}"

    def check_win(self, player_socket):
        # Check if all ships of the given player have been sunk
        player_board = self.get_player_board(player_socket)
        return all(coord in self.hits for coord in player_board)
        

class BattleshipServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.games = {}  # Store game instances for each pair of clients

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("Server is listening...")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address} has been established.")
            self.clients.append(client_socket)
            if len(self.clients) % 2 == 0:
                player1_socket = self.clients[-2]
                player2_socket = self.clients[-1]
                self.start_game(player1_socket, player2_socket)

    def start_game(self, player1_socket, player2_socket):
        game = BattleshipGame()
        self.games[player1_socket] = game
        self.games[player2_socket] = game
        self.setup_board(player1_socket, game)
        self.setup_board(player2_socket, game)
        self.send_board(player1_socket, game)
        self.send_board(player2_socket, game)
        threading.Thread(target=self.handle_client, args=(player1_socket,)).start()
        threading.Thread(target=self.handle_client, args=(player2_socket,)).start()

    def setup_board(self, player_socket, game):
        # Send a message to the player to set up their board and place their ships
        player_socket.send("setup".encode())
        # Receive the player's board setup and ship positions
        board_setup = player_socket.recv(1024).decode()
        game.set_player_board(player_socket, board_setup)

    def handle_client(self, client_socket):
        game = self.games[client_socket]
        opponent_socket = next(socket for socket in self.games if socket != client_socket)
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            elif data == "board":
                self.send_board(client_socket, game)
            else:
                x, y = map(int, data.split(","))
                hit, message = game.handle_move(x, y)
                if hit:
                    if game.check_win():
                        self.broadcast(opponent_socket, f"win,{message}")
                        self.broadcast(client_socket, "end")
                        break
                    else:
                        self.broadcast(opponent_socket, f"hit,{message}")
                else:
                    self.broadcast(opponent_socket, f"miss,{message}")
                self.send_board(client_socket, game)

    def send_board(self, client_socket, game):
        board_str = '\n'.join([' '.join(row) for row in game.get_player_board(client_socket)])
        client_socket.send(board_str.encode())

    def broadcast(self, client_socket, message):
        client_socket.send(message.encode())

