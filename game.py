from player import Player
from result import Result
from ai import AI
from collections import Counter
from flask import flash
from flask import Markup
import random
import math

class Game:
    # Game class

    # Dictionary for mapping dice points to its values
    dice_fontawesome_dict = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six'
    }

    def __init__(self, game_type, difficulty = None):
        # Initialization
        self.dices = (1,2,3,4,5,6)
        self.players = []
        self.active_player = 0
        self.turn_to_end = False
        self.turn = 0
        self.winners = []
        self.number_of_rounds = 3
        self.finished = False
        self.winner = -1
        self.game_type = game_type
        self.starting_player = 0
        self.difficulty = difficulty

    def add_player(self, name):
        # For adding new player to the game
        self.players.append( Player(name) )

    def number_of_players(self):
        # Get number of players
        return len(self.players)

    def next_player(self):
        # Change active player to the next in queue
        self.active_player += 1
        self.active_player %= self.number_of_players()

    def roll(self, dice_list):
        # Return new values for each dice in the list
        for i in range(len(dice_list)):
            random_dice = random.randint(1,6)
            self.players[self.active_player].dices_saved.append(random_dice)

    def get_round_progress(self):
        # Returns round progress in format round/number of rounds
        return self.get_round()+'/'+str(self.number_of_rounds)

    def get_round(self):
        # Returns round number
        return str(math.ceil(self.turn / 2))

    def start_rolling(self):
        # Handles rolling dice
        if self.check_if_finished():
            self.turn_to_end = False
            self.turn = 0
            return


        if not self.turn_to_end:
            self.turn += 1
            self.players[self.active_player].dices_saved = []
            self.players[self.active_player].dices_to_reroll = []
            self.roll([0 for _ in range(5)])
            self.turn_to_end = True
            if self.game_type == 'solo' and self.active_player == 1:
                self.start_rolling()
        else:

            message_dice_count_ai = ''
            if self.game_type == 'solo' and self.active_player == 1 and self.difficulty != 'easy':

                for dice in self.players[self.active_player].dices_saved:
                    message_dice_count_ai += '<i class="fas fa-dice-'
                    message_dice_count_ai += self.dice_fontawesome_dict[dice]
                    message_dice_count_ai += '"></i> '
                if self.difficulty == 'hard' and self.starting_player == 0:
                    starting_player_score = Result.dice_score(self.players[0].score_dices[-1])
                    self.players[self.active_player].dices_saved, self.players[
                        self.active_player].dices_to_reroll = AI.ai_move_second(
                        self.players[self.active_player].dices_saved, starting_player_score)
                else:
                    self.players[self.active_player].dices_saved, self.players[self.active_player].dices_to_reroll = AI.ai_move_first(self.players[self.active_player].dices_saved)

            self.roll(self.players[self.active_player].dices_to_reroll)
            score = Result.dice_score(self.players[self.active_player].dices_saved)
            self.players[self.active_player].score.append(score)
            self.players[self.active_player].score_dices.append(self.players[self.active_player].dices_saved)
            self.players[self.active_player].dices_to_reroll = []

            message_dice_count = ''

            for dice in self.players[self.active_player].score_dices[-1]:
                message_dice_count += '<i class="fas fa-dice-'
                message_dice_count += self.dice_fontawesome_dict[dice]
                message_dice_count +='"></i> '

            if message_dice_count_ai != '':
                message = Markup('<b>' + self.players[self.active_player].name + '</b> wyrzuca<br>' + message_dice_count_ai + ',<br>a po przerzuceniu<br>' + message_dice_count)
            else:
                message = Markup('Gracz <b>' + self.players[self.active_player].name + '</b> wyrzuca<br>' + message_dice_count)
            flash(message)
            if self.turn % self.number_of_players() == 0:
                winner = self.check_winner()
                self.winners.append(winner)
                self.starting_player = winner

                if self.turn == (self.number_of_rounds * 2):
                    self.finished = True
                    return

                if self.check_if_won_most():
                    self.finished = True
                    return

                if winner != self.active_player:
                    self.next_player()


            else:
                self.next_player()
            self.turn_to_end = False

    def check_if_finished(self):
        # Returns True if the game is finished or False if not
        return self.finished


    def check_winner(self):
        # Returns index of winning player or -1 in case of a draw
        winner = -1
        if self.players[0].score[-1] > self.players[1].score[-1]:
            winner = 0
        elif self.players[0].score[-1] < self.players[1].score[-1]:
            winner = 1
        return winner

    def check_if_won_most(self):
        # Checks if it's possible to win with player with most wins
        statistics = Counter([value for value in self.winners if value != -1])

        if statistics[0] > self.number_of_rounds - self.turn/2 and statistics[0] > statistics[1]:
            return True
        if statistics[1] > self.number_of_rounds - self.turn/2 and statistics[1] > statistics[0]:
            return True
        return False

    def check_game_winner(self):
        # Returns game winner
        statistics = Counter(self.winners)
        occurrences = statistics.most_common()

        if occurrences[0][0] == -1 and occurrences[0][1] == self.number_of_rounds:
            # If there are only draws
            return -1

        # Else delete draws from list, as they do not determine the winner
        statistics = Counter([value for value in self.winners if value != -1])
        occurrences = statistics.most_common()

        # If most common occurrence is the only one, that player wins
        if len(occurrences) == 1:
            return occurrences[0][0]

        # Else if most common occurrence is equal to the second one, this is a draw,
        # as players share the same score
        if occurrences[0][1] == occurrences[1][1]:
            return -1

        # Finally, if the draw does not occur, player with most occurrences wins
        return  occurrences[0][0]

    def __repr__(self):
        return f'''
===Game===
Players: {self.players}
Active: {self.active_player}
Turn to end: {self.turn_to_end}
Winners: {self.winners}
Turn: {self.turn}
Round: {self.get_round_progress()}
        '''