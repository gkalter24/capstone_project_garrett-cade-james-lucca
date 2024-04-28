import socket
from games.BattleshipClient import BattleshipClient
def main():
    host = '127.0.0.1'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to the game server.")

        try:
            while True:
                    flag = True
                    message = sock.recv(1024).decode()  
                    print(message)
                    message = sock.recv(1024).decode()  
                    print(message)
                    if "Waiting" in message:
                        message2 = sock.recv(1024).decode()  
                        print(message2)
                        if "disconnected" in message2:
                            return
                    while flag:
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
                    if "disconnected" in message:
                            return
                    if gameNum == 1:
                        playBattleship(sock)
                        return

        except KeyboardInterrupt:
            print("Game ended.")
            return
        
def playBattleship(sock2):
     client = BattleshipClient(client_sock = sock2)
     client.setup()



if __name__ == "__main__":
    main()
