"""
Your task, is to create a NxN spiral with a given size.

For example, spiral with size 5 should look like this:

>>> 00000
>>> ....0
>>> 000.0
>>> 0...0
>>> 00000

and with the size 10:

>>> 0000000000
>>> .........0
>>> 00000000.0
>>> 0......0.0
>>> 0.0000.0.0
>>> 0.0..0.0.0
>>> 0.0....0.0
>>> 0.000000.0
>>> 0........0
>>> 0000000000

Return value should contain array of arrays, of 0 and 1, for example for given size 5 result should be:

>>> [[1,1,1,1,1],[0,0,0,0,1],[1,1,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]

Because of the edge-cases for tiny spirals, the size will be at least 5.

General rule-of-a-thumb is, that the snake made with '1' cannot touch to itself.
"""

from itertools import chain

def spiralize(size):
    mx = []
    frame_cells = lambda row, even: tuple(chain(
        *[[x, size - x - 1] for x in range(
            row if row <= size / 2 else size - row - 1
        ) if x % 2 == even]
    ))
    for rdx in range(size):
        mx.append([0]*size)
        even = 0 if size % 2 or rdx <= size / 2 else 1
        odd = 1 if size % 2 or rdx <= size / 2 else 0
        white_cells = frame_cells(rdx, 1)
        black_cells = frame_cells(rdx, 0)
        for cdx in range(size):
            # Draw frames
            if rdx % 2 == even:
                if cdx not in white_cells:
                    mx[rdx][cdx] = 1
            elif rdx % 2 == odd:
                if cdx in black_cells:
                    mx[rdx][cdx] = 1
            # Draw a "neck" - always before the left-top corner of frame.
            if rdx <= size / 2 and cdx + 1 == rdx and not (
                    rdx == size / 2 and size % 4 == 0):
                mx[rdx][cdx] = (rdx + 1) % 2
    return mx
