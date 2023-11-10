
import random

def initialise_board(size=10):
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append(None)
    return board

def create_battleships(filename="battleships.txt"):
    ships = {}
    file = open(filename, "r")
    shipData = file.readlines()[0].split(",")
    file.close()
    for ship in range(0, len(shipData), 2):
        ships[shipData[ship]] = shipData[ship+1]
    return ships


def print_board(board):
    print("  ", end="")
    for i in range(len(board)):
        print(i, end="    ")
    print()
    for i in range(len(board)):
        print(i, end=" ")
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print()

def place_battleships(board, ships, configuration='simple'):
    if (configuration == 'simple'):
        row = 0
        for ship in ships:
            random.randint(len(board[0]))
    if (configuration == 'random'):
        pass
    else:
        pass

create_battleships()
