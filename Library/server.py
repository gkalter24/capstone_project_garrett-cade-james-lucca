import socket
import threading
from games.Con4 import ConnectFour 

game_options = {
    '1': ConnectFour
}

def handle_two_player_session(conn1, conn2):
    try:
        while True:
            conn1.sendall("Choose a game:\n1. Connect Four\nOr type 'exit' to quit: ".encode())
            conn2.sendall("Waiting for player 1 to choose a game...\n".encode())

            choice1 = conn1.recv(1024).decode().strip()
            print(f"Debug: Player 1 choice received: {choice1}")  
            if choice1.lower() == 'exit':
                break

            conn2.sendall(f"Player 1 chose {choice1}. Please confirm by typing '{choice1}' or choose another game.".encode())
            choice2 = conn2.recv(1024).decode().strip()
            print(f"Debug: Player 2 choice received: {choice2}") 
            if choice2.lower() == 'exit':
                break

            if choice1 == choice2 and choice1 in game_options:
                game = game_options[choice1]()
                game.start_game(conn1, conn2)  
            else:
                conn1.sendall("Failed to agree on a game. Please try again.\n".encode())
                conn2.sendall("Failed to agree on a game. Please try again.\n".encode())

    finally:
        conn1.close()
        conn2.close()
        print("Session ended with both players.")

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

            threading.Thread(target=handle_two_player_session, args=(conn1, conn2)).start()

    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
