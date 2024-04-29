import socket
import sys
from termios import TCIFLUSH, tcflush
from games.BattleshipClient import BattleshipClient
from games.Con4 import *
from games.Connect4Client import *
from games.tClient import *

def main():
    host = '127.0.0.1'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to the game server.")
        except:
            print("Server full.")
            return

        try:
            while True:
                    flag = True
                    message = sock.recv(1024).decode()  
                    print(message)
                    if "Connected" in message:
                        message = sock.recv(1024).decode()  
                        print(message)
                    if "Waiting" in message:
                        message2 = sock.recv(1024).decode()  
                        print(message2)
                        if "disconnected" in message2:
                            return
                    while flag:
                        tcflush(sys.stdin, TCIFLUSH)
                        game = input("Select a game (1,2,3,4): ")
                        try:
                            gameNum = int(game)
                            if gameNum in [1,2,3,4]:
                                flag = False
                            else:
                                print("Invalid input, try again")
                        except:
                            print("Invalid input, try again")
                    sock.send(game.encode())
                    gameNum = int(game)
                    message = sock.recv(1024).decode()  
                    print(message)
                    if "Failed" in message:
                        if "Choose" in message:
                            print("here")
                        gameNum = 0
                    if "disconnected" in message:
                            return
                    if gameNum == 1:
                        playBattleship(sock)
                        return
                    if gameNum == 2:
                        playConnect4(sock)
                        return
                    if gameNum == 3:
                        playTicTacToe(sock)
                        return

        except KeyboardInterrupt:
            print("Game ended.")
            return
        
def playBattleship(sock2):
     client = BattleshipClient(client_sock = sock2)
     client.setup()

def playConnect4(sock):
    client = Connect4Client(client_sock = sock)
    client.play()

def playTicTacToe(sock):
    client = TicTacToeClient(client_sock = sock)
    client.play()

if __name__ == "__main__":
    main()
