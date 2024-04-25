import socket
import threading
import time

class BattleshipGame:
    def __init__(self):
        self.board_size = 10
        self.p1board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.p1OppBoard = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.p2board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.p2OppBoard = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.p1ships = []
        self.p2ships = []
        self.guessedp1 = set()
        self.guessedp2 = set()

   
    def place_ship(self, player, x, y):
        if player == 1:
            if (x, y) in self.p1ships:
                return False
            if x > self.board_size or y > self.board_size:
                return False
            self.p1ships.append((x, y))
            return True
        else:
            if (x, y) in self.p2ships:
                return False
            if x > self.board_size or y > self.board_size:
                return False
            self.p2ships.append((x, y))
            return True

    def check_hit(self, x, y, player):
        player = 1 - player
        if player == 1:
            if (x, y) in self.p2ships:
                self.p1OppBoard[x][y] = "X"
                self.guessedp1.add((x,y))
                return True
            else:
                self.p1OppBoard[x][y] = "O"
                return False
        if player == 0:
            if (x, y) in self.p1ships:
                self.p2OppBoard[x][y] = "X"
                self.guessedp2.add((x,y))
                return True
            else:
                self.p2OppBoard[x][y] = "O"
                return False

class BattleshipServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5585
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("Server is listening...")

        while len(self.players) < 2:
            client_socket, _ = self.server_socket.accept()
            print("Connection established with player", len(self.players) + 1)
            self.players.append(client_socket)

        self.setup_game()

    def setup_game(self):
        game = BattleshipGame()
        print("Starting Game...")
        self.setup_board(self.players[0], game, 1)
        self.setup_board(self.players[1], game, 2)

        print("Boards Created")
        while True:
            for i, client_socket in enumerate(self.players):
                opponent_socket = self.players[1 - i]
                #print(str(i))
                num1 = 5 - len(game.guessedp1) 
                num2 = 5 - len(game.guessedp2)
                time.sleep(1)
                if i == 0:
                    string = "Sink the other players ships (" + str(num1) + "):"
                else:
                    string = "Sink the other players ships (" + str(num2) + "):"
                client_socket.send(string.encode())
                string2 = "Wait for your turn"
                opponent_socket.send(string2.encode())
                time.sleep(1)
                board = self.format_board(i + 1, game)
                client_socket.send(board.encode())
                try:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        return
                    x, y = map(int, data.split(","))
                    if game.check_hit(x, y, i):
                        response = "Hit!"
                    else:
                        response = "Miss!"
                    if len(game.guessedp1) > 4:
                        response = "Player 1 Wins!"
                        client_socket.send(response.encode())
                        opponent_socket.send(response.encode())
                        print("Game Over, Player 1 Wins!")
                        return
                    if len(game.guessedp2) > 4:
                        response = "Player 2 Wins!"
                        client_socket.send(response.encode())
                        opponent_socket.send(response.encode())
                        print("Game Over, Player 2 Wins!")
                        return
                    time.sleep(1)
                    client_socket.send(response.encode())
                    response = "Opponent " + response
                    opponent_socket.send(response.encode())
                    time.sleep(1)
                except Exception as e:
                    print(f"Error handling client: {e}")
                    return

    def setup_board(self, client_socket, game, player):
        print("Getting ships from player " + str(player))
        client_socket.send("Place your ships. (5  remaining) Enter ship coordinates as 'x,y' (e.g., '0,0').".encode())
        num = 4
        for i in range(5):
            try:
                data = client_socket.recv(1024).decode()
                x, y = map(int, data.split(","))
                if not game.place_ship(player, x, y):
                    client_socket.send("Invalid placement. Try again.".encode())
                    continue
            except ValueError:
                client_socket.send("Invalid input. Use format 'x,y'.".encode())
                continue
            string = "Ship placed successfully. " + str(num) + " remaining"
            client_socket.send(string.encode())
            num -= 1

    def format_board(self, player, game):
        if player == 1:
            board = '\n'.join([' '.join(row) for row in game.p1OppBoard])
        else:
            board = '\n'.join([' '.join(row) for row in game.p2OppBoard])
        return board

if __name__ == "__main__":
    server = BattleshipServer()
    server.start()