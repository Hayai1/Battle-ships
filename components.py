
from random import randint
from json import load
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
        ships[shipData[ship]] = int(shipData[ship+1])
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
    boardDimensions = (len(board)-1,len(board[0])-1)
    if (configuration == 'simple'):
        row = 0
        for ship in ships:
            x = randint(0,boardDimensions[0]-ships[ship])
            for walkCounter in range(ships[ship]):
                board[row][x+walkCounter] = ship
            row+=1
    elif (configuration == 'random'):
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
        placementDirections = { 'right':(1,0), 'left':(-1,0), 'up':(0,-1), 'down':(0,1) }
        with open(configuration) as f:data = load(f)
        shiplocations = data['shipLocs']
        for ship in shiplocations:
            shipLengths = ships[ship['name']]
            placementDirection = placementDirections[ship['direction']]
            for walkCounter in range(0, shipLengths):
                board[ship['y']+walkCounter*placementDirection[1]][ship['x']+walkCounter*placementDirection[0]] = ship['name']
    return board

board = place_battleships(initialise_board(),create_battleships(),'placement.json')
print_board(board)
