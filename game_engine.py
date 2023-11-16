from components import *

def attack(coordinates, board, battleships):
    cell = board[coordinates[0]][coordinates[1]]
    if cell == None:
        print("Miss!")
        return False
    else:
        print("Hit!")
        board[coordinates[0]][coordinates[1]] = None
        battleships[cell] -= 1
        if battleships[cell] == 0:
            del battleships[cell]
        return True
        
    
def cli_coordinates_input():
    print("Enter coordinates to attack (x,y):")
    print("x: ", end="")
    x = int(input())
    print("y: ", end="")
    y = int(input())
    return (x,y)

def simple_game_loop():
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships)
    print_board(board)
    while (ships != []):
        print("Welcome to Battleships!")
        place_battleships(board, ships)
        attack(cli_coordinates_input(), board, ships)
    print("You win!")

if __name__ == "__main__":
    simple_game_loop()