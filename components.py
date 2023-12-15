from random import randint
from json import load, dump

def initialise_board(size: int = 10):
    """creates an empty board of a specified size
    
    Parameters:
    size : int - the size of the board

    Returns:
    list - the board
    """
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append(None)
    return board

def create_battleships(filename: str ="battleships.txt"):
    """creates a dictionary of battleships from a specified file

    Parameters:
    filename : str - the name of the file to read the battleships from

    Returns:
    dict - the dictionary of battleships
    """
    ships = {}
    file = open(filename, "r")
    ship_data = file.read().split("\n")
    file.close()
    for ship in ship_data:
        ship = ship.split(":")
        ships[ship[0]] = int(ship[1])
    return ships

def write_Placement_Json_File(data : dict, filename : str ="placement.json"):
    """writes the data param to a json file specified by the filename param

    Parameters:
    data : dict - the data to write to the file
    filename : str - the name of the file to write to

    Returns:
    bool - whether the file was written to successfully
    """
    with open(filename, 'w') as outfile:
        dump(data, outfile)
    return True

def print_board(board: list):
    """prints a board to the console

    Parameters:
    board : list - the board to print
    """
    print("  ", end="")
    for i in range(len(board)):
        print(i, end="    ")
    print()
    for i in range(len(board)):
        print(i, end=" ")
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print()

def place_battleships(board : list, ships : dict, algorithm : str='simple'):
    """places battleships on a board

    Parameters:
    board : list - the board to place the battleships on
    ships : dict - the dictionary of battleships
    algorithm : str - the algorithm to use to place the battleships

    Algorithms:
    simple - places each battleship horizontal on a new rows starting from (0,0).
    random - places the ships randomly
    filename - places the ships according to the data in the specified file

    Returns:
    list - the board with the battleships placed on it
    """
    board_dimensions = (len(board)-1,len(board[0])-1)
    if (algorithm == 'simple'):
        row = 0
        x = 0
        for ship in ships:
            for walk_counter in range(ships[ship]):
                board[row][x+walk_counter] = ship
            row+=1
    elif (algorithm == 'random'):
        for ship in ships:
            ship_length = ships[ship]
            finding_viable_location_for_ship = True
            while finding_viable_location_for_ship:
                x = randint(0,board_dimensions[0])
                y = randint(0,board_dimensions[1])
                direction_Multiplier = ((0,1),(1,0),(0,-1),(-1,0))[randint(0,3)]
                locs = []
                for walk_counter in range(ship_length):
                    loc = (x+walk_counter*direction_Multiplier[0],y+walk_counter*direction_Multiplier[1])
                    if (loc[0] < 0 or loc[0]>board_dimensions[0] or #if the location is out of bounds or there is already a ship there
                        loc[1] < 0 or loc[1]>board_dimensions[1] or 
                        board[loc[0]][loc[1]] != None):
                        break
                    locs.append(loc)
                #if the ship can be placed at the location, place it
                if len(locs) == ship_length:
                    for loc in locs:
                        board[loc[0]][loc[1]] = ship
                    finding_viable_location_for_ship = False   
    else:#algorithm is a filename
        placement_directions = { 'h':(1,0), 'v':(0,1) }
        with open(algorithm) as f:shipLocs = load(f)
        for ship in shipLocs:
            shiploc = shipLocs[ship]
            x = int(shiploc[0])
            y = int(shiploc[1])
            orientation = shiploc[2]
            shipLengths = ships[ship]
            placement_direction = placement_directions[orientation]
            placement_directionX = placement_direction[0]
            placement_directionY = placement_direction[1]
            for walk_counter in range(0, shipLengths):  
                board[y+walk_counter*placement_directionY][x+walk_counter*placement_directionX] = ship
    return board

