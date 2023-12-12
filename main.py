import game_engine
from flask import Flask, render_template, request, jsonify, session
from components import create_battleships, initialise_board,reWritePlacementJsonFile, place_battleships, print_board
from mp_game_engine import newUser, generate_attack, newUser, players
app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('main.html', player_board=players["player"][0])


@app.route('/attack', methods=['GET', 'POST'])
def attack():
    if request.method == 'GET':
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        playerBoard = players["player"][0]
        enemyBoard = players["enemy"][0]
        playerShips = players["player"][1]
        enemyShips = players["enemy"][1]
        print("enemy ships: ", enemyShips)
        print_board(enemyBoard)
        hit, players["enemy"][0],players["enemy"][1] = game_engine.attack((x,y), enemyBoard, enemyShips)
        if players["enemy"][1] == {}:
            return jsonify({'hit': hit,'AI_Turn': generate_attack(),'finished': 'you win!!!'})
        if players["player"][1] == {}:
            return jsonify({'hit': hit,'AI_Turn': generate_attack(),'finished': 'you lose...'})
        return jsonify({'hit': hit,'AI_Turn': generate_attack()})


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    if request.method == 'GET':
        try:
            board_size = request.args.get('board_size')
            ships = create_battleships(request.args.get('ships'))
            return render_template('placement.html', ships=ships, board_size=int(board_size))
        except:
            return render_template('index.html')
    if request.method == 'POST':
        data = request.get_json()
        reWritePlacementJsonFile(data)
        
        player_ships = create_battleships()
        enemy_ships = create_battleships()
        player_board = place_battleships(initialise_board(), player_ships, 'placement.json')
        enemy_board = place_battleships(initialise_board(),enemy_ships)
        newUser("player", player_board, player_ships)
        newUser("enemy", enemy_board, enemy_ships)
        return jsonify({'message': 'Received'}), 200
        
       

if __name__ == "__main__":
    app.run(debug=True)