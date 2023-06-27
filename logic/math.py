"""
probability of playing card in turn:
prob = prob_of_getting_lands_cmc * prob_of_getting_land_colors * prob_of_getting_card
"""
import copy
import math
import itertools


def newtons_symbol(n: int, k: int):
    return math.factorial(n) / math.factorial(k) / math.factorial(n - k)


def hypergeometric_prob(deck_size: int,
                        number_of_draws: int,
                        card_type_number_in_deck: int,
                        x: int) -> float:
    """
    ```
    prob = (K over k)(N-K over n-k)/(N over n)
    ```
    where newton's symbol tells in how many ways you can draw k cards from n cards deck
    ```
    (n over k) = n! / (k!(n-k)!)
    ```
    * `N` - deck size (deck_size)
    * `K` - number of desired cards in deck (card_type_number_in_deck)
    * `n` - number of draws
    * `k` - number of desired cards in hand which are required to success (x)
    """
    if x > card_type_number_in_deck:
        return 0.0

    # combinations of taking x cards from desired cards
    success_combinations = newtons_symbol(card_type_number_in_deck, x)

    # combinations of taking other cards from rest of the deck
    other_cards_number = deck_size - card_type_number_in_deck
    other_cards_draw = number_of_draws - x
    other_cards_combinations = newtons_symbol(other_cards_number, other_cards_draw)

    # all possible combinations of drawing cards
    all_combinations = newtons_symbol(deck_size, number_of_draws)

    # probability of drawing x desired cards in n size hand
    return success_combinations * other_cards_combinations / all_combinations


def calculate_probability_drawing_lands_and_cards(deck_size: int,
                                                  number_of_draws: int,
                                                  number_of_lands: int,
                                                  number_of_cards: int,
                                                  land_success: int,
                                                  card_success: int):
    """
    Calculate probability of event when you draw hand of cards and have
    x lands in the same color as y cards.

    probability = lands_combination * cards_combination * other_cards_combinations / all_combinations
    """
    if land_success + card_success > number_of_draws:
        return 0.0

    lands_combinations = newtons_symbol(number_of_lands, land_success)
    cards_combinations = newtons_symbol(number_of_cards, card_success)
    other_cards_in_hand = number_of_draws - land_success - card_success
    other_cards_in_deck = deck_size - number_of_cards - number_of_lands
    if other_cards_in_hand > 0 and other_cards_in_deck > 0:
        other_cards_combinations = newtons_symbol(other_cards_in_deck, other_cards_in_hand)
    else:
        other_cards_combinations = 1.0

    all_combinations = newtons_symbol(deck_size, number_of_draws)
    return lands_combinations * cards_combinations * other_cards_combinations / all_combinations


def calculate_probability_of_mana_color_curve(deck_size: int,
                                              number_of_lands: int,
                                              number_of_color_lands: int,
                                              number_of_required_color_mana_symbol: int,
                                              card_cmc: int,
                                              number_of_draws: int = None,
                                              turn_number: int = None):
    """
    Calculate probability of event when you draw lands of CMC
    which X are in required color and Y are in different color.
    """
    if number_of_draws is None and turn_number is None:
        raise ValueError('Provide number_of_draws of turn_number')

    if number_of_draws and turn_number:
        raise ValueError('Provide only one: number_of_draws or turn_number')

    if turn_number is not None:
        number_of_draws = 7 + turn_number

    other_lands_combinations = newtons_symbol(
        number_of_lands - number_of_color_lands,
        card_cmc - number_of_required_color_mana_symbol
    )
    color_lands_combinations = newtons_symbol(
        number_of_color_lands,
        number_of_required_color_mana_symbol
    )
    other_cards_in_hand = number_of_draws - card_cmc
    other_cards_in_deck = deck_size - number_of_lands
    if other_cards_in_hand < 0:
        raise ValueError('other cards in hand < 0')
    if other_cards_in_deck < 0:
        raise ValueError('other cards in deck < 0')

    if other_cards_in_hand > 0:
        other_cards_combinations = newtons_symbol(other_cards_in_deck, other_cards_in_hand)
    elif other_cards_in_hand == 0:
        other_cards_combinations = 1.0

    all_combinations = newtons_symbol(deck_size, number_of_draws)

    return other_lands_combinations * color_lands_combinations * other_cards_combinations / all_combinations


