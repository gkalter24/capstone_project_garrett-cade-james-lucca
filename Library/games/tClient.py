import socket

class TicTacToeClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to the Tic Tac Toe server.")
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
                    move = input("")
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
    client = TicTacToeClient("127.0.0.1", 5002)
    if client.connect():
        client.play()
