from games.Con4 import *
import socket
import threading 

def play_game(conn1, conn2):
    game = ConnectFour() 
    game.start_game(conn1, conn2)  

def handle_game_session(server_socket):
    while True:
        print("Waiting for players...")
        conn1, addr1 = server_socket.accept()
        print(f"Player 1 connected from {addr1}")
        
        conn2, addr2 = server_socket.accept()
        print(f"Player 2 connected from {addr2}")
        
        threading.Thread(target=play_game, args=(conn1, conn2)).start()

def main():
    host = '127.0.0.1'
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  
    print("Server started on port", port)

    handle_game_session(server_socket)

    server_socket.close()

if __name__ == "__main__":
    main()
