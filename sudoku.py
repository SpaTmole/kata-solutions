"""
Write a function that will solve a 9x9 Sudoku puzzle.
The function will take one argument consisting of the 2D puzzle array,
with the value 0 representing an unknown square.

The Sudokus tested against your function will be "easy"
(i.e. determinable; there will be no need to assume and test possibilities on unknowns)
and can be solved with a brute-force approach.
"""

def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    unknowns = set([])  # Represents unknown points, which will re-solved later.
    def has_in_row(row):
        return set(puzzle[row]) - {0}

    def has_in_col(col):
        res = set()
        for r in puzzle:
            if r[col] != 0:
                res.add(r[col])
        return res

    def has_in_cell(row, col):
        res = set()
        cell = (row // 3, col // 3)
        for r in puzzle[cell[0]*3:(cell[0]+1)*3]:
            for c in r[cell[1]*3:(cell[1]+1)*3]:
              if c != 0:
                  res.add(c)
        return res

    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if puzzle[row][col] == 0:
                unknowns.add((row, col))
    while unknowns:
        for elem in list(unknowns):
            options = set(range(
                1, 10
            )) - (has_in_row(elem[0]) | has_in_col(elem[1]) | has_in_cell(*elem))
            if len(options) == 1:
                puzzle[elem[0]][elem[1]] = options.pop()
                unknowns.remove(elem)
    return puzzle
