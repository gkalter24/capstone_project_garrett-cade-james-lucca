import socket
from games.BattleshipClient import BattleshipClient
from games.Con4 import *
from games.Connect4Client import *

def main():
    host = '127.0.0.1'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to the game server.")

        try:
            while True:
                    message = sock.recv(1024).decode()  
                    print(message)
                    message = sock.recv(1024).decode()  
                    print(message)
                    if "Waiting" in message:
                        message2 = sock.recv(1024).decode()  
                        print(message2)
                    game = input("Select a game (1,2,3,4): ")
                    sock.send(game.encode())
                    gameNum = int(game)
                    message = sock.recv(1024).decode()  
                    print(message)
                    if gameNum == 1:
                        playBattleship(sock)
                        return
                    if gameNum == 2:
                        playConnect4(sock)
                        return

        except KeyboardInterrupt:
            print("Game ended.")
            return
        
def playBattleship(sock2):
     client = BattleshipClient(client_sock = sock2)
     client.setup()

def playConnect4(sock3):
    client = Connect4Client(sock3)
    client.play()

if __name__ == "__main__":
    main()
