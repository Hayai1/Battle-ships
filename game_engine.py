from components import *

chosen_coordinates = {}#dictionary of lists of coordinates that have already been guessed for each player


def new_set_of_chosen_coordinates(name : str):
    """creates a set of coordinates that have already been guessed for a player

    Parameters
    ----------
    name : str - the name of the player
    """
    chosen_coordinates[name] = []

def attack(coordinates : tuple, board : list, battleships : dict):
    """attacks a board at a given set of coordinates
    updates the board and battleships dictionary accordingly
    returns whether the attack was a hit or not and the updated board and battleships dictionary
    
    Parameters:
    coordinates : tuple - the coordinates to attack
    board : list - the board to attack
    battleships : dict - the dictionary of battleships to attack

    Returns:
    hit : bool - whether the attack was a hit or not
    board : list - the updated board
    battleships : dict - the updated battleships dictionary
    """
    x = coordinates[0]
    y = coordinates[1]
    hit = False
    cell = board[y][x]
    if cell != None:#if the cell is not empty
        battleships[cell] -= 1
        if battleships[cell] == 0:
            del battleships[cell]
        board[y][x] = None
        hit = True
    return hit, board, battleships
        
    
def cli_coordinates_input():
    """get input from the user for coordinates
    
    Returns:
    tuple - the coordinates the user entered
    """
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

def within_board(coordinates: tuple, board: list):
    """checks if a set of specified coordinates is within a specified board

    Parameters:
    coordinates : tuple - the coordinates to check
    board : list - the board to check

    Returns:
    bool - whether the coordinates are within the board
    """
    x = coordinates[0]
    y = coordinates[1]
    height = len(board)
    width = len(board[0])
    return (x >= 0 and x < width and 
            y >= 0 and y < height)

def simple_game_loop():
    """a simple game loop that uses the command line interface
    """

    #set up the game
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships, 'placement.json')
    print_board(board) 
    place_battleships(board, ships)
    print("Welcome to Battleships!")
    
    #game loop
    while (ships != []):
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