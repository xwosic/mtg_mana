import json
from decklist.reader import DecklistReader
from pprint import pprint
from logic.core import (prob_of_playing_this_card_on_curve, 
                        prob_of_playing_card_on_curve, 
                        probability_of_playing_commander_on_curve, 
                        probability_for_mana_costs)
from scryfall_client.card import Card


deck_reader = DecklistReader('./standard.txt')

decklist = deck_reader.get_decklist()

# decklist.load_card_info_from_file('./cache.json')
decklist.fetch_cards_info()

# commander = Card(name='Atla Palani')
# commander.call_api()
# decklist.commanders = [commander]

# pprint(decklist.deck)
decklist.fill_decklist_info()

# pprint(decklist.deck_info)

on_curve = prob_of_playing_card_on_curve(deck=decklist, show_plot=True)
pprint(on_curve)

print('probability_of_playing_commander_on_curve', probability_of_playing_commander_on_curve(
    deck=decklist
))

mana_costs = probability_for_mana_costs(decklist, True)
pprint(mana_costs)

print('sum of on curve', sum([v for v in on_curve.values()]))
print('sum of mana cost', sum([v for v in mana_costs.values()]) - 1)