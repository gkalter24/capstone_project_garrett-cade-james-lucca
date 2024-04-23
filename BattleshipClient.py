import socket

class BattleshipClient:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5567
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to server.")

    def setup(self):
        message = self.client_socket.recv(1024).decode()
        print(message)
        count = 0
        while True:
            try:
                move = input("Enter your move (x,y): ")
                self.client_socket.send(move.encode())
                response = self.client_socket.recv(1024).decode()
                print(response)
                if "Ship placed successfully." in response:
                    count += 1
                if count > 4:
                    self.play()
                    break
            except KeyboardInterrupt:
                print("Game ended.")
                break

    def play(self):
        print("Ready to Start")
        
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
                move = input("Enter your move (x,y): ")
                self.client_socket.send(move.encode())
                response = self.client_socket.recv(1024).decode()
                print(response)
            except KeyboardInterrupt:
                print("Game ended.")
                break

if __name__ == "__main__":
    client = BattleshipClient()
    client.setup()