#!/usr/bin/python3

from socket import socket, AF_INET, SOCK_STREAM
from argparse import ArgumentParser
import threading 
import string
import time

MAX_MESSAGE_LENGTH = 20
current_turn = 1
game_state = {
    "P1 Guesses":dict.fromkeys(string.ascii_lowercase, 0),
    "P2 Guesses":dict.fromkeys(string.ascii_lowercase, 0),
    "P1 Word":"",
    "P2 Word":"",
    "P1 Man":0,
    "P2 Man":0
}


def main():

    hostname = '127.0.0.1'

    # Parse arguments
    arg_parser = ArgumentParser(description="Hangman server")
    arg_parser.add_argument("-p", "--port",
            type=int, required=True, help="Port to listen on")
    settings = arg_parser.parse_args()

    print("Running hangman server on port {}".format(settings.port))

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((hostname, settings.port))
    sock.listen(2)

    client_number = 1
    while True:
        client_sock, client_address = sock.accept()
        print(f"Connected to client {client_number}: {client_address}")
        threading.Thread(target=handle_client, args=(client_sock, client_number)).start()
        client_number += 1
        
    sock.close()
    return

def handle_client(sock, client_number):
    global current_turn
    global game_state

    sent = False
    
    while True:
        if client_number != current_turn:
            if sent:
                time.sleep(1)
                continue
            else:
                # If it's not the player's turn and the message hasn't been sent, inform the client
                sock.send("It is the other player's turn.\n".encode())
                sent = True
                continue
        else:
            # if game hasn't started, prompt for word
            if game_state["P%s Word" % current_turn] == "":
                sock.send("Input a word: \n".encode())
                word = receive_msg(sock)
                game_state["P%s Word" % current_turn] = word
            else: 
                guess = receive_msg(sock)
                if game_state["P%s Guesses" % current_turn][guess] == 0:
                    sock.send("Good Guess! The word is ")


            if current_turn == 1:
                current_turn = 2
            else:
                current_turn = 1
   
    sock.close()
    return

def receive_msg(sock):
    in_msg = sock.recv(4096)
    msg = in_msg.decode().strip()
    return msg

if __name__ == '__main__':
    main()