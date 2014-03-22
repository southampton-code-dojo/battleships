""" Battleships game components. """
from copy import copy

# Useful constants
HORIZONTAL = 0
VERTICAL = 1

# Use a 10x10 board
BOARD_SIZE = 10


class Board(object):

    """ A game board that contains ships """

    class CannotPlaceShip(Exception):
        pass

    def __init__(self):
        self.ships = []

    def ship_at_position(self, x, y):
        """ Return the ship at position x, y. None if none. """
        for ship in self.ships:
            if [x, y] in ship["coordinates"]:
                return ship
        return None

    def current_state(self):
        """ Return the current state of the board. """
        columns = []
        for x in range(BOARD_SIZE):
            current_column = []
            for y in range(BOARD_SIZE):
                ship = self.ship_at_position(x, y)
                if ship:
                    current_column.append(ship["size"])
                else:
                    current_column.append(None)
            columns.append(current_column)
        return columns

    def __str__(self):
        """ Represent the current state of the board as a string. """
        state = self.current_state()

        output = ""

        # Transpose so it's easier to output
        for row in zip(*state):
            for cell in row:
                if not cell:
                    output += " "
                else:
                    output += str(cell)
            output += "\n"

        return output[:-1]

    def place_ship(self, size, x, y, direction=HORIZONTAL):
        """ Place a ship sized size at x,y. """
        coordinates = []
        current_coordinate = [x, y]
        current_size = size
        while current_size > 0:
            if self.ship_at_position(*current_coordinate):
                raise self.CannotPlaceShip("Already a ship at %s" %
                                           current_coordinate)
            coordinates.append(copy(current_coordinate))
            current_size -= 1
            current_coordinate[direction] += 1

        self.ships.append({"size": size, "coordinates": coordinates})
