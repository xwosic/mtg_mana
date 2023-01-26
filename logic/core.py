from logic.math import probability_of_getting_right_lands, \
                       probability_from_combinations, \
                       probability_for_playing_commander_cmc
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


def prob_of_playing_card_on_curve(turn: int, deck: Decklist):
    """
    
    """
    getting_cmc_lands_and_cards = probability_from_combinations(
        deck=deck.deck_info['total_number'],
        turn=turn,
        lands=deck.deck_info['total_lands'],
        cards=deck.deck_info['cards_cmc'][turn]
    )
    return getting_cmc_lands_and_cards


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
        print(getting_required_num_of_lands, right_colors)
        results[commander.name] = getting_required_num_of_lands * right_colors

    return results
