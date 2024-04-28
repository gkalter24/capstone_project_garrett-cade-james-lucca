import socket
import threading
from games.Con4 import *
from games.Connect4Client import * 
from games.BattleshipServer import BattleshipGame
from games.BattleshipServer import BattleshipServer

game_options = {
    '1': BattleshipServer,
    '2': ConnectFourServer
}

def handle_two_player_session(conn1, conn2, sock3):
    try:
        while True:
            conn1.sendall("Choose a game:\n1. Battleship\n2. Connect4\n3. Tic Tac Toe\n4. Hangman\n Or type 'exit' to quit: ".encode())
            conn2.sendall("Waiting for player 1 to choose a game...\n".encode())
            
            choice1 = conn1.recv(1024).decode().strip()
            if not choice1:
                conn2.sendall("Player 1 disconnected".encode())
                print("Player 1 disconnected, restarting library...")
                restartLibrary(sock3)
                return
            print(f"Debug: Player 1 choice received: {choice1}")  
            if choice1.lower() == 'exit':
                break

            conn2.sendall(f"Player 1 chose {choice1}. Please confirm by typing '{choice1}' or choose another game.".encode())
            choice2 = conn2.recv(1024).decode().strip()
            if not choice2:
                conn1.sendall("Player 2 disconnected".encode())
                print("Player 2 disconnected, restarting library...")
                restartLibrary(sock3)
                return
            print(f"Debug: Player 2 choice received: {choice2}") 
            if choice2.lower() == 'exit':
                break

            if choice1 == choice2 and choice1 in game_options:
                conn1.sendall("Game starting. Wait for your turn...\n".encode())
                conn2.sendall("Game starting. Wait for your turn...\n".encode())
                print("Starting game...")
                players = [conn1, conn2]
                if choice1 == '1':
                    startBattleshipServer(sock3, players)  
                    return
                if choice1 == '2':
                    startConnect4Server(sock3, players)
            else:
                conn1.sendall("Failed to agree on a game. Please try again.\n".encode())
                conn2.sendall("Failed to agree on a game. Please try again.\n".encode())
    except socket.error:
        print("Connection Error")
        restartLibrary(sock3)
        return
    

def startBattleshipServer(sock3, playerArray):
    print("Starting Battleship Game")
    server = BattleshipServer(client_sock = sock3, players = playerArray)
    server.setup_game()
    restartLibrary(sock3)
    return

def startConnect4Server(sock, playerArray):
    print("Starting Connect4 Game")
    server = ConnectFourServer(server_sock = sock, players = playerArray)
    server.play_game(playerArray[0], playerArray[1])

def main():
    host = '127.0.0.1'  
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    try:
        while True:
            conn1, addr1 = server_socket.accept()
            print(f"Player 1 connected from {addr1}")
            conn1.sendall("Connected to server. Waiting for another player...\n".encode())

            conn2, addr2 = server_socket.accept()
            print(f"Player 2 connected from {addr2}")
            conn2.sendall("Connected to server. Player 1 is ready.\n".encode())

            handle_two_player_session(conn1, conn2, server_socket)
            return

    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        #print("Finally")
        server_socket.close()

def restartLibrary(server_socket):
    print("Waiting for new connections...")

    try:
        while True:
            try:
                conn1, addr1 = server_socket.accept()
                print(f"Player 1 connected from {addr1}")
                conn1.sendall("Connected to server. Waiting for another player...\n".encode())

                conn2, addr2 = server_socket.accept()
                print(f"Player 2 connected from {addr2}")
                conn2.sendall("Connected to server. Player 1 is ready.\n".encode())

                handle_two_player_session(conn1, conn2, server_socket)
            except socket.error:
                print("Connection Error")
                return

    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        #print("Finally")
        server_socket.close()

if __name__ == "__main__":
    main()
