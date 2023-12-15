from random import randint
from json import load, dump

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
    shipData = file.read().split("\n")
    file.close()
    for ship in shipData:
        ship = ship.split(":")
        ships[ship[0]] = int(ship[1])
    return ships
def write_Placement_Json_File(data, filename="placement.json"):
    with open(filename, 'w') as outfile:
        dump(data, outfile)
    return True
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

def place_battleships(board, ships, algorithm='simple'):
    boardDimensions = (len(board)-1,len(board[0])-1)
    if (algorithm == 'simple'):
        row = 0
        for ship in ships:
            x = randint(0,boardDimensions[0]-ships[ship])
            for walkCounter in range(ships[ship]):
                board[row][x+walkCounter] = ship
            row+=1
    elif (algorithm == 'random'):
        for ship in ships:
            shipLength = ships[ship]
            findingViableLocationForTheShip = True
            while findingViableLocationForTheShip:
                x = randint(0,boardDimensions[0])
                y = randint(0,boardDimensions[1])
                directionMultiplier = ((0,1),(1,0),(0,-1),(-1,0))[randint(0,3)]
                locs = []
                for walkCounter in range(shipLength):
                    loc = (x+walkCounter*directionMultiplier[0],y+walkCounter*directionMultiplier[1])
                    if (loc[0] < 0 or loc[0]>boardDimensions[0] or 
                        loc[1] < 0 or loc[1]>boardDimensions[1] or 
                        board[loc[0]][loc[1]] != None):
                        break
                    locs.append(loc)
                if len(locs) == shipLength:
                    for loc in locs:
                        board[loc[0]][loc[1]] = ship
                    findingViableLocationForTheShip = False   
    else:
        placementDirections = { 'h':(1,0), 'v':(0,1) }
        with open(algorithm) as f:shipLocs = load(f)
        for ship in shipLocs:
            shiploc = shipLocs[ship]
            x = int(shiploc[0])
            y = int(shiploc[1])
            orientation = shiploc[2]
            shipLengths = ships[ship]
            placementDirection = placementDirections[orientation]
            placementDirectionX = placementDirection[0]
            placementDirectionY = placementDirection[1]
            for walkCounter in range(0, shipLengths):  
                board[y+walkCounter*placementDirectionY][x+walkCounter*placementDirectionX] = ship
    return board

