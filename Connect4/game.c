/*****
 * Project 02: Grid game
 * COSC 208, Introduction to Computer Systems, Fall 2023
 * James Burke
 *****/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define ROWS 6
#define COLS 7
#define WIN_COUNT 4

//use of typedef to avoid having to declare struct before every instance of GameState
typedef struct{
    char **board;
    char curPlayer;
    int moves;
} GameState;

//function prototypes 
GameState* initializeGame();
void printInstructions();
void printGame(GameState *game);
bool makeMove(GameState *game, int col);
bool checkWinner(GameState *game, int row, int col);
bool checkFull(GameState *game);
void freeBoard(GameState *game);

int main() {
    char playAgain = 'y';

    while(playAgain == 'y' || playAgain == 'Y') {
        GameState* game = initializeGame();
        printInstructions();
        printGame(game);
        int col;
        char input[10];
        bool play = true;

        while (play){
            printf("Player %c's turn. Moves: %d\n", game->curPlayer, game->moves);
            fgets(input, sizeof(input), stdin);
            sscanf(input, "%d", &col);

            if(col >= COLS || col < 0){
                printf("Invalid input, try again!\n");
                continue;
            }

            if(checkFull(game)){
                printf("Board is full, its a draw! Play again?\n");
                play = false;
                break;
            }

            if(makeMove(game, col)){
                printGame(game);
                printf("Player %c wins!\n", game->curPlayer);
                play = false;
            } else {
                printGame(game);
                game->curPlayer = (game->curPlayer == 'X') ? 'O' : 'X';
            }
        }
        printf("Do you want to play again? (y/n): ");
        playAgain = getchar();
        while (getchar() != '\n'); 
        freeBoard(game);
    }
    printf("Thanks for playing!\n");
    return 0;
}

//prints game instructions
void printInstructions(){
    printf("Welcome to Connect Four!\n");
    printf("In this two player game, both players will alternate turns placing their chips in the board.\n");
    printf("The first player to place 4 consecutive pieces in a row, either horizontally, vertically, or diagonally, wins!\n");
    printf("If the board is filled without any player satisfying the win condition, the game will end in a draw.\n");
}

//initializes the game by mallocing space for the rows and columns on the game board as well as setting the current player and moves to 0
GameState* initializeGame(){
    GameState *game = malloc(sizeof(GameState));
    game->board = malloc(sizeof(char *) * ROWS);
    for(int i = 0; i < ROWS; i++){
        game->board[i] = malloc(sizeof(char) * COLS);
        for(int j = 0; j < COLS; j++){
            game->board[i][j] = ' ';
        }
    }
    game->curPlayer = 'X';
    game->moves = 0;
    return game;
}

//prints a copy of the current game board
void printGame(GameState *game){
    for(int p = 0; p < (COLS*2)+1; p++){
        printf("-");
    }
    printf("\n");
    for(int i = 0; i < ROWS; i++){
        for(int j = 0; j < COLS; j++){
            printf("|%c", game->board[i][j]);
        }
        printf("|\n");
        for(int k = 0; k < (COLS*2)+1; k++){
            printf("-");
        }
        printf("\n");
    }
    printf(" 0 1 2 3 4 5 6\n");
}

//checks if the board is full by iterating through the entire array to check if there are any space characters
bool checkFull(GameState *game){
    for(int i = 0; i < ROWS; i++){
        for(int j = 0; j < COLS; j++){
            if(game->board[i][j] == ' '){
                return false;
            }
        }
    }
    return true;
}

//starts at the bottom of the board and adds a player piece at the first free space
bool makeMove(GameState *game, int col){
    char piece = game->curPlayer;
    for(int i = ROWS-1; i >= 0; i--){
        if(game->board[i][col] == ' '){
            game->board[i][col] = piece;
            game->moves+=1;
            return (checkWinner(game, i, col));
        }
    }
    printf("Column is full! Try again\n");
    return false;
}

//uses a 2D array to store each possible direction, then check left and right adjanceny through each during using a nested for and while loop
bool checkWinner(GameState *game, int row, int col){
    int dir[4][2] = {{0,1}, {1,0}, {1,1}, {1,-1}};
    char piece = game->curPlayer;
    for(int i = 0; i < WIN_COUNT; i++){
        int ct = 1;
        for(int j = -1; j <= 1; j+=2){
            int dirX = dir[i][0] * j;
            int dirY = dir[i][1] * j;
        
            int newRow = row + dirX;
            int newCol = col + dirY;

            while(newRow >= 0 && newRow < ROWS && newCol >= 0 && newCol < COLS && (game->board[newRow][newCol] == piece)){
                ct++;
                if(ct == WIN_COUNT){
                    return true;
                }
                newRow += dirX;
                newCol += dirY;
            }
        }
    }
    return false;
}

//frees the game board by first freeing every row, then the board, and finally the game struct itself
void freeBoard(GameState *game){
    for(int i = 0; i < ROWS; i++){
        free(game->board[i]);
    }
    free(game->board);
    free(game);
}