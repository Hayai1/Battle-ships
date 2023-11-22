from flask import Flask, render_template, request, redirect, url_for, jsonify
import mp_game_engine
from components import create_battleships, initialise_board, place_battleships, print_board
from game_engine import attack, cli_coordinates_input
from mp_game_engine import newUser,players
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        if 'ships' in request.args and 'board_size' in request.args:
            ships = request.args.get('ships')
            board_size = request.args.get('board_size')
            return redirect(url_for('placement_interface', ships=ships, board_size=board_size))
        else:
            return render_template('main.html')
    elif request.method == 'POST':
        if 'coordinate' in request.form:
            coordinate = request.form.get('coordinate')
            # Perform the necessary game logic to progress the game
            # ...
            return jsonify({'message': 'Game progressed'})
        else:
            return jsonify({'message': 'Invalid request'})


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    if request.method == 'GET':
        ships = request.args.get('ships')
        board_size = request.args.get('board_size')
        ships = create_battleships(ships)
        print(board_size)
        return render_template('placement.html', ships=ships, board_size=int(board_size))
       

if __name__ == "__main__":
    app.run(debug=True)