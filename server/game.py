""" Battleships game components. """
from copy import copy

# Useful constants
HORIZONTAL = 0
VERTICAL = 1

# Use a 10x10 board
BOARD_SIZE = 10

# Just used for formatting output
SHIP_NAMES = {
    1: "Submarine",
    2: "Destroyer",
    3: "Cruiser",
    4: "Battleship",
    5: "Aircraft Carrier"
}

# Default Ships available
# 2 x Submarine, 2 x Destroyer, 1 x Crusier,
# 1 x Battleship, 1 x Aircraft Carrier
DEFAULT_SHIPS = [5, 4, 3, 2, 2, 1, 1]

class CannotPlaceShip(Exception):
        pass

class Board(object):

    """ A game board that contains ships """

    CannotPlaceShip = CannotPlaceShip

    def __init__(self):
        self.ships = []
        self.destroyed_ships = []

    def ship_at_position(self, x, y):
        """ Return the ship at position x, y. None if none. """
        for ship in self.ships:
            if [x, y] in ship["coordinates"]:
                return ship
        return None

    def wreckage_at_position(self, x, y):
        """ Return the wreckage at position x, y. None if none. """
        for ship in self.ships + self.destroyed_ships:
            if [x, y] in ship["destroyed_coordinates"]:
                return ship
        return None

    def current_state(self):
        """ Return the current state of the board. """
        columns = []
        for x in range(BOARD_SIZE):
            current_column = []
            for y in range(BOARD_SIZE):
                ship = self.ship_at_position(x, y)
                wreck = self.wreckage_at_position(x, y)
                if ship:
                    current_column.append(ship["size"])
                elif wreck:
                    current_column.append(str(wreck["size"]) + "x")
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
                elif isinstance(cell, basestring) and cell.endswith("x"):
                    output += "x"
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
            if current_coordinate[0] < 0 or current_coordinate[1] < 0:
                raise self.CannotPlaceShip("Coordinate can't be < 0")
            if current_coordinate[0] >= BOARD_SIZE or \
                    current_coordinate[1] >= BOARD_SIZE:
                raise self.CannotPlaceShip("Coordinate can't be >= %s" %
                                           BOARD_SIZE)
            coordinates.append(copy(current_coordinate))
            current_size -= 1
            current_coordinate[direction] += 1

        self.ships.append({"size": size, "coordinates": coordinates,
                           "destroyed_coordinates": []})

    def shoot(self, x, y):
        """ Shoot at a given coordinate. Returns the ship hit, or None. """
        ship = self.ship_at_position(x, y)
        if not ship:
            return None

        ship["coordinates"].remove([x, y])
        ship["destroyed_coordinates"].append([x, y])

        if len(ship["coordinates"]) == 0:
            self.ships.remove(ship)
            self.destroyed_ships.append(ship)

        return ship


class Player(object):

    """ Represents the players in the game. """

    CannotPlaceShip = CannotPlaceShip

    def __init__(self, ai=None, board=None):
        """ Initialise the player, injecting a board if needed. """
        self.__board = board
        if not self.__board:
            self.__board = Board()

        self.ai = ai
        if not ai:
            # Use default, random AI
            self.ai = AI()

        self.__unplaced_ships = copy(DEFAULT_SHIPS)

    @property
    def ships_to_place(self):
        """ Property to protect unplaced ships. """
        return self.__unplaced_ships

    def place_ship(self, size, x, y, direction=HORIZONTAL):
        """ Place a ship, ensuring we're able to. """
        if not size in self.__unplaced_ships:
            raise self.CannotPlaceShip("No %s to place" % SHIP_NAMES[size])

        self.__unplaced_ships.remove(size)
        self.__board.place_ship(size, x, y, direction)

    def end_ship_placement(self):
        self.__unplaced_ships = []

    def place_ships(self):
        """ Tell the AI to place their ships. """
        if len(self.__unplaced_ships) > 0:
            self.ai.place_ships(self)
            self.end_ship_placement()


class AI(object):

    """ An AI which can play battleships. """

    def place_ships(self):
        pass


class GameRunner(object):

    """ Runs a game with two players. """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def place_ships(self):
        self.player1.place_ships()
        self.player2.place_ships()

    def play(self):
        self.place_ships()