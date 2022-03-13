"""
Given an unlimited supply of coins of given denominations,
find the minimum number of coins required to get the desired change.

For example, consider S = { 1, 3, 5, 7 }.

If the desired change is 15, the minimum number of coins required is 3

(7 + 7 + 1) or (5 + 5 + 5) or (3 + 5 + 7)


If the desired change is 18, the minimum number of coins required is 4

(7 + 7 + 3 + 1) or (5 + 5 + 5 + 3) or (7 + 5 + 5 + 1)
"""

from datetime import datetime
from functools import wraps

def decorator(fn):
    cache = {}
    @wraps(fn)
    def wrapped(col, rest):
        key = (tuple(col), rest)
        if key in cache:
            return cache[key]
        result = fn(col, rest)
        cache[key] = result
        return result

    return wrapped


def change_coins_rec(src, target):
    def find_branch(col, rest):
        amount = target
        for item in src:
            if item <= rest:
                amount = min(amount, find_branch(col + [item], rest - item))
        if rest == 0:
            return len(col)
        return amount

    return find_branch([], target)

def change_coins_rec_cached(src, target):
    @decorator
    def find_branch(col, rest):
        amount = target
        for item in src:
            if item <= rest:
                amount = min(amount, find_branch(col + [item], rest - item))
        if rest == 0:
            return len(col)
        return amount

    return find_branch([], target)


def change_coins_iter(src, target):
    collections = []
    counter = 0

    def find_branch(collection, rest):
        for item in src:
            if rest >= item:
                new_collection = collection + [item]
                new_rest = rest - item
                collections.append((new_collection, new_rest))
        if rest == 0:
            return len(collection)
        else:
            return target # Max possible

    amount = min(target, find_branch([], target))
    while counter < len(collections):
        current_collection, current_rest = collections[counter]
        amount = min(amount, find_branch(current_collection, current_rest))
        counter += 1

    return amount


def change_coins_iter_cached(src, target):
    collections = []
    counter = 0

    @decorator
    def find_branch(collection, rest):
        for item in src:
            if rest >= item:
                new_collection = collection + [item]
                new_rest = rest - item
                collections.append((new_collection, new_rest))
        if rest == 0:
            return len(collection)
        else:
            return target # Max possible

    amount = min(target, find_branch([], target))
    while counter < len(collections):
        current_collection, current_rest = collections[counter]
        amount = min(amount, find_branch(current_collection, current_rest))
        counter += 1

    return amount


tests = [
    (set([1,3,5,7]), 15, 3),
    (set([1,3,5,7]), 18, 4),
    (set([1,3,5,7]), 20, 4),
    (set([1,3,5,7]), 21, 3),
    (set([1,2,3,4,5,6,7]), 21, 3),
    (set([1,2,3,4,5,6,7,8,9,10]), 21, 3),
    #  (set([5, 7, 10]), 100, 10),
]

def test(fn):
    start = datetime.now()
    for src_set, target, expected in tests:
        res = fn(src_set, target)
        print(src_set, target, " | Expected:", expected, " vs Res:", res)
        assert res == expected

    print("Total time: ", datetime.now() - start)


test(change_coins_rec)
test(change_coins_rec_cached)
test(change_coins_iter)
test(change_coins_iter_cached)
