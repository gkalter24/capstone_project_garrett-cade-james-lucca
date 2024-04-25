import socket
import threading 

class GameState:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.win_count = 4
        self.board = [[' ' for i in range(self.cols)] for j in range(self.rows)]
        self.cur_player = 'X'
        self.moves = 0

    def print_instructions(self):
        return (
        "Welcome to Connect Four!\n"
        "In this two player game, both players will alternate turns placing their chips in the board.\n"
        "The first player to place 4 consecutive pieces in a row, either horizontally, vertically, or diagonally, wins!\n"
        "If the board is filled without any player satisfying the win condition, the game will end in a draw."
    )


    def print_game(self):
        game_str = ''
        for p in range((self.cols * 2) + 1):
            game_str += '-'
        game_str += '\n'
        for i in range(self.rows):
            for j in range(self.cols):
                game_str += f'|{self.board[i][j]}'
            game_str += '|\n'
            for k in range((self.cols * 2) + 1):
                game_str += '-'
            game_str += '\n'
        game_str += ' ' + ' '.join(str(i) for i in range(self.cols)) + '\n'
        return game_str

    def check_full(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == ' ':
                    return False
        return True

    def make_move(self, col):
        if col < 0 or col >= self.cols:
            print("Invalid input, try again!")
            return False
        for i in range(self.rows - 1, -1, -1):
            if self.board[i][col] == ' ':
                self.board[i][col] = self.cur_player
                self.moves += 1
                if self.check_winner(i, col):
                    return True
                break
        else:
            print("Column is full! Try again")
        return False

    def switch_player(self):
        self.cur_player = 'O' if self.cur_player == 'X' else 'X'

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dirX, dirY in directions:
            count = 1
            for j in [-1, 1]:
                newX, newY = row + dirX * j, col + dirY * j
                while 0 <= newX < self.rows and 0 <= newY < self.cols and self.board[newX][newY] == self.cur_player:
                    count += 1
                    if count == self.win_count:
                        return True
                    newX += dirX * j
                    newY += dirY * j
        return False

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8001))
    server_socket.listen(2)
    print("Server started. Waiting for players to connect...")

    clients = []
    while len(clients) < 2:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Player connected from {addr}")

    game = GameState()
    player_turn = 0

    for client in clients:
        client.send(game.print_instructions().encode())
        client.send(game.print_game().encode())

    game_over = False
    while not game_over:
        current_player = clients[player_turn]
        move = int(current_player.recv(1024).decode())
        valid_move, message = game.make_move(move)
        if valid_move:
            if message:  
                game_over = True
                for client in clients:
                    client.send((game.print_game() + "\n" + message).encode())
            else: 
                player_turn = 1 - player_turn
                for client in clients:
                    client.send(game.print_game().encode())
        else:
            current_player.send(message.encode())  

    for client in clients:
        client.close()
    server_socket.close()


threading.Thread(target=start_server).start()