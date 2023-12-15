from components import *

chosen_coordinates = {}

def new_set_of_chosen_coordinates(name):
    chosen_coordinates[name] = []

def attack(coordinates, board, battleships):
    x = coordinates[0]
    y = coordinates[1]
    hit = False
    cell = board[y][x]
    if cell != None:
        battleships[cell] -= 1
        if battleships[cell] == 0:
            del battleships[cell]
        board[y][x] = None
        hit = True
    return hit, board, battleships
        
    
def cli_coordinates_input():
    while True:
        print("Enter coordinates to attack (x,y):")
        print("x: ", end="")
        try:
            x = int(input())
            break
        except:
            print("Invalid x input")
    while True:
        print("y: ", end="")
        try:
            y = int(input())
            break
        except:
            print("Invalid y input")    
    return (x,y)

def within_board(coordinates, board):
    x = coordinates[0]
    y = coordinates[1]
    return x >= 0 and x < len(board[0]) and y >= 0 and y < len(board)

def simple_game_loop():
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships, 'placement.json')
    print_board(board)
    while (ships != []):
        print("Welcome to Battleships!")
        place_battleships(board, ships)
        loc = cli_coordinates_input()
        while not within_board(loc, board):
            print("Invalid coordinates")
            loc = cli_coordinates_input()
        hit, board,ships = attack(loc, board, ships)
        if hit:
            print("Hit!")
        else:
            print("Miss!")
    print("You win!")

if __name__ == "__main__":
    simple_game_loop()