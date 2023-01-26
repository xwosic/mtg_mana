from decklist.reader import DecklistReader
from pprint import pprint
from logic.core import prob_of_playing_this_card_on_curve, prob_of_playing_card_on_curve, probability_of_playing_commander_on_curve
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