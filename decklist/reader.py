import re
from decklist import Decklist


class DecklistReader:
    '''
    Reads txt decklist and parses it to scryfall request.
    '''
    def __init__(self, decklist: str):
        self.decklist = {
            'commander': {},
            'mainboard': {},
            'sideboard': {},
            'maybeboard': {}
        }
        destination = 'mainboard'
        with open(decklist, 'r') as file:
            for line in file.readlines():
                if self.validate(line):
                    card, count = self.parse_name_and_count_from_line(line)
                    self.add_to_deck(destination, card, count)
                else:
                    new_destination = self.change_destination(line)
                    if new_destination:
                        destination = new_destination

    def change_destination(self, line):
        for dest in self.decklist:
            if dest in line.lower():
                return dest

    def validate(self, line: str):
        return re.match(r'\d+ .*', line)

    def parse_name_and_count_from_line(self, line: str) -> tuple:
        count, *name = line.split(' ')
        name = ' '.join(name)
        name = name.rstrip()
        try:
            count = int(count)
        except TypeError:
            name = count + ' ' + name
            count = 1

        return name, count

    def add_to_deck(self, destination, card, count):
        if card not in self.decklist[destination]:
            self.decklist[destination][card] = count
        else:
            self.decklist[destination][card] += count

    def get_decklist(self):
        return Decklist(self.decklist['mainboard'])
