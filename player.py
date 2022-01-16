class Player:
    def __init__(self, name):
        self.name = name
        self.dices_saved = []
        self.dices_to_reroll = []
        self.score = []

    def add_to_reroll(self, index):
        dice = self.dices_saved.pop(index)
        self.dices_to_reroll.append(dice)

    def remove_from_reroll(self, index):
        dice = self.dices_to_reroll.pop(index)
        self.dices_saved.append(dice)

    def reroll(self):
        pass

    def __repr__(self):
        return f'''
        ---
Name: {self.name}
Dices saved: {self.dices_saved}
Dices to reroll: {self.dices_to_reroll}
Score: {self.score}
        ---
        '''