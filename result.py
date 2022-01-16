from collections import Counter

class Result:
    @staticmethod
    def dice_score(dice_list):
        occurrences = Counter(sorted(dice_list))

        most_common = occurrences.most_common(5)

        if most_common[0][1] == 5:
            # Five of the same type
            return 70 + most_common[0][0]

        if most_common[0][1] == most_common[1][1] and most_common[0][0] < most_common[1][0]:
            highest = most_common[1]
            second_highest = most_common[0]
        else:
            highest = most_common[0]
            second_highest = most_common[1]

        if highest[1] == 4:
            # Four of the same type
            return 60 + highest[0]
        elif highest[1] == 3:
            if second_highest[1] == 2:
                # Full house
                return 30 + highest[0] * 3 + second_highest[0] * 2
            else:
                # Three of the same type
                return 15 + highest[0]
        elif highest[1] == 2:
            if second_highest[1] == 2:
                # Two pairs
                return 4 + highest[0] + second_highest[0]
            else:
                # One pair
                return 3 + highest[0]

        elif highest[1] == 1:
            # Six high straight
            six_high_straight = Counter([6, 5, 4, 3, 2])
            if six_high_straight == occurrences:
                return 30

            # Five high straight
            five_high_straight = Counter([5, 4, 3, 2, 1])
            if five_high_straight == occurrences:
                return 25

            return 0