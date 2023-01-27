import json
from decklist.reader import DecklistReader
from pprint import pprint
from logic.core import (prob_of_playing_this_card_on_curve, 
                        prob_of_playing_card_on_curve, 
                        probability_of_playing_commander_on_curve, 
                        probability_for_mana_costs)
from scryfall_client.card import Card


deck_reader = DecklistReader('./eggplant.txt')

decklist = deck_reader.get_decklist()

decklist.load_card_info_from_file('./eggplant.json')
# decklist.fetch_cards_info()

# commander = Card(name='Atla Palani')
# commander.call_api()
# decklist.commanders = [commander]

pprint(decklist.deck)
decklist.fill_decklist_info()

pprint(decklist.deck_info)

# card_name = 'Sol Ring'
# print('prob_of_playing_this_card_on_curve', card_name, prob_of_playing_this_card_on_curve(
#     card=decklist.deck[card_name]['info'],
#     deck=decklist
# ))

prob_of_playing_card_on_curve(deck=decklist, show_plot=True)

print('probability_of_playing_commander_on_curve', probability_of_playing_commander_on_curve(
    deck=decklist
))

mana_costs = probability_for_mana_costs(decklist, True)
