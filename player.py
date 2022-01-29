from collections import Counter
class Player:
    def __init__(self, name):
        # Initialization
        self.name = name
        self.dices_saved = []
        self.dices_to_reroll = []
        self.score = []
        self.score_dices = []

    def add_to_reroll(self, index):
        # Adds dice with given index to reroll pool
        dice = self.dices_saved.pop(index)
        self.dices_to_reroll.append(dice)

    def remove_from_reroll(self, index):
        # Removes from reroll pool by index
        dice = self.dices_to_reroll.pop(index)
        self.dices_saved.append(dice)

    def handle_reroll_by_array_index(self, index_list):
        # Rerolls dices with given index list
        dice_list = []
        for index in index_list:
            dice_list.append(self.dices_saved[index])
        dice_list_counter = Counter(dice_list)
        dices_saved_counter = Counter(self.dices_saved)
        difference = dices_saved_counter - dice_list_counter
        new_dices_saved = list(difference.elements())

        self.dices_to_reroll = dice_list
        self.dices_saved = new_dices_saved

    def __repr__(self):
        return f'''
        ---
Name: {self.name}
Dices saved: {self.dices_saved}
Dices to reroll: {self.dices_to_reroll}
Score: {self.score}
Score dices: {self.score_dices}
        ---
        '''