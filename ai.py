from result import Result
from collections import Counter


def high_card(dice_score, dices_saved):
    # When computer rolls high card, it tries to achieve straight
    if dice_score == Counter([6, 5, 4, 3, 1]):
        return [6, 5, 4, 3], [1]
    if dice_score == Counter([6, 5, 4, 2, 1]):
        return [6, 5, 4, 2], [1]
    if dice_score == Counter([6, 5, 3, 2, 1]):
        return [6, 5, 3, 2], [1]
    if dice_score == Counter([6, 4, 3, 2, 1]):
        return [6, 4, 3, 2], [1]
    return [], dices_saved

def pair_dices(most_common):
    # Pair
    pair = most_common[0][0]
    return [pair, pair], [0] * 3

def two_pairs(most_common):
    # Two pairs
    first_pair = most_common[0][0]
    second_pair = most_common[1][0]
    return [first_pair, second_pair] * 2, [0]

def three_of_a_kind_dices(most_common):
    # Three of a kind
    three_of_a_kind = most_common[0][0]
    return [three_of_a_kind] * 3, [0] * 2

def high_score(dices_saved):
    # AI keeps high value scores
    return dices_saved, []

def four_of_a_kind_dices(most_common):
    # Four of a kind - AI tries to roll five of a kind
    four_of_a_kind = most_common[0][0]
    return [four_of_a_kind] * 4, [0]

def high_card_with_known_score(dice_score, dices_saved, score):
    if score <= 30:
        return high_card(dice_score, dices_saved)
    else:
        return [], [0]*5

def pair_dices_with_known_score(most_common, score):
    # Pair
    pair = most_common[0][0]
    if score > Result.dice_score([pair]*5):
        # If five of a kind doesn't give AI a win, it will reroll all
        return [], [0]*5
    return [pair, pair], [0] * 3

def two_pairs_with_known_score(most_common, score):
    # Two pairs
    first_pair = most_common[0][0]
    second_pair = most_common[1][0]
    if score > Result.dice_score([first_pair]*3+[second_pair]*2):
        return [first_pair] * 2, [0] * 3
    return [first_pair, second_pair] * 2, [0]

def three_of_a_kind_dices_with_known_score(most_common, score, dices_saved):
    # Three of a kind
    three_of_a_kind = most_common[0][0]
    if score > Result.dice_score([three_of_a_kind]*5):
        # Computer keeps the highest score dice and rerolls the rest
        if max(dices_saved) == three_of_a_kind:
            return [], [0]*5
        return [max(dices_saved)], [0] * 4
    return [three_of_a_kind] * 3, [0] * 2

def straight_with_known_score(score, dices_saved):
    if score <= Result.dice_score(dices_saved):
        return dices_saved, []
    return [], [0]*5

def full_house_with_known_score(most_common, score):
    three_of_a_kind = most_common[0][0]
    pair = most_common[1][0]
    if score > Result.dice_score([three_of_a_kind]*5):
        return [], [0]*5
    if Result.dice_score([three_of_a_kind]*4 < score < Result.dice_score([pair]*4)):
        return [pair]*2, [0]*3
    return [three_of_a_kind]*3, [0] * 2

def four_of_a_kind_dices_with_known_score(most_common, score):
    # Four of a kind - AI tries to roll five of a kind
    four_of_a_kind = most_common[0][0]
    if score > Result.dice_score([four_of_a_kind]*5):
        return [], [0] * 5
    return [four_of_a_kind] * 4, [0]

def poker_with_known_score(most_common, score, dices_saved):
    if score == most_common[0][0]:
        return dices_saved, []
    return [], [0]*5




class AI:
    """Returns tuple in form (dices_saved[], dices_to_reroll[])"""
    @staticmethod
    def ai_move_first(dices_saved):
        dice_score = Result.dice_score(dices_saved)
        occurrences = Counter(sorted(dices_saved))
        most_common = occurrences.most_common(5)

        if dice_score < 1:
            return high_card(dice_score, dices_saved)

        if dice_score < 7:
            return pair_dices(most_common)

        if dice_score < 16:
            return two_pairs(most_common)

        if dice_score < 22:
            return three_of_a_kind_dices(most_common)

        if dice_score > 70 or dice_score == 25 or dice_score == 30 or (36 <= dice_score <= 58):
            return high_score(dices_saved)
        else:
            return four_of_a_kind_dices(most_common)



    @staticmethod
    def ai_move_second(dices_saved, starting_player_score):
        dice_score = Result.dice_score(dices_saved)
        occurrences = Counter(sorted(dices_saved))
        most_common = occurrences.most_common(5)

        if dice_score > starting_player_score:
            # If AI is winning with a player, it doesn't risk and doesn't reroll
            return dices_saved, []
        if dice_score < 1:
            return high_card_with_known_score(dice_score, dices_saved, starting_player_score)
        if dice_score < 7:
            return pair_dices_with_known_score(most_common, starting_player_score)
        if dice_score < 16:
            return two_pairs_with_known_score(most_common, starting_player_score)
        if dice_score < 22:
            return three_of_a_kind_dices_with_known_score(most_common, starting_player_score, dices_saved)
        if dice_score == 25 or dice_score == 30:
            return straight_with_known_score(starting_player_score, dices_saved)
        if dice_score < 59:
            return full_house_with_known_score(most_common, starting_player_score)
        if dice_score < 67:
            return four_of_a_kind_dices_with_known_score(most_common, starting_player_score)
        return poker_with_known_score(most_common, starting_player_score, dices_saved)














