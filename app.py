from flask import Flask, render_template, request, redirect, session
from markupsafe import Markup
from flask import flash
from game import Game

import itertools

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z'
SESSION_TYPE = 'redis'

games = {}
game_id = itertools.count()

@app.route('/')
# Index route
def index():
    return render_template('index.html')

@app.route('/hotseat')
# Route for hotseat form
def hotseat():
    return render_template('hotseat.html')

@app.route('/hotseat_start', methods=['POST'])
# Route for handling hotseat form
def hotseat_start():
    global game_id, games
    new_game_id = next(game_id)
    games[new_game_id] = Game('hotseat')
    for player in request.form:
        if request.form[player] != '':
            games[new_game_id].add_player(request.form[player])
    if games[new_game_id].number_of_players() != 2:
        games.pop(new_game_id)
        return redirect('/hotseat')
    else:
        session['game_id'] = new_game_id
        return redirect('/board')

@app.route('/solo')
# Route for solo form
def solo():
    return render_template('solo.html')

@app.route('/solo_start', methods=['POST'])
# Route for handling solo form
def solo_start():
    global game_id, games
    if not request.form.get('difficulty'):
        return redirect('/solo')
    new_game_id = next(game_id)
    games[new_game_id] = Game('solo', request.form.get('difficulty'))
    if request.form.get('player1') != '':
        games[new_game_id].add_player(request.form.get('player1'))
    games[new_game_id].add_player('Komputer')
    if games[new_game_id].number_of_players() != 2:
        games.pop(new_game_id)
        return redirect('/solo')
    else:
        session['game_id'] = new_game_id
        return redirect('/board')

@app.route('/multiplayer')
# Route for multiplayer room selection
def multiplayer():
    return render_template('multiplayer.html', games = games)

@app.route('/multiplayer_new')
# Route for new multiplayer room form
def multiplayer_new():
    return render_template('multiplayer-new.html')

@app.route('/multiplayer_start', methods=['POST'])
# Route for handling multiplayer form
def multiplayer_start():
    global game_id, games
    new_game_id = next(game_id)
    games[new_game_id] = Game('multiplayer')
    if request.form.get('player1') != '':
        games[new_game_id].add_player(request.form.get('player1'))
    if games[new_game_id].number_of_players() != 1:
        games.pop(new_game_id)
        return redirect('/multiplayer')
    else:
        session['game_id'] = new_game_id
        session['player_id'] = 0
        return redirect('/board')

@app.route('/multiplayer_join')
# Route for joining multiplayer room form
def multiplayer_join():
    if not request.args.get('id'):
        message = Markup('<b>Błędny</b> adres! 😥')
        flash(message)
        return redirect('/multiplayer')
    room_id = int(request.args.get('id'))
    session['game_id'] = room_id
    return render_template('multiplayer-join.html', games=games, room_id=room_id)

@app.route('/multiplayer_join_room', methods=['GET', 'POST'])
# Route for handling multiplayer join room
def multiplayer_join_room():
    session['game_id'] = int(request.args.get('id'))
    if not session['game_id'] and session['game_id'] != 0:
        message = Markup('<b>Nie ma</b> takiego pokoju! 😥')
        flash(message)
        return redirect('/multiplayer')
    room_id = session['game_id']
    if len(games[room_id].players) != 1:
        message = Markup('Ups, ktoś był <b>szybszy</b>! Gra jest w toku! 😥')
        flash(message)
        return redirect('/multiplayer')
    games[room_id].add_player(request.form.get('player1'))
    session['player_id'] = 1
    return redirect('/board')

@app.route('/board')
# Route for board view
def board():
    global games
    if games[session['game_id']].number_of_players() != 2 and games[session['game_id']].game_type != 'multiplayer':
        message = Markup('Ta gra ma coś <b>za mało</b> graczy! 😠')
        flash(message)
        return redirect('/')
    if games[session['game_id']].game_type == 'multiplayer' and (session['player_id'] == 0 or session['player_id'] == 1):
        if games[session['game_id']].check_if_finished():
            return redirect('/win')
        return render_template('board.html', game=games[session['game_id']],
                               active_player=games[session['game_id']].players[games[session['game_id']].active_player], player_id=session['player_id'])

    return render_template('board.html', game=games[session['game_id']], active_player = games[session['game_id']].players[games[session['game_id']].active_player])

@app.route('/roll', methods=['POST'])
# Route for dice roll form action
def roll():
    global games
    if games[session['game_id']].number_of_players() == 0:
        return redirect('/hotseat')

    to_reroll = []
    if 'dice0' in request.form:
        to_reroll.append(0)
    if 'dice1' in request.form:
        to_reroll.append(1)
    if 'dice2' in request.form:
        to_reroll.append(2)
    if 'dice3' in request.form:
        to_reroll.append(3)
    if 'dice4' in request.form:
        to_reroll.append(4)

    games[session['game_id']].players[games[session['game_id']].active_player].handle_reroll_by_array_index(to_reroll)
    games[session['game_id']].start_rolling()

    if games[session['game_id']].check_if_finished():
        return redirect('/win')

    return redirect('/board')

@app.route('/win')
# Route for winning screen
def win():
    global games
    session_game_id = session['game_id']
    if games[session_game_id].check_if_finished():
        session['game_id'] = 0
        return render_template('win.html', winner=games[session_game_id].check_game_winner(), game=games[session_game_id])
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5151, debug=True)