def probability_of_not_drawing_x_turns(deck_size: int, turns: int, number_of_cards: int):
    not_drawing = 1.0
    other_cards = deck_size - number_of_cards
    for i in range(turns):
        not_drawing *= (other_cards - i) / (deck_size - i)
    return not_drawing


def probability_of_drawing_during_x_turns(deck_size: int, turns: int, number_of_cards: int):
    return 1.0 - probability_of_not_drawing_x_turns(deck_size, turns, number_of_cards)


def negative_hypergeometric_distribution(deck_size, number_of_cards, draws_cards, draws_other_cards):
    """
    probability of drawing k cards and f other cards from deck with K desired cards
    """
    N = deck_size
    K = number_of_cards
    f = draws_other_cards
    k = draws_cards
    return newtons_symbol(k + f - 1, k) * newtons_symbol(N - f - k, K - k) / newtons_symbol(N, K)


def get_color_combinations(cmc: int, number_of_lands: int, colors: dict = None):
    """
    colors = {
        'red': {
            'required': 2,
            'color_lands': 10,
        }
        'green': {
            'required': 1,
            'color_lands': 20
        }
    }

    rrg2
    rrg(lands-3, 2)
    (R 2)(G 1)(L-3 2)
    """
    if not colors:
        return newtons_symbol(number_of_lands, cmc)

    else:
        sum_of_colors = 0
        combinations = 1
        for color in colors:
            number = colors[color]['required']
            lands = colors[color]['color_lands']
            sum_of_colors += number
            # (R 2)
            combinations *= newtons_symbol(lands, number)
        # (L-3 2)
        combinations *= newtons_symbol(number_of_lands - sum_of_colors, cmc - sum_of_colors)

    return combinations


# def prob_of_playing_color_card_in_turn(deck: int, color_cards_number: int, color_lands_number: int, lands_number: int,
#                                        card_cmc: int, card_color_requirement: int, number_of_draws: int):
#     """
#     prob = color_cards_combination * color_lands_combination * lands_combination * other_cards_combination / all_com
#     """
#     color_cards_combination = newtons_symbol(color_cards_number, 1)  # >= min required
#     color_lands_combination = get_color_combinations(
#         card_cmc,
#         lands_number,
#         colors={
#             'red': {
#                 'required': card_color_requirement,
#                 'color_lands': color_lands_number
#             }
#         }
#     )  # >= min required
#     # lands_combination = newtons_symbol(lands_number - color_lands_number, card_cmc - card_color_requirement)
#     other_cards_combination = newtons_symbol(deck - lands_number - 1, number_of_draws - 1 - card_cmc)
#     all_combinations = newtons_symbol(deck, number_of_draws)
#     return (
#         color_cards_combination
#         * color_lands_combination
#         # * lands_combination
#         * other_cards_combination
#         / all_combinations
#     )


def prob_of_getting_x_or_more_cards_in_turn(deck: int, turn: int, num_of_cards: int, x: int):
    """
    Hypergeometric probability can be summed to calculate failure probability.

    When you want to get prob of getting 3 or more cards of same type:
    ```
    P(X > 3) = 1 - P(X = 0) + P(X = 1) + P(X = 2)
    ```
    """
    number_of_draws = 7 + turn
    fail_probability = sum(
        [hypergeometric_prob(deck, number_of_draws, num_of_cards, i)
         for i in range(x)]
    )

    return 1.0 - fail_probability


