import socket
import time
from games.hangpeople import *

class player:
    def __init__(self):
        self.guesses = set()
        self.word = ""
        self.opp_guess = ""
        self.person = 0

class hangpersonGame:
    def __init__(self, p1, p2):
        self.current_player = "1"
        self.players = [p1, p2]

    def send_state(self, conn, player):
        current = self.players[player]
        state_str = "Opponent's Progress: \n" + ' '.join(current.opp_guess) + "\n"
        state_str += "\nYour Hangperson: " + hangpeople.people[current.person] 
        state_str += "\n" + ' '.join(self.players[1 - player].opp_guess)
        state_str += "\n" + str(list(current.guesses))
        conn.sendall(state_str.encode())

    def check_win(self, player):
        check = self.players[1 - player]
        if check.word == check.opp_guess:
            return True
        return False

    def make_move(self, move, player):
        # return true if a move is valid 
        current = self.players[player]
        opp = self.players[1 - player]
        move = move.lower()
        if move.isalpha() and len(move) == 1 and move not in current.guesses:
            # update guesses
            current.guesses.add(move)
            if move in opp.opp_guess:
                self.update_guess(move, opp.opp_guess, opp.word)
                # if guess is in word, update guess progress in opponent 
            else:
                current.person += 1
            return True
        return False
    
    def update_guess(self, move, opp_guess, word):
        idx = 0
        for letter in word:
            if letter == move:
                opp_guess[idx] = move
            idx += 1
    
    def check_word(self, word, player): 
        if word.isalpha() and len(word) > 1:
            self.players[player].word = word.lower()
            self.players[player].opp_guess = ''.join('_' for _ in word)
            return True
        return False

    def switch_player(self):
        self.current_player = "1" if self.current_player == "2" else "2"

class hangpersonServer:
    def __init__(self, server_socket, players):
        self.host = "127.0.0.1"
        self.port = 5000
        self.server_socket = server_socket
        self.players = players

    def play_game(self, conn1, conn2):
        player1 = player()
        player2 = player()
        game = hangpersonGame(player1, player2)

        # Check connections
        try:
            conn1.sendall("You are P1\n".encode())
        except socket.error:
            conn2.sendall("Player 1 disconnected, closing connection...")
            print("Connection error, closing game...")
            return
        try:
            conn2.sendall("You are P2\n".encode())
        except socket.error:
            conn1.sendall("Player 2 disconnected, closing connection...")
            print("Connection error, closing game...")
            return

        words_in = 0
        while True:
            player = game.current_player - 1
                
            current_conn = conn1 if game.current_player == '1' else conn2
            waiting_conn = conn2 if current_conn == conn1 else conn1

            game.send_state(current_conn, player)

            try:
                current_conn.sendall("Your turn...\n".encode())
            except socket.error:
                s = "Opponent disconnected, closing connection..."
                waiting_conn.sendall(s.encode())
                print("Connection error, closing game...")
                return
            try:
                time.sleep(1)
                waiting_conn.sendall("Waiting for other player...\n".encode())
            except socket.error:
                s = "Opponent disconnected, closing connection..."
                current_conn.sendall(s.encode())
                print("Connection error, closing game...")
                return
            
            # if players have not entered words
            if words_in < 2:
                valid_word = False
                while not valid_word:
                    try:
                        current_conn.sendall("Enter your word: ".encode())
                    except socket.error:
                        s = "Opponent disconnected, closing connection..."
                        waiting_conn.sendall(s.encode())
                        print("Connection error, closing game...")
                        return
                    word = current_conn.recv(1024).decode().strip()
                    if not word:
                        s = "Opponent disconnected, closing connection..."
                        waiting_conn.sendall(s.encode())
                        print("Connection error, closing game...")
                        return
                    try:
                        if game.check_word(word, player):
                            valid_word = True
                            words_in += 1
                        else:
                            current_conn.sendall("Invalid move. Please try again.\n".encode())
                    except ValueError:
                        current_conn.sendall("Invalid input. Please enter a word consisting of alphabetic characters greater than length 1\n".encode())
            else:
                valid_move = False
                while not valid_move:
                    try:
                        current_conn.sendall("Enter your guess: ".encode())
                    except socket.error:
                        s = "Opponent disconnected, closing connection..."
                        waiting_conn.sendall(s.encode())
                        print("Connection error, closing game...")
                        return
                    move = current_conn.recv(1024).decode().strip()
                    if not move:
                        s = "Opponent disconnected, closing connection..."
                        waiting_conn.sendall(s.encode())
                        print("Connection error, closing game...")
                        return
                    try:
                        if game.make_move(move, player):
                            valid_move = True
                        else:
                            current_conn.sendall("Invalid move. Please try again.\n".encode())
                    except ValueError:
                        current_conn.sendall("Invalid input. Please enter a single letter.\n".encode())

                if game.check_win(player):
                    game.send_state(current_conn)
                    game.send_state(waiting_conn)
                    winning_message = "Congratulations! You won!\n"
                    current_conn.sendall(winning_message.encode())
                    waiting_conn.sendall("Sorry, you lost!\n".encode())
                    break

            game.switch_player()