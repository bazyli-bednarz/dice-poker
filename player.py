class Player:
    def __init__(self, name):
        self.name = name
        self.dices_saved = []
        self.dices_to_reroll = []
        self.score = []
        self.score_dices = []

    def add_to_reroll(self, index):
        print(self)
        dice = self.dices_saved.pop(index)
        self.dices_to_reroll.append(dice)

    def remove_from_reroll(self, index):
        dice = self.dices_to_reroll.pop(index)
        self.dices_saved.append(dice)

    def handle_reroll_by_array_index(self, index_list):
        # [0,1,2,5]
        dice_list = []
        for index in index_list:
            dice_list.append(self.dices_saved[index])

        new_dices_saved = [x for x in self.dices_saved if x not in dice_list]
        self.dices_to_reroll = dice_list
        self.dices_saved = new_dices_saved


    def reroll(self):
        pass

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