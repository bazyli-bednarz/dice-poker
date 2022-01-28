from flask import Flask, render_template, request, redirect
from result import Result
from player import Player
from game import Game

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z'
game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hotseat')
def hotseat():
    return render_template('hotseat.html')

@app.route('/hotseat_start', methods=['POST'])
def hotseat_start():
    global game
    game = Game()
    for player in request.form:
        if request.form[player] != '':
            game.add_player(request.form[player])
    if game.number_of_players() <= 1:
        return redirect('/hotseat')
    else:
        return redirect('/board')

@app.route('/board')
def board():
    global game
    if game.number_of_players() == 0:
        return redirect('/hotseat')
    return render_template('board.html', game=game, active_player = game.players[game.active_player])

@app.route('/roll', methods=['POST'])
def roll():
    global game
    if game.number_of_players() == 0:
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

    game.players[game.active_player].handle_reroll_by_array_index(to_reroll)
    game.start_rolling()

    if game.check_if_finished():
        return redirect('/win')

    return redirect('/board')

@app.route('/win')
def win():
    global game
    if game.check_if_finished():
        return render_template('win.html', winner=game.check_game_winner(), game=game)
    return redirect('/')


#
# game.add_player('Tomasz')
# game.add_player('Bożena')
#
#
# print(game)
#
# #Tomasz 1/2
# game.start_rolling()
#
# #Tomasz 2/2
# game.start_rolling()
#
# #Bożena 1/2
# game.start_rolling()
#
#
# #Bożena 2/2
# game.start_rolling()
# print('PO 1 RUNDZIE', game)
#
#
#
# #Tomasz 1/2
# game.start_rolling()
#
# #Tomasz 2/2
# game.start_rolling()
#
# #Bożena 1/2
# game.start_rolling()
# game.players[game.active_player].add_to_reroll(0)
# game.players[game.active_player].add_to_reroll(0)
# game.players[game.active_player].add_to_reroll(0)
#
# # print('PO USTAWIENIU PRZERZUCENIA 1',rozgrywka)
#
# game.players[game.active_player].remove_from_reroll(2)
#
# # print('PO USTAWIENIU PRZERZUCENIA 2',rozgrywka)
# #Bożena 2/2
# game.start_rolling()
# print('PO 2 RUNDZIE', game)
#
#
# #Tomasz 1/2
# game.start_rolling()
#
# #Tomasz 2/2
# game.start_rolling()
#
# #Bożena 1/2
# game.start_rolling()
#
#
# #Bożena 2/2
# game.start_rolling()
# print('PO 3 RUNDZIE', game)


# -----


# rozgrywka.start_rolling()
#
# rozgrywka.players[rozgrywka.active_player].add_to_reroll(0)
# rozgrywka.players[rozgrywka.active_player].add_to_reroll(0)
# rozgrywka.players[rozgrywka.active_player].add_to_reroll(2)
# rozgrywka.players[rozgrywka.active_player].remove_from_reroll(2)
#
#
# rozgrywka.start_rolling()
#
# print(rozgrywka)
#
# rozgrywka.start_rolling()
# rozgrywka.players[rozgrywka.active_player].add_to_reroll(0)
# print(rozgrywka)
#
# rozgrywka.start_rolling()
# print(rozgrywka)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5151, debug=True)
