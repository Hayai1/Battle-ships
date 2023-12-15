from components import initialise_board
from random import randint
class AI:
    def __init__(self, longestShip=5):
        #this will be how the ai keeps track of the player board
        self.playerBoard = initialise_board(10)
        self.lastLocation = None
        self.boardSize = (len(self.playerBoard[0]),len(self.playerBoard))
        self.lastMoveWasAHit = False
        self.longestShip = longestShip
        self.shipLocated = False
        self.direction = None
        self.directionProbabilities = None
        self.newShipLoc = False
        self.locatingInTheOppositeDirection = False
        self.shipFoundHasSunk = False
        self.shipDirectionFound = False
        self.correctHits = 0

    def generate_attack(self):    
        '''
        if the last move the ai made was a hit, mark that on the mimic board and 
        if the ai has not located a ship, it will start to locate a ship
        '''
        if self.lastMoveWasAHit:
            self.playerBoard[self.lastLocation[1]][self.lastLocation[0]] = "X"
            if not self.shipLocated:
                self.shipLocated = True
                self.shipFoundHasSunk = False
                self.shipDirectionFound = False
                self.newShipLoc = self.lastLocation
                #get a list of the directions to try with the probabilities of them being the best direction
                self.directionProbabilities = self.calcuateBestDirection(self.lastLocation, self.playerBoard)
                bestDirection = max(self.directionProbabilities, key=self.directionProbabilities.get)
                self.direction = self.getVectorDirection(bestDirection)
        #once the ai has located a ship
        if self.shipLocated:
            if self.correctHits == self.longestShip:
                self.shipLocated = False
                self.shipFoundHasSunk = False
                self.shipDirectionFound = False
                self.correctHits = 0
                return self.getRandomMove()
            if self.lastMoveWasAHit:
                self.correctHits+=1
            if self.correctHits == 2:
                self.shipDirectionFound = True
            #if the ai has failed to locate the next part of the ship with the thought to be the curretn best direction try the next best direction
            if not self.lastMoveWasAHit and not self.shipDirectionFound:
                self.directionProbabilities[self.getTextFromVectorDirection(self.direction)] = 0
                bestDirection = max(self.directionProbabilities, key=self.directionProbabilities.get)
                self.direction = self.getVectorDirection(bestDirection)
                self.lastLocation = self.newShipLoc

            #if the ai is trying in the oppisite direction means it has found the direction of the ship and will keep firing in that direction until it misses to guranatee the ship is sunk
            if not self.lastMoveWasAHit and self.locatingInTheOppositeDirection:
                self.shipFoundHasSunk = True
            #if the ai has found the direction of the ship, it will keep firing in that direction until it misses
            if not self.lastMoveWasAHit and not self.locatingInTheOppositeDirection and self.shipDirectionFound:
                self.oppositeDirection()
            #if the ai has found the direction of the ship, it will keep firing in that direction until it misses
            if not self.shipFoundHasSunk:
                x = self.lastLocation[0]+self.direction[0]
                y = self.lastLocation[1]+self.direction[1]
                if y==10 or x == 10:
                    print("y is 10")
                if not self.inRangeOfBoard((x,y)):
                    if self.playerBoard[y][x] != None:
                        if not self.locatingInTheOppositeDirection:
                            self.oppositeDirection()
                            x = self.lastLocation[0]+self.direction[0]
                            y = self.lastLocation[1]+self.direction[1]
                            if self.inRangeOfBoard((x,y)):
                                if not self.playerBoard[y][x] != None:
                                    self.shipLocated = False
                                    self.locatingInTheOppositeDirection = False
                                    self.correctHits = 0
                                    self.lastMoveWasAHit = False
                                    return self.getRandomMove()

                    else:
                        self.shipLocated = False
                        self.locatingInTheOppositeDirection = False
                        self.correctHits = 0
                        self.lastMoveWasAHit = False
                        return self.getRandomMove()
                self.playerBoard[y][x] = "O"
                self.lastLocation = (x,y)
                self.lastMoveWasAHit = False
                print({(0,-1) : "up",(0,1) : "down",(-1,0) : "left",(1,0) : "right"}.get(self.direction))
                print((x,y))
                return (x,y)
            else:
                self.lastMoveWasAHit = False
                self.correctHits = 0
                self.shipLocated = False
                self.locatingInTheOppositeDirection = False
        #if the ai has not located a ship, it will randomly guess
        return self.getRandomMove()
    def inRangeOfBoard(self, loc):
        if loc[0] < 0 or loc[0] > self.boardSize[0]-1 or loc[1] < 0 or loc[1] > self.boardSize[1]-1:
            return False
        return True
    def getRandomMove(self):
        loc = None
        while loc == None:
            x = randint(0,self.boardSize[0]-1)
            y = randint(0,self.boardSize[1]-1)
            if self.playerBoard[y][x] == None:
                loc = (x,y)
                self.playerBoard[y][x] = "O"
                self.lastLocation = loc
        return loc
    def oppositeDirection(self):
        if   self.direction == (0,-1):self.direction = (0,1)
        elif self.direction == (0,1) :self.direction = (0,-1)
        elif self.direction == (-1,0):self.direction = (1,0)
        elif self.direction == (1,0) :self.direction = (-1,0)
        self.lastLocation = self.newShipLoc
        self.locatingInTheOppositeDirection = True
    def getVectorDirection(self, direction : str):
        directionMultipliers = {'up': (0,-1),'down' : (0,1),'left': (-1,0),'right' : (1,0)}
        return directionMultipliers[direction]
    def getTextFromVectorDirection(self, direction : tuple):
        directionMultipliers = {(0,-1) : "up",(0,1) : "down",(-1,0) : "left",(1,0) : "right"}
        return directionMultipliers[direction]
    def calcuateBestDirection(self, loc, board):
        directions = {'up': 0,'down' : 0,'left': 0,'right' : 0}
        directionMultipliers = {'up': (0,-1),'down' : (0,1),'left': (-1,0),'right' : (1,0)}
        for direction in directions:
            #check if the direction is valid and which direction has the most amount of empty spaces
            directionMultiplier = directionMultipliers[direction]
            for i in range(1,10):
                x = loc[0]+i*directionMultiplier[0]
                y = loc[1]+i*directionMultiplier[1]
                
                #if it's in the board and the space is empty
                if (x < 0 or x>self.boardSize[0]-1 or y < 0 or y>self.boardSize[1]-1 or board[y][x] != None):
                    break
                directions[direction] += 1
        return directions




