from components import create_battleships, initialise_board, place_battleships, print_board
from game_engine import attack, cli_coordinates_input

players = {
    
}
def newUser(name, board):
    players[name] = board
    return name

def generate_attack(board): 
    from random import randint
    return (randint(0, len(board)-1), randint(0, len(board)-1))

def ai_opponent_game_loop():
    print("Welcome to Battleships!")
    user = newUser(input(), initialise_board())
    ai = newUser('AI', initialise_board())
    place_battleships(players[user],create_battleships(), 'placement.json')
    place_battleships(players[ai],create_battleships(), 'random')
           