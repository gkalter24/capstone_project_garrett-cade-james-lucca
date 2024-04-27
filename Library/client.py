import socket

def main():
    host = '127.0.0.1'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Connected to the game server.")

        try:
            while True:
                server_message = ""
                while True:
                    part = sock.recv(1024).decode()
                    server_message += part
                    if len(part) < 1024:  
                        break

                if "Your turn" in server_message:
                    print(server_message)
                    move = input("Enter your move: ")
                    sock.sendall(move.encode())
                elif "won" in server_message or "Tie game" in server_message or "lost" in server_message:
                    print(server_message)
                    break
                elif "Choose a game:" in server_message:
                    print(server_message)
                    game_choice = input("Select a game by entering the number: ")
                    sock.sendall(game_choice.encode())
                elif "Waiting for" in server_message:
                    print(server_message)
                else:
                    print(server_message)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Game session ended.")

if __name__ == "__main__":
    main()
