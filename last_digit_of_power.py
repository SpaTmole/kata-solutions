# https://www.codewars.com/kata/5518a860a73e708c0a000027/train/python
# ...
"""
Example of the ring:

28 ^  0  =  1
28 ^  1  =  28
28 ^  2  =  784
28 ^  3  =  21952
28 ^  4  =  614656
28 ^  5  =  17210368
28 ^  6  =  481890304
28 ^  7  =  13492928512
28 ^  8  =  377801998336
28 ^  9  =  10578455953408
28 ^  10  =  296196766695424
28 ^  11  =  8293509467471872
28 ^  12  =  232218265089212416
28 ^  13  =  6502111422497947648
28 ^  14  =  182059119829942534144
28 ^  15  =  5097655355238390956032
28 ^  16  =  142734349946674946768896
28 ^  17  =  3996561798506898509529088
28 ^  18  =  111903730358193158266814464
28 ^  19  =  3133304450029408431470804992
28 ^  20  =  87732524600823436081182539776
28 ^  21  =  2456510688823056210273111113728

last digits starts repeating in 4 rounds: 8, 4, 2, 6
"""

rings = {
    1: 1, # [1],
    2: 4, # [6, 2, 4, 8],
    3: 4, # [1, 3, 9, 7],
    4: 2, # [6, 4],
    5: 1, # [5],
    6: 1, # [6],
    7: 4, # [1, 7, 9, 3],
    8: 4, # [6, 8, 4, 2],
    9: 2, # [1, 9],
    0: 1, # [0],
}


def last_digit(src):
    if not len(src):
        return 1
    res = src.pop()

    for base in src[::-1]:
        if base == 0:
            if res == 0:
                res = 1
            else:
                res = 0
            continue
        if res == 0:
            res = 1
            continue

        ring = 4 # Max possible
        power = res % ring
        if res >= ring:
            power += ring

        res = base ** power

    return res % 10

def last_digit_improved(src):
    def modByLast(current, rest, currentMod):
        return ((current % currentMod) * ((current % currentMod) ** ((rest + 3) % 4))) % currentMod

    if not len(src):
        return 1

    lastZero = False
    lastRest = 1
    lastIsBig = False # last >= 2, not 1, not 0;

    reducedSrc = src[1:]
    for base in reducedSrc[::-1]: # first base (src[0]) will be defining mod 10
        if lastZero:
            lastZero = False
            lastRest = 1
            lastIsBig = False
        else:
            if lastIsBig and base % 4 == 2:
                lastRest = 0
            else:
                lastRest = modByLast(base, lastRest, 4)

            lastZero = base == 0
            lastIsBig = base > 1

    if lastZero:
        return 1

    return modByLast(src[0], lastRest, 10)

def simple_last_digit(lst):
    n = 1
    for x in reversed(lst):
        n = x ** (n if n < 4 else n % 4 + 4)
    return n % 10

test_data = [
    ([], 1),
    ([0, 0], 1),
    ([0, 0, 0], 0),
    ([1, 2], 1),
    ([3, 4, 5], 1),
    ([4, 3, 6], 4),
    ([7, 6, 21], 1),
    ([12, 30, 21], 6),
    ([2, 2, 2, 0], 4),
    ([937640, 767456, 981242], 0),
    ([123232, 694022, 140249], 6),
    ([499942, 898102, 846073], 6),
    # Hard cases
    ([449663, 405611, 451893], 7),
    ([449663, 405611, 451893, 95512], 7),
    ([233358, 406271, 422496], 8),
    ([706003, 824491, 757133], 7),
    ([657727, 361491, 487668], 7),

]
for test_input, test_output in test_data:
    result = last_digit(test_input)
    print(result, " vs ", test_output)
    assert result == test_output
