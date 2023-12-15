from components import initialise_board
from random import randint
class AI:
    def __init__(self,board_size: int = 10,  longest_ship : int=5):
        #this will be how the ai keeps track of the player board
        self.longest_ship = longest_ship
        self.player_board = initialise_board(10)
        self.board_size = (board_size,board_size)
        self.correct_hits = 0#how many correct hits the ai has made in a row
        self.last_location = None#the last location the ai fired at
        self.new_ship_loc = None#the location of the new ship the ai has located
        self.direction_probabilities = None#the probabilities of the best direction to try
        self.direction = None#the direction the ai is currently trying
        self.last_move_was_a_hit = False#whether the last move the ai made was a hit
        self.ship_located = False#whether the ai has located a ship
        self.locating_in_the_opposite_direction = False#whether the ai is trying in the opposite direction
        self.ship_found_has_sunk = False#whether the ai has sunk the ship it has located
        self.ship_direction_found = False#whether the ai has found the direction of the ship it has located
        

    def generate_attack(self):    
        '''
        generates a move for the ai to make
        '''

        #if the ai's last move was a hit, mark it as a hit on the player board
        if self.last_move_was_a_hit:
            self.player_board[self.last_location[1]][self.last_location[0]] = "X"
            #if the ai has not located a ship yet it means a new ship has been found and the ai will try to locate the rest of the ship
            if not self.ship_located:
                self.ship_located = True
                self.ship_found_has_sunk = False
                self.ship_direction_found = False
                self.new_ship_loc = self.last_location
                #get a list of the directions to try with the probabilities of them being the best direction
                self.direction_probabilities = self.calcuate_best_direction(self.last_location, self.player_board)
                best_direction = max(self.direction_probabilities, key=self.direction_probabilities.get)
                self.direction = self.get_vector_direction(best_direction)
        #once the ai has located a ship
        if self.ship_located:
            #if the amount of hits the ai has made is equal to the longest ship, it means the ai has sunk the ship and will try to locate a new ship by doing random moves again
            if self.correct_hits == self.longest_ship:
                self.ship_located = False
                self.ship_found_has_sunk = False
                self.ship_direction_found = False
                self.correct_hits = 0
                return self.get_random_move()
            #increase the amount of correct hits the ai has made
            if self.last_move_was_a_hit:
                self.correct_hits+=1
            #if the ai has made 2 correct hits in a row, it means the ai has found the direction of the ship
            if self.correct_hits == 2:
                self.ship_direction_found = True
            #if the ai has failed to locate the next part of the ship with the thought to be best direction try the next best direction
            if not self.last_move_was_a_hit and not self.ship_direction_found:
                self.direction_probabilities[self.get_text_from_vector_direction(self.direction)] = 0
                best_direction = max(self.direction_probabilities, key=self.direction_probabilities.get)
                self.direction = self.get_vector_direction(best_direction)
                self.last_location = self.new_ship_loc

            #if the ai misses and is traveling in the opposite direction, it means the ship has sunk
            if not self.last_move_was_a_hit and self.locating_in_the_opposite_direction:
                self.ship_found_has_sunk = True
            #if the ai has found the direction of the ship, and has reached the end of the ship in that direction, the ship might have not sunk as there is still a chance the ship is in the opposite direction from the original coordinate
            if not self.last_move_was_a_hit and not self.locating_in_the_opposite_direction and self.ship_direction_found:
                self.opposite_direction()
            #if the ai has found the direction of the ship, but it hasn't sunk yet the ai must keep firing
            if not self.ship_found_has_sunk:
                x = self.last_location[0]+self.direction[0]
                y = self.last_location[1]+self.direction[1]
                #check if the ai has reached the end of the board or hit a location that has already tried and failed try the opposite direction. If the ai IS trying the oppisite direction at this point the ship has sunk, go back to random moves
                if not self.in_range_of_board((x,y)):
                    if self.player_board[y][x] != None:
                        if not self.locating_in_the_opposite_direction:
                            self.opposite_direction()
                            x = self.last_location[0]+self.direction[0]
                            y = self.last_location[1]+self.direction[1]
                            if self.in_range_of_board((x,y)):
                                if not self.player_board[y][x] != None:
                                    self.ship_located = False
                                    self.locating_in_the_opposite_direction = False
                                    self.correct_hits = 0
                                    self.last_move_was_a_hit = False
                                    return self.get_random_move()

                    else:
                        self.ship_located = False
                        self.locating_in_the_opposite_direction = False
                        self.correct_hits = 0
                        self.last_move_was_a_hit = False
                        return self.get_random_move()
                #if the ai has not reached the end of the board or hit a location that has already been tried, try the next location
                self.player_board[y][x] = "O"#mark the location as tried for now until the ai knows if it was a hit or not
                self.last_location = (x,y)
                self.last_move_was_a_hit = False
                return (x,y)
            else:
                self.last_move_was_a_hit = False
                self.correct_hits = 0
                self.ship_located = False
                self.locating_in_the_opposite_direction = False
        #if the ai has not located a ship, it will randomly guess
        return self.get_random_move()
    
    def in_range_of_board(self, loc: tuple):
        """returns whether the param loc is in the board"""
        if loc[0] < 0 or loc[0] > self.board_size[0]-1 or loc[1] < 0 or loc[1] > self.board_size[1]-1:
            return False
        return True
    def get_random_move(self):
        """returns a random move the ai can make"""
        loc = None
        while loc == None:
            x = randint(0,self.board_size[0]-1)
            y = randint(0,self.board_size[1]-1)
            if self.player_board[y][x] == None:
                loc = (x,y)
                self.player_board[y][x] = "O"
                self.last_location = loc
        return loc
    def opposite_direction(self):
        """sets the direction to the opposite direction"""
        if   self.direction == (0,-1):self.direction = (0,1)
        elif self.direction == (0,1) :self.direction = (0,-1)
        elif self.direction == (-1,0):self.direction = (1,0)
        elif self.direction == (1,0) :self.direction = (-1,0)
        self.last_location = self.new_ship_loc
        self.locating_in_the_opposite_direction = True

    def get_vector_direction(self, direction : str):
        """returns the vector direction of the param text direction e.g. up = (0,-1)"""
        direction_multipliers = {'up': (0,-1),'down' : (0,1),'left': (-1,0),'right' : (1,0)}
        return direction_multipliers[direction]
    
    def get_text_from_vector_direction(self, direction : tuple):
        """returns the text direction of the param vector direction e.g. (0,-1) = up"""
        direction_multipliers = {(0,-1) : "up",(0,1) : "down",(-1,0) : "left",(1,0) : "right"}
        return direction_multipliers[direction]
    
    def calcuate_best_direction(self, loc : tuple, board: list):
        """returns a dictionary of the probabilities of the best direction to try"""
        """works by the higher the amount of empty spaces to try in a particular direction, the higher the probability of that being the best direction"""
        directions = {'up': 0,'down' : 0,'left': 0,'right' : 0}
        direction_multipliers = {'up': (0,-1),'down' : (0,1),'left': (-1,0),'right' : (1,0)}
        for direction in directions:
            #check if the direction is valid and which direction has the most amount of empty spaces
            direction_multiplier = direction_multipliers[direction]
            for i in range(1,10):
                x = loc[0]+i*direction_multiplier[0]
                y = loc[1]+i*direction_multiplier[1]
                
                #if it's in the board and the space is empty
                if (x < 0 or x>self.board_size[0]-1 or y < 0 or y>self.board_size[1]-1 or board[y][x] != None):
                    break
                directions[direction] += 1
        return directions