def prob_of_getting_cards_in_range(deck: int, turn: int, num_of_cards: int, min_range: int, max_range: int):
    """
    Calculates probability of getting x cards where:
    ```
    min_range <= x <= max_range
    ```
    """
    number_of_draws = 7 + turn
    result = 0
    for i in range(min_range, max_range + 1):
        r = hypergeometric_prob(deck, number_of_draws, num_of_cards, i)
        result += r
    return result


def generate_land_card_other_combinations(deck, turn, lands, cards):
    """
    turn=2 cards=4
    ['llcoooooo', 'llccooooo', 'llcccoooo', 'llccccooo',
     'lllcooooo', 'lllccoooo', 'lllcccooo', 'lllccccoo',
     'llllcoooo', 'llllccooo', 'llllcccoo', 'llllcccco',
     'lllllcooo', 'lllllccoo', 'lllllccco', 'lllllcccc',
     'llllllcoo', 'llllllcco', 'llllllccc', 'lllllllco',
     'lllllllcc', 'llllllllc']
    """
    def add_trailing_o(string):
        return string + 'o' * (hand - len(string))

    hand = turn + 7
    combinations = []
    for land_num in range(turn, hand):
        comb = 'l' * land_num
        for _ in range(cards):
            comb += 'c'
            if len(comb) <= hand:
                combinations.append(add_trailing_o(comb))

    return combinations


def generate_land_other_combinations(turn):
    """
    turn=4
    ['llllooooooo', 'llllloooooo', 'llllllooooo', 'llllllloooo', 'llllllllooo', 'llllllllloo', 'llllllllllo']
    """
    def add_trailing_o(string):
        return string + 'o' * (hand - len(string))

    hand = turn + 7
    combinations = []
    for land_num in range(turn, hand):
        comb = 'l' * land_num
        if len(comb) <= hand:
            combinations.append(add_trailing_o(comb))

    return combinations


def prob_land_card_other(deck, turn, all_lands, lands, all_cards, cards, others):
    """
    Returns probability calculated from:

    (all_lands lands)(all_cards cards)(other_cards other_in_hand)/(deck, hand)
    """
    return (newtons_symbol(all_lands, lands)
            * newtons_symbol(all_cards, cards)
            * newtons_symbol(deck - all_lands - all_cards, others)
            / newtons_symbol(deck, turn + 7))


def probability_from_combinations(deck: int, turn: int, lands: int, cards: int):
    """
    Probability of event where:
    * at least one card with this name in turn = card's cmc
    * lands in number >= card's cmc
    """
    combinations = generate_land_card_other_combinations(deck, turn, lands, cards)
    all_probs = 0
    for combination in combinations:
        p = prob_land_card_other(
            deck,
            turn,
            lands,
            combination.count('l'),
            cards,
            combination.count('c'),
            combination.count('o')
        )
        all_probs += p

    return all_probs


def probability_for_playing_commander_cmc(deck, turn, lands):
    """
    Probability of getting enough lands to play commander.
    Color of lands is not taken into consideration here.
    """
    hand = turn + 7
    result = 0.0
    for combination in generate_land_other_combinations(turn):
        p = (newtons_symbol(lands, combination.count('l'))
             * newtons_symbol(deck - lands, combination.count('o'))
             / newtons_symbol(deck, hand))
        result += p
    return result


def probability_of_getting_right_lands(mana_cost: dict, deck_info: dict):
    """
    From mana cost takes only color symbols and ignore colorless.
    Returns probability of getting X lands in right color.
    Chanses are changing after each land draw.
    
    Example:
    You've got 10 Mountains and 14 Forests in deck.
    Cost of card is 4{R}{F}{F}
    Probability of getting these colors is:
    10/24 * 14/23 * 13/22
    """

    lands = copy.deepcopy(deck_info['lands'])
    total_num_of_lands = deck_info['total_lands']
    prob = 1
    for color in mana_cost:
        if color == "C":
            continue  # skipping colorless
    
        for _ in range(mana_cost[color]):
            if not lands[color] or not total_num_of_lands:
                prob *= 0
            prob *= lands[color] / total_num_of_lands
            lands[color] -= 1
            total_num_of_lands -= 1

    return prob    


