import socket

class Connect4Client:
    def __init__(self, client_sock):
        self.host = "127.0.0.1"
        self.port = 5000
        self.client_socket = client_sock

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to the game server.")
            return True
        except Exception as e:
            print(f"Unable to connect to the server: {e}")
            return False

    def play(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode()
                print(message)
                if "Enter your move" in message:
                    move = input("Enter your move (column number): ")
                    self.client_socket.send(move.encode())
                elif "Congratulations" in message or "Sorry" in message or "Tie game" in message:
                    print("Game Over.")
                    break
        except KeyboardInterrupt:
            print("Disconnected from the server.")
        finally:
            self.client_socket.close()
            print("Connection closed.")

if __name__ == "__main__":
    client = Connect4Client()
    if client.connect():
        client.play()
