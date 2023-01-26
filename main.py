from decklist.reader import DecklistReader
from pprint import pprint
# from logic.math import probability_from_combinations
from logic.core import prob_of_playing_this_card_in_turn, prob_of_playing_card_on_curve


deck_reader = DecklistReader('./mgtgo.txt')

decklist = deck_reader.get_decklist()

decklist.load_card_info_from_file('./cache.json')

pprint(decklist.deck)
pprint(len(decklist.deck))


decklist.fill_decklist_info()

pprint(decklist.deck_info)

# print('Etali', decklist.deck['Etali, Primal Storm']['info'].mana_cost)
# print('Forest', decklist.deck['Forest']['info'].mana_cost)
# print('Rugged', decklist.deck['Rugged Highlands']['info'].mana_cost)
# print('in both sets', 5/8, 4/8)
# print('removed', 4/7, 3/7)
# print('extended', 5/9, 4/9)

print('prob_of_playing_this_card_in_turn', prob_of_playing_this_card_in_turn(
    card=decklist.deck['Etali, Primal Storm']['info'],
    deck=decklist
))

print('prob_of_playing_card_on_curve', prob_of_playing_card_on_curve(
    turn=5,
    deck=decklist
))