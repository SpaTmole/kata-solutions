"""
Texas Holdem hand

Given hole cards and community cards, the function hand to return the type of hand and a list of ranks in decreasing order of significance,
to use for comparison against other hands of the same type, of the best possible hand.

hand(["4♠", "9♦"], ["J♣", "Q♥", "Q♠", "2♥", "Q♦"])
"""

ranks_map = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

# Map: name -> (amount_of_suites, amount_of_ranks, five-in-a-row)
order_of_strategies = (
    ("straight-flush", (5, None, True)),
    ("four-of-a-kind", (None, [4], None)),
    ("full house", (None, [3, 2], None)),
    ("flush", (5, None, None)),
    ("straight", (None, None, True)),
    ("three-of-a-kind", (None, [3], None)),
    ("two pair", (None, [2, 2], None)),
    ("pair", (None, [2], None)),
)

def item_value(item):
    return ranks_map[item[:-1]]

def hand(hole_cards, community_cards):
    suites = {
        "♠": 0,
        "♦": 0,
        "♣": 0,
        "♥": 0,
    }
    ranks = {x: 0 for x in ranks_map.keys()}

    full_set = sorted(hole_cards + community_cards, key=item_value)[::-1]

    last_item_value = 0
    in_a_row = []
    straight_result = None
    in_a_row_counter = 0
    for item in full_set:
        current_item_value = item_value(item)
        if last_item_value == current_item_value + 1 :
            in_a_row.append(item)
            in_a_row_counter += 1
            if in_a_row_counter == 5:
                straight_result = in_a_row
        elif last_item_value != current_item_value:
            in_a_row = [item]
            in_a_row_counter = 1
        elif last_item_value == current_item_value:
            # don't increase in_a_row_counter
            in_a_row.append(item) # Will be removed in deduplication

        last_item_value = current_item_value

        suites[item[-1]] += 1
        ranks[item[:-1]] += 1

    for name, settings in order_of_strategies:
        matched_conditions = [False, False, False]
        suites_amount, ranks_amounts, five_in_a_row = settings
        tiebreaking_suite = None
        if suites_amount is not None:
            for suite_key, suite_value in suites.items():
                if suites_amount <= suite_value:
                    matched_conditions[0] = True
                    tiebreaking_suite = suite_key
                    break
        else:
            matched_conditions[0] = True

        tiebreaker_ranks = []
        if ranks_amounts is not None:
            for item in full_set:
                rank_key = item[:-1]
                rank_value = ranks.get(rank_key, 0)
                if rank_value >= ranks_amounts[0]:
                    tiebreaker_ranks += [rank_key] * ranks_amounts[0]
                    if len(ranks_amounts) == 2:
                        for item2 in full_set:
                            rank_key2 = item2[:-1]
                            rank_value2 = ranks.get(rank_key2, 0)
                            if rank_value2 >= ranks_amounts[1] and rank_key2 != rank_key:
                                tiebreaker_ranks += [rank_key2] * ranks_amounts[1]
                                matched_conditions[1] = True
                                break
                    else:
                        matched_conditions[1] = True
                    if matched_conditions[1]:
                        break

        else:
            matched_conditions[1] = True

        if five_in_a_row is not None:
            if straight_result:
                tiebreaker_ranks = list(map(lambda x: x[:-1], straight_result))
                if tiebreaking_suite is not None:
                    flush_in_row = 0
                    skipped = 0
                    for i, item in enumerate(straight_result):
                        item = straight_result[i]
                        if item[-1] == tiebreaking_suite:
                            flush_in_row += 1
                        elif i + 1 < len(straight_result) and straight_result[i + 1][:-1] == item[:-1]: # if next is not equal to current
                            skipped += 1
                        elif i - 1 >= 0 and straight_result[i - 1][:-1] == item[:-1]: # if previous equal to current
                            skipped += 1
                        else:
                            flush_in_row = 0

                        if flush_in_row == suites_amount:
                            tiebreaker_ranks = tiebreaker_ranks[i - suites_amount - skipped + 1:i + 1]
                            matched_conditions[2] = True
                            break

                else:
                    matched_conditions[2] = True
        else:
            matched_conditions[2] = True

        if all(matched_conditions):
            rest_for_the_hand = 5 - len(tiebreaker_ranks)
            tiebreaker_set = set(tiebreaker_ranks)
            for item in full_set:
                if rest_for_the_hand == 0:
                    break

                if item[:-1] not in tiebreaker_set:
                    if tiebreaking_suite is None or tiebreaking_suite == item[-1]:
                        tiebreaker_ranks.append(item[:-1])
                        rest_for_the_hand -= 1

            # Remove duplications:
            result = []
            deduplicated_tiebreaker_set = set([])
            for item in tiebreaker_ranks:
                if item in tiebreaker_set:
                    if item not in deduplicated_tiebreaker_set:
                        result.append(item)
                        deduplicated_tiebreaker_set.add(item)
                else:
                    result.append(item)

            return name, result[:5]

    return "nothing", list(map(lambda item: item[:-1], full_set[:5]))

tests = [
    ((["K♠", "A♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]),
     ("nothing", ["A", "K", "Q", "J", "9"]),
     ),
    ((["K♠", "Q♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]),
     ("pair", ["Q", "K", "J", "9"]),
     ),
    ((["K♠", "J♦"], ["J♣", "K♥", "9♥", "2♥", "3♦"]),
     ("two pair", ["K", "J", "9"]),
     ),
    ((["4♠", "9♦"], ["J♣", "Q♥", "Q♠", "2♥", "Q♦"]),
     ("three-of-a-kind", ["Q", "J", "9"]),
     ),
    ((["Q♠", "2♦"], ["J♣", "10♥", "9♥", "K♥", "3♦"]),
     ("straight", ["K", "Q", "J", "10", "9"]),
     ),
    ((["A♠", "K♦"], ["J♥", "5♥", "10♥", "Q♥", "3♥"]),
     ("flush", ["Q", "J", "10", "5", "3"]),
     ),
    ((["A♠", "A♦"], ["K♣", "K♥", "A♥", "Q♥", "3♦"]),
     ("full house", ["A", "K"]),
     ),
    ((["2♠", "3♦"], ["2♣", "2♥", "3♠", "3♥", "2♦"]),
     ("four-of-a-kind", ["2", "3"]),
     ),
    ((["8♠", "6♠"], ["7♠", "5♠", "9♠", "J♠", "10♠"]),
     ("straight-flush", ["J", "10", "9", "8", "7"]),
     ),
    # Extra tests
    (
        (['9♥', '7♥'], ['7♣', 'K♦', '8♥', '10♥', 'J♥']),
        ('straight-flush', ['J', '10', '9', '8', '7']),
    ),
    (
        (['7♠', 'Q♥'], ['8♥', '9♦', '6♠', '10♥', '10♦']),
        ('straight', ['10', '9', '8', '7', '6']),
    ),
    (
        (['8♠', 'J♠'], ['10♠', '9♦', 'Q♠', '9♠', '4♠']),
        ('straight-flush', ['Q', 'J', '10', '9', '8']),
    ),
]

for args, expected in tests:
    result = hand(*args)
    print("hand(", args, ") = ", result, "vs Expected:", expected)
    assert result[0] == expected[0]
    assert result[1] == expected[1]
