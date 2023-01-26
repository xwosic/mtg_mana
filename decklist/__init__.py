import json
import re
import itertools
from scryfall_client.card import get_cards_collection, Card
from typing import List


class Decklist:
    def __init__(self, mainboard: dict, commanders: list = None):
        self.deck = mainboard
        self.commanders: List[Card] = commanders if commanders else []
        self.size = self.count_size()
        self.deck_info = {
            'total_number': None,
            'total_lands': 0,
            'lands': {
                'R': 0,
                'G': 0,
                'U': 0,
                'B': 0,
                'W': 0,
                'C': 0
            },
            'cards_cmc': {}
        }

    def count_size(self):
        return sum([count for count in self.deck.values()])

    def fetch_cards_info(self):
        payload = list(self.deck.keys())
        if self.commanders:
            payload.extend(self.commanders)

        cards = get_cards_collection(payload)
        for card in cards:
            self.deck[card.name] = {
                'count': self.deck[card.name],
                'info': card
            }

    def load_card_info_from_file(self, file: str):
        with open(file, 'r') as f:
            cards = f.read()

        cards: List[Card] = json.loads(cards)['data']

        for card in cards:
            card = Card(card)
            if card.name in self.deck:
                self.deck[card.name] = {
                    'count': self.deck[card.name],
                    'info': card
                }
            else:
                self.deck[card.name] = {
                    'count': 1,
                    'info': card
                }

    def fill_decklist_info(self):
        self.get_lands_info()
        self.get_cards_cmc_info()
        self.get_total_number()
    
    def get_total_number(self):
        self.deck_info['total_number'] = sum(
            [self.deck[n]['count'] 
             for n in self.deck]
        )
    
    def _is_land(self, card: Card):
        return re.match(r'.*Land.*', card.type_line)

    def get_lands_info(self):
        for name in self.deck:
            card: Card = self.deck[name]['info']
            if self._is_land(card):
                count = self.deck[name]['count']
                self.deck_info['total_lands'] += count
                for color in card.produced_mana:
                    self.deck_info['lands'][color] += count

    def get_cards_cmc_info(self):
        for name in self.deck:
            card: Card = self.deck[name]['info']
            if not self._is_land(card):
                count = self.deck[name]['count']
                if card.cmc in self.deck_info['cards_cmc']:
                    self.deck_info['cards_cmc'][card.cmc] += count
                else:
                    self.deck_info['cards_cmc'][card.cmc] = count

    def sort_by_mana_cost(self):
        groups = {}
        for key, group in itertools.groupby(self.deck.values(), lambda card: json.dumps(card['info'].mana_cost)):
            if key not in groups:
                groups[key] = list(group)
            else:
                groups[key].extend(group)
        return groups
