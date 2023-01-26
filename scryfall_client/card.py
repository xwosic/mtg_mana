import json
import re
import requests
import time

SCRY_FALL_URL = 'https://api.scryfall.com'
API_DELAY = 100
LAST_API_CALL = time.time()


class Card:
    def __init__(self, data: dict = None, name: str = None):
        self.data = data if data else None
        self._name = name

    def call_api(self):
        response = requests.get(SCRY_FALL_URL + f'/cards/named?fuzzy={self._name}')
        if response.status_code == 200:
            self.data = response.json()
        else:
            raise RuntimeError(f'Failed to get card: {self._name}')

    def __getitem__(self, key: str):
        return self.data[key]
    
    def __repr__(self):
        return f"Card(name={self.name})"
    
    def __str__(self):
        return str(self.data)

    @property
    def name(self):
        return self.data['name']

    @property
    def cmc(self):
        return int(self.data['cmc'])

    @property
    def mana_cost(self):
        """
        Property converting:
        
        "" -> {}
        
        "{2}{R}{W}" -> {"C": 2, "R": 1, "W": 1}
        
        """
        cost = {}
        mana_symbols = re.findall(r'\{.\}', self.data['mana_cost'])
        mana_symbols = [s.replace('{', '').replace('}', '') for s in mana_symbols]
        for symbol in mana_symbols:
            if symbol in ['R', 'G', 'U', 'W', 'B']:
                if symbol in cost:
                    cost[symbol] += 1
                else:
                    cost[symbol] = 1
            else:
                if "C" in cost:
                    cost["C"] += int(symbol)
                else:
                    cost["C"] = int(symbol)
        
        return cost

    @property
    def colors(self):
        return self.data['colors']
    
    @property
    def type_line(self):
        return self.data['type_line']
    
    @property
    def produced_mana(self):
        return self.data.get('produced_mana', [])


def _split_to_chunks(lst, chunk_size):
    """
    chunk_size=2

    [1, 2, 3, 4, 5] -> [[1, 2], [3, 4], [5]]
    """
    if len(lst) <= chunk_size:
        return [lst]

    chunk = lst[:chunk_size]
    chunks = lst[chunk_size:]
    result = [chunk]
    result.extend(_split_to_chunks(chunks, chunk_size))
    return result


def get_cards_collection(decklist: list):
    """
    Call scryfall api for each cardname in decklist.
    Returns Card objects.
    """
    url = SCRY_FALL_URL + '/cards/collection'
    chunks = _split_to_chunks(decklist, 74)
    results = []
    cache = {
        'data': []
    }
    for chunk in chunks:
        body = {
            'identifiers': [
                {'name': n} for n in chunk
            ]
        }
        response = requests.post(url, json=body)

        results.extend([Card(data=d) for d in response.json()['data']])
        cache['data'].extend(response.json()['data'])
    
    with open('./cache.json', 'w') as f:
        f.write(json.dumps(cache))

    return results