def prob_of_str_combination(combination: str, count_mapping: dict):
    """
    ccrrw, {c: 20, r: 10, w: 10}
    newtons (20 2) (10 2) (10 1)
    all (40 5)
    returns (20 2) / (40 5)
    """
    types = set(combination)
    print(types)
    for t in types:
        if t not in count_mapping:
            raise ValueError(f'count_mapping {count_mapping} not matching with "{t}"')
    
    newtons = [
        newtons_symbol(count_mapping[t], combination.count(t))
        for t in types
    ]
    combinations = 1
    for n in newtons:
        combinations *= n

    all_combinations = newtons_symbol(
        sum([count for count in count_mapping.values()]),
        len(combination)
    )
    return combinations / all_combinations


def get_mana_cost_combinations(mana_cost: dict, deck_info: dict, turn: int):
    """
    in this case C is every other land type

    {C: 1, R: 2, W: 1} turn 5
    crrwc
    crrwr
    crrww
    """
    letters = ''.join([
        symbol
        for symbol, count in mana_cost.items()
        for _ in range(count)
    ])

    def conditions(combination: tuple):
        for color in mana_cost:
            if color != 'C':
                if color not in combination:
                    return False
                
                if mana_cost[color] > combination.count(color):
                    return False
        return True

    all_combinations = list(itertools.combinations_with_replacement(letters, r=turn))
    success_mana_combinations = set(filter(conditions, all_combinations))
    return [''.join(comb) for comb in success_mana_combinations]


def probability_of_getting_lands_in_colors(mana_cost: dict, deck_info: dict):
    """
    Probability of event:
    * cmc <= lands <= hand - 1
    * lands in colors required in mana cost
    """
    cards_cmc = sum([c for c in mana_cost.values()])
    hand = cards_cmc + 7
    lands_greater_of_equal_to_turn = prob_of_getting_cards_in_range(
        deck_info['total_number'],
        cards_cmc,
        deck_info['total_lands'],
        min_range=cards_cmc,
        max_range=hand - 1
    )
    lands_in_good_colors_probability = probability_of_getting_right_lands(
        mana_cost=mana_cost,
        deck_info=deck_info
    )
    return lands_greater_of_equal_to_turn * lands_in_good_colors_probability


# mana_comb = get_mana_cost_combinations({'R': 2, "W": 1, "C": 1}, {}, 4)
# print('get_mana_cost_combinations', mana_comb)
# print('prob_of_str_combination', prob_of_str_combination(mana_comb[0], {'R': 10, 'W': 10, "C": 20}))


def prob_of_drawing_combination(combination: str | list, count_mapping: dict):
    """
    ## iterating probability
    ```
    lands = "rrrwwbb"
    cards = 112
    ```
    ### prob of "rwb12r"
    ```
    3/10 * 2/9 * 2/8 * 2/7 * 1/6 * 2/5 = 0.00031746031746031746
    ```
    """
    types = set(combination)
    for t in types:
        if t not in count_mapping:
            raise ValueError(f'count_mapping {count_mapping} not matching with "{t}"')
    
    mapping = copy.deepcopy(count_mapping)
    total_number = sum([c for c in mapping.values()])
    prob = 1.0
    for element_type in combination:
        if not mapping[element_type] or not total_number:
            prob = 0
        prob *= mapping[element_type] / total_number
        mapping[element_type] -= 1
        total_number -= 1
    
    return prob

print('iter', prob_of_drawing_combination('rwb12r', {
    'r': 3,
    'w': 2,
    'b': 2,
    '1': 2,
    '2': 1
}))