from flask import Flask, render_template, jsonify, redirect, request
import game_engine
from components import create_battleships, initialise_board,reWritePlacementJsonFile, place_battleships, print_board
from mp_game_engine import newUser, generate_attack, newUser, players, ai

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def root():
    if request.method == 'GET':
        #check if the player has already placed their ships
        try:
            print_board(players["ai"][0])
            player_board=players["player"][0]
            return render_template('main.html', player_board=player_board)
        
        #if not, redirect them to the placement page
        except:
            return redirect('/placement?ships=battleships.txt&board_size=10')

@app.route('/attack', methods=['GET'])
def attack():
    
    if request.method == 'GET':
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        playerBoard = players["player"][0]
        aiBoard = players["ai"][0]
        playerShips = players["player"][1]
        aiShips = players["ai"][1]
        
        #check if the player has already guessed at this location
        if (x,y) in game_engine.chosen_coordinates["player"]:
            return jsonify({'alreadyGuessed': "You've already guessed at location " + str((x,y))})
        
        #if not, add it to the list of guessed locations
        game_engine.chosen_coordinates["player"].append((x,y))

        #attack ai ship with inputted coordinates 
        hitAiship, aiBoard,aiShips = game_engine.attack((x,y), aiBoard, aiShips)

        #generate ai attack coordinates and attack at those coordinates
        ai_attack_coordinates = ai.generate_attack()

        hitPlayerShip, playerBoard,playerShips = game_engine.attack(ai_attack_coordinates, playerBoard, playerShips)
        if hitPlayerShip:ai.lastMoveWasAHit = True
        print(hitPlayerShip)
        #update the players and ai's dictionary with the new boards and ships
        players["player"][0] = playerBoard
        players["ai"][0] = aiBoard  
        players["player"][1] = playerShips 
        players["ai"][1] = aiShips 

        #check for winning conditions:
        if players["ai"][1] == {}:
            return jsonify({'hit': hitAiship,'AI_Turn': ai_attack_coordinates,'finished': 'you win!!!'})
        if players["player"][1] == {}:
            return jsonify({'hit': hitAiship,'AI_Turn': ai_attack_coordinates,'finished': 'you lose...'})
        #if no winning conditions are met, return the hit status and the ai's attack coordinates
        return jsonify({'hit': hitAiship,'AI_Turn': ai_attack_coordinates})

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    if request.method == 'GET':
        #get the board size and ships from the url
        board_size = request.args.get('board_size')
        ships = create_battleships(request.args.get('ships'))

        return render_template('placement.html', ships=ships, board_size=int(board_size))
    if request.method == 'POST':
        #get the json data from the request and rewrite the placement.json file
        data = request.get_json()
        reWritePlacementJsonFile(data)

        #create the boards and ships for the player and ai
        player_ships = create_battleships()
        ai_ships = create_battleships()
        player_board = place_battleships(initialise_board(), player_ships, 'placement.json')
        ai_board = place_battleships(initialise_board(),ai_ships, 'random')

        #create the player and ai dictionaries 
        newUser("player", player_board, player_ships)
        newUser("ai", ai_board, ai_ships)
        
        #create a new set of chosen coordinates for the player and ai
        game_engine.new_set_of_chosen_coordinates("player")
        game_engine.new_set_of_chosen_coordinates("ai")

        #return a message to the client
        return jsonify({'message': 'Received'}), 200
        
if __name__ == "__main__":
    app.run(debug=True)