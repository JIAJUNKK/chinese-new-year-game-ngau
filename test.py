import itertools
import copy
deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
# 3 7 j 3 4
# 6 6 4 10 3


class NGAW:
    def __init__(self, pictures_count, is_a_spade, card_array):
        self.pictures_count = pictures_count
        self.spade = is_a_spade
        self.card_array = card_array

    def input_cards(self):
        while len(self.card_array) < 5:
            user_card = input(f"Enter Card {len(self.card_array) + 1}: ").upper()
            if user_card == '1':
                user_card = 'A'

            NGAW.check_five_pictures_count(self, user_card)
            NGAW.is_a_spade(self, user_card)

            if user_card.isdigit() and user_card != '1':
                user_card = int(user_card)

            self.card_array.append(user_card)

        return self.card_array

    def check_five_pictures_count(self, user_card):
        if user_card == 'J' or user_card == 'Q' or user_card == 'K':
            self.pictures_count += 1
        return self.pictures_count

    def is_a_spade(self, user_card):
        if user_card == "A":
            check_spade = int(input("Spades or no? Enter 1 for yes. Enter 2 for no\n>>"))
            if check_spade == 1:
                self.spade = True
        return self.spade


class Checking:
    def __init__(self, ngaw: NGAW, check_ngaw_zai: [], change_cards_to_6: [], change_cards_to_3: [], ngaw_zai: []):
        self.card_array = ngaw.card_array
        self.check_ngaw_zai = check_ngaw_zai

        self.change_cards_to_6_array = change_cards_to_6
        self.change_cards_to_3_array = change_cards_to_3

        self.ngaw_zai = ngaw_zai

    @staticmethod
    def find_combinations(cards_array, cards):
        for five_cards in range(len(cards_array) + 1):
            for card in itertools.combinations(cards_array, five_cards):
                if len(card) == 3:
                    cards.append(card)

    @staticmethod
    def convert_to_list(cards):
        for three_cards in range(len(cards)):
            cards[three_cards] = list(cards[three_cards])

    @staticmethod
    def changing_cards_into_numbers(cards):
        for three_cards in range(len(cards)):
            for card in range(len(cards[three_cards])):
                if cards[three_cards][card] == 'J' or cards[three_cards][card] == 'Q' or cards[three_cards][card] == 'K':
                    cards[three_cards][card] = 10

                if cards[three_cards][card] == 'A':
                    cards[three_cards][card] = 1
        return cards

    @staticmethod
    def change_cards_to_6(cards, checkNgawArray, ngawzaiArray):
        for three_cards in range(0, int(len(cards))):
            for card in range(0, len(cards[three_cards])):
                if sum(cards[three_cards]) % 10 != 0:
                    while cards[three_cards][card] == 3:
                        cards[three_cards][card] = 6
            if sum(cards[three_cards]) % 10 == 0:
                ngawzaiArray.append(checkNgawArray[three_cards])

    @staticmethod
    def change_cards_to_3(cards, checkNgawArray, ngawzaiArray):
        for three_cards in range(0, int(len(cards))):
            for card in range(0, len(cards[three_cards])):
                if sum(cards[three_cards]) % 10 != 0:
                    while cards[three_cards][card] == 6:
                        cards[three_cards][card] = 3
            if sum(cards[three_cards]) % 10 == 0:
                ngawzaiArray.append(checkNgawArray[three_cards])
    @staticmethod
    def sum_up_points(two_cards_array):
        for cards in range (len(two_cards_array)):
            if sum(two_cards_array[cards]) % 10 == 0:
                two_cards_array[cards] = 10
            else:
                two_cards_array[cards] = sum(two_cards_array[cards]) % 10

    def find_ngaw_zai(self):
        self.find_combinations(self.card_array, self.check_ngaw_zai)
        self.find_combinations(self.card_array, self.change_cards_to_3_array)
        self.find_combinations(self.card_array, self.change_cards_to_6_array)

        self.convert_to_list(self.check_ngaw_zai)
        self.convert_to_list(self.change_cards_to_3_array)
        self.convert_to_list(self.change_cards_to_6_array)

        self.changing_cards_into_numbers(self.change_cards_to_6_array)
        self.changing_cards_into_numbers(self.change_cards_to_3_array)

        self.change_cards_to_6(self.change_cards_to_6_array, self.check_ngaw_zai, self.ngaw_zai)
        self.change_cards_to_3(self.change_cards_to_3_array, self.check_ngaw_zai, self.ngaw_zai)


