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
    user = newUser(input("Enter a username: "), initialise_board())
    ai = newUser('AI', initialise_board())
    aiships = create_battleships()
    playerships = create_battleships()
    playersBoard = place_battleships(players[user],playerships, 'placement.json')
    aiBoard = place_battleships(players[ai],aiships, 'random')
    while True:
        print("<----------------Your board:---------------->")
        print_board(players[user])
        print("<-----------------ai board:----------------->")
        print_board(players[ai])
        print("Enter coordinates to attack (x,y):")
        print("x: ", end="")
        x = int(input())
        print("y: ", end="")
        y = int(input())
        hit, aiBoard,aiships = attack((x,y), aiBoard, aiships)
        if hit:print("Hit!")
        else:print("Miss!")
        hit, playersBoard,playerships = attack(generate_attack(playersBoard), playersBoard, playerships)
        if hit:print("Hit!")
        else:print("Miss!")
        if aiships == {} or playerships == {}:
            print("You win!" if aiBoard == [] else "You lose!")
            break

if __name__ == "__main__":
    ai_opponent_game_loop()
           