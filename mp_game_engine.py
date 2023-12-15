from ai import AI
from components import create_battleships, initialise_board, place_battleships, print_board
from game_engine import attack
ai = AI()

players = {
    
}


def newUser(name: str, board: list, ships: dict):
    """creates a new user in the players dictionary

    Parameters:
    name : str - the name of the user
    board : list - the board of the user
    ships : dict - the ships of the user

    Returns:
    name : str - the name of the user
    """
    players[name] = [board, ships]
    return name


def generate_attack():
    """generates an attack for the ai

    Returns:
    tuple - the coordinates of the attack
    """
    return ai.generate_attack()

def ai_opponent_game_loop():
    """the game loop for the ai opponent game"""
    #initialise the game
    print("Welcome to Battleships!")
    user = newUser(input("Enter a username: "), initialise_board(), create_battleships())
    ai = newUser('AI', initialise_board(),create_battleships())
    ai_ships = create_battleships()
    player_ships = create_battleships()
    players_board = place_battleships(players[user],player_ships, 'placement.json')
    ai_board = place_battleships(players[ai],ai_ships, 'random')
    players_ai_board = initialise_board()#this board is for the player to see where they have attacked the ai
    #game starts
    while True:
        print("<----------------Your board:---------------->")
        print_board(players[user])
        print("<-----------------your ai board:----------------->")
        print_board(players_ai_board)
        print("Enter coordinates to attack (x,y):")
        print("x: ", end="")
        x = int(input())
        print("y: ", end="")
        y = int(input())
        hit, ai_board,ai_ships = attack((x,y), ai_board, ai_ships)
        if hit:
            print("Hit!")
            players_ai_board[y][x] = "X"
        else:
            print("Miss!")
            players_ai_board[y][x] = "O"
        hit, players_board,player_ships = attack(generate_attack(players_board), players_board, player_ships)
        if hit:
            print("Hit!")
            players_board[y][x] = "X"
        else:
            print("Miss!")
            players_board[y][x] = "O"
        if ai_ships == {} or player_ships == {}:
            print("You win!" if ai_board == [] else "You lose!")
            break

if __name__ == "__main__":
    ai_opponent_game_loop()
           