class FinalCalculation:
    def __init__(self, double: bool, double_point: int, ngaw_tongku: bool, double_array: [], cards: NGAW, ngawArray: Checking, two_cards_array: [], ngaw: NGAW,
                 conversion: Checking):
        self.double = double
        self.double_point = double_point
        self.ngaw_tongku = ngaw_tongku
        self.double_array = double_array

        self.calculation_cards_array = cards.card_array
        self.calculation_ngawArray = ngawArray.ngaw_zai
        self.calculation_two_cards_array = two_cards_array

        self.is_a_spade = ngaw.spade
        self.convert_into_numbers = conversion

    @staticmethod
    def calculate_largest_points(ngawArray, cards_array, two_cards_array):
        for card in range(len(ngawArray)):
            cards_array_copy = copy.deepcopy(cards_array)
            for i in range(3):
                if ngawArray[card][i] in cards_array_copy:
                    cards_array_copy.remove(ngawArray[card][i])
            two_cards_array.append(cards_array_copy)

    def is_a_double(self, points_array):
        for two_cards in points_array:
            if len(set(two_cards)) == 1:
                self.double = True
                self.double_array.append(two_cards[0])
        return self.double

    def is_ngaw_tongku(self, points_array):
        for two_cards in points_array:
            if ('J' in two_cards or 'Q' in two_cards or 'K' in two_cards) and self.is_a_spade:
                self.ngaw_tongku = True
        return self.ngaw_tongku

    def check_how_many_points(self, points_array):
        self.convert_into_numbers.changing_cards_into_numbers(points_array)
    def calculate_final_results(self):
        self.calculate_largest_points(self.calculation_ngawArray, self.calculation_cards_array,
                                      self.calculation_two_cards_array)
        self.is_a_double(self.calculation_two_cards_array)
        self.is_ngaw_tongku(self.calculation_two_cards_array)


user_input = NGAW(0, False, [])
check_user_cards = Checking(user_input, [], [], [], [])
calculation = FinalCalculation(False, 0, False, [],
                               user_input, check_user_cards, [], user_input, check_user_cards)

print(user_input.input_cards())
print("The cards you have entered are: ", user_input.card_array)
print(f"You have {user_input.pictures_count} picture(s)", )

check_user_cards.find_ngaw_zai()
calculation.calculate_final_results()

print(f"Spade status: {user_input.spade}")
print("Double status    : ", calculation.double)

print("Ngaw zai:                            ", check_user_cards.ngaw_zai)
if len(check_user_cards.ngaw_zai) == 0:
    print("You have got no points")
else:
    if user_input.pictures_count >= 5:
        print("You have gotten 5 pictures")

    elif user_input.spade and not calculation.double:
        print("You have gotten a NGAWTONGKU")

    elif calculation.double and not calculation.ngaw_tongku:
        calculation.double_array = sorted(set(calculation.double_array), reverse=True)
        print("Your final score is: Double", next(iter(calculation.double_array)))

    elif not calculation.double and not calculation.ngaw_tongku:
        check_user_cards.changing_cards_into_numbers(calculation.calculation_two_cards_array)
        check_user_cards.sum_up_points(calculation.calculation_two_cards_array)
        print(f"Your have gotten {max(calculation.calculation_two_cards_array)} points from your cards")

