from result import Result
from collections import Counter

class AI:
    """Returns tuple in form (dices_saved[], dices_to_reroll[])"""
    @staticmethod
    def ai_move_first(dices_saved):
        dice_score = Result.dice_score(dices_saved)
        occurrences = Counter(sorted(dices_saved))
        most_common = occurrences.most_common(5)

        if dice_score < 1:
            return [], dices_saved
        if dice_score < 7:
            pair = most_common[0][0]
            return [pair, pair], [0]*3
        if dice_score < 16:
            first_pair = most_common[0][0]
            second_pair = most_common[1][0]
            return [first_pair, second_pair]*2, [0]
        if dice_score < 22:
            three_of_a_kind = most_common[0][0]
            return [three_of_a_kind]*3, [0]*2
        if dice_score > 70 or dice_score == 25 or dice_score == 30 or (36 <= dice_score <= 58):
            return dices_saved,[]
        else:
            four_of_a_kind = most_common[0][0]
            return [four_of_a_kind]*4, [0]


    @staticmethod
    def ai_move_second():
        pass

