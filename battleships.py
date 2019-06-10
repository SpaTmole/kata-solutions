"""
Write a method that takes a field for well-known board game "Battleship"
as an argument and returns true if it has a valid disposition of ships,
false otherwise.
Argument is guaranteed to be 10*10 two-dimension array.
Elements in the array are numbers, 0 if the cell is free and 1 if occupied by ship.

Battleship (also Battleships or Sea Battle) is a guessing game for two players.
Each player has a 10x10 grid containing several "ships" and objective is to destroy enemy's
forces by targetting individual cells on his field.
The ship occupies one or more cells in the grid.
Size and number of ships may differ from version to version.
In this kata we will use Soviet/Russian version of the game.


Before the game begins, players set up the board and place the ships
accordingly to the following rules:
    There must be single battleship (size of 4 cells),
    2 cruisers (size 3),
    3 destroyers (size 2) and 4 submarines (size 1).
    Any additional ships are not allowed, as well as missing ships.

    Each ship must be a straight line, except for submarines, which are just single cell.

    The ship cannot overlap or be in contact with any other ship, neither by edge nor by corner.
"""

def validate_battlefield(field):
    ships = set()
    valid = set()
    allowed_fleet = {
        1: 4,
        2: 3,
        3: 2,
        4: 1
    }

    def check_ship(rx, cx):
        # corners
        for mod_x, mod_y in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
            if (rx + mod_x, cx + mod_y) in ships:
                return False

        # determine direction of the ship;
        # if it has several "directions" it makes an L bend - it is forbidden.
        directions = {
            'x': [(1, 0), (-1, 0)],
            'y': [(0, 1), (0, -1)]
        }
        mod_direction = None
        for mod_x, mod_y in directions['x'] + directions['y']:
            if (rx + mod_x, cx + mod_y) in ships:
                if not mod_direction:
                    mod_direction = 'x' if mod_x else 'y'
                elif (-mod_x, -mod_y) not in directions[mod_direction]:
                    # it makes an L bend
                    return False

        ship = [(rx, cx)]
        if mod_direction:
            ext_count = 1
            lookup_cells = [(
                rx + directions[mod_direction][_dir][0] * ext_count,
                cx + directions[mod_direction][_dir][1] * ext_count
            ) for _dir in range(2)]
            while any(lookup_cells):
                ext_count += 1
                for _clx, cell in enumerate(lookup_cells):
                    if cell in ships:
                        ship.append(cell)
                        lookup_cells[_clx] = (
                            rx + directions[mod_direction][_clx][0] * ext_count,
                            cx + directions[mod_direction][_clx][1] * ext_count
                        )
                    else:
                        lookup_cells[_clx] = None

                    if len(ship) > 4:
                        return False

        if not allowed_fleet.get(len(ship)):
            return False

        # put the ship to the field
        allowed_fleet[len(ship)] -= 1
        valid.update(ship)
        return True

    for _rx, row in enumerate(field):
        for _cx, cell in enumerate(row):
            if cell:
                ships.add((_rx, _cx))

    for ship_cell in ships:
        if ship_cell not in valid:
            if not check_ship(*ship_cell):
                return False
    # all ships must be placed.
    return not any(allowed_fleet.values())
