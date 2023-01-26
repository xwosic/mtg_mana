import json
from decklist.reader import DecklistReader
from pprint import pprint
from logic.core import (prob_of_playing_this_card_on_curve, 
                        prob_of_playing_card_on_curve, 
                        probability_of_playing_commander_on_curve, 
                        probability_for_mana_costs)
from scryfall_client.card import Card


deck_reader = DecklistReader('./mgtgo.txt')

decklist = deck_reader.get_decklist()

decklist.load_card_info_from_file('./cache.json')
commander = Card(name='Atla Palani')
commander.call_api()
decklist.commanders = [commander]

pprint(decklist.deck)
decklist.fill_decklist_info()

pprint(decklist.deck_info)

card_name = 'Sol Ring'
print('prob_of_playing_this_card_on_curve', card_name, prob_of_playing_this_card_on_curve(
    card=decklist.deck[card_name]['info'],
    deck=decklist
))

print('prob_of_playing_card_on_curve', prob_of_playing_card_on_curve(
    turn=1,
    deck=decklist
))

print('probability_of_playing_commander_on_curve', probability_of_playing_commander_on_curve(
    deck=decklist
))

pprint(decklist.sort_by_mana_cost())
mana_costs = probability_for_mana_costs(decklist)
pprint(mana_costs)
mana_costs = dict(sorted(mana_costs.items()))

import matplotlib.pyplot as plt
x = []
y = []
for k, v in mana_costs.items():
    t = ''
    for s, n in json.loads(k).items():
        t += str(s) + str(n)
    x.append(t)
    y.append(v)
plt.plot(x, y, marker='o')
plt.xticks(rotation=90)
plt.show()