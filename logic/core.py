import json
import matplotlib.pyplot as plt
from logic.math import probability_of_getting_right_lands, \
                       probability_from_combinations, \
                       probability_for_playing_commander_cmc, \
                       probability_of_getting_lands_in_colors
from decklist import Decklist
from scryfall_client.card import Card


def prob_of_playing_this_card_on_curve(card: Card, deck: Decklist):
    """
    Probability of event where:
    * at least one card with this name in turn = card's cmc
    * lands in number >= card's cmc
    * lands are in colors and number that enables to play this card
    """
    getting_cmc_lands_and_card = probability_from_combinations(
        deck=deck.deck_info['total_number'],
        turn=card.cmc,
        lands=deck.deck_info['total_lands'],
        cards=deck.deck[card.name]['count']
    
    )
    lands_in_good_colors_probability = probability_of_getting_right_lands(
        mana_cost=card.mana_cost,
        deck_info=deck.deck_info
    )
    print('getting_cmc_lands_and_card', getting_cmc_lands_and_card)
    print('lands_in_good_colors_probability', lands_in_good_colors_probability)
    return getting_cmc_lands_and_card * lands_in_good_colors_probability


def prob_of_playing_card_on_curve(deck: Decklist, show_plot=False):
    """
    Probability of drawing lands and at least one card with cmc
    that can be played "on curve". Color is not taken into consideration.
    """
    results = {}
    for cmc, count_of_cards in deck.deck_info['cards_cmc'].items():
            results[cmc] = probability_from_combinations(
                deck=deck.deck_info['total_number'],
                turn=cmc,
                lands=deck.deck_info['total_lands'],
                cards=count_of_cards
            )

    if show_plot:
        plt.bar(results.keys(), results.values())
        plt.title('Prob of playing card on curve')
        plt.show()

    return results


def probability_of_playing_commander_on_curve(deck: Decklist):
    if not deck.commanders:
        return 0.0
    results = {}
    for commander in deck.commanders:
        getting_required_num_of_lands = probability_for_playing_commander_cmc(
            deck=deck.deck_info['total_number'],
            turn=commander.cmc,
            lands=deck.deck_info['total_lands']
        )
        right_colors = probability_of_getting_right_lands(
            commander.mana_cost,
            deck.deck_info
        )
        results[commander.name] = getting_required_num_of_lands * right_colors

    return results


def probability_for_mana_costs(deck: Decklist, show_plot=False):
    """
    Probability of having mana in good color and amount to play card with this cost
    in turn = cmc.

    * cmc <= lands <= drawn cards - 1 (enough lands to play card)
    * lands in colors required in mana cost (min num of lands in correct colors)
    """
    result = {}
    mana_costs = deck.sort_by_mana_cost()
    for mana_cost_json in mana_costs:
        mana_cost = json.loads(mana_cost_json)
        result[mana_cost_json] = probability_of_getting_lands_in_colors(mana_cost, deck.deck_info)
    
    result = dict(sorted(result.items()))

    if show_plot:
        x = []
        y = []
        for k, v in result.items():
            t = ''
            for s, n in json.loads(k).items():
                if s == "C":
                    t += str(n)
                else:
                    t += s * n 
            x.append(t)
            y.append(v)
        plt.bar(x, y)
        plt.title('Probability of having mana to pay the mana cost')
        plt.xlabel('Mana cost')
        plt.ylabel('Probability')
        plt.xticks(rotation=90)
        plt.show()

    return result
