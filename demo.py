""" This is a Demo AI to show how the game works.

This will be added by default into all servers so whatever is here will be
the behaviour of the "Demo" player on the server.

"""

from game import AI
import random


class BattleshipsAI(AI):

    """ Your class name must be BattleshipsAI and must extend AI. """

    # Use something unique as team name. This will identify your bot
    # on the server
    TEAM_NAME = "Your Team Name"

    def __init__(self):
        # Initialise data here
        pass

    def place_ships(self, game):

        """ While we have ships to place, place ships. """

        while len(game.ships_to_place) > 0:
            try:
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                # We need to tell the game which ship (size) we're
                # placing, the x and y co-ordinates, and the direction to place
                # it.
                game.place_ship(game.ships_to_place[0], x, y, game.HORIZONTAL)
            except game.CannotPlaceShip:
                # This will be raised if we try to overlap ships
                # or go outside the boundary (x0-9y0-9)

                # If it is raised, ships_to_place won't change
                # so we can just loop and try again
                pass

    def take_shot(self, game):
        # We just indicate which location we want to shoot at.
        # This will return a tuple

        # The first element of the tuple will be True or False indicating
        # if anything was hit. The second element will be None unless
        # something was destroyed - in which case it will be the size of the
        # ship destroyed.

        # E.g. If it is a miss - the return value will be
        # (False, None)

        # If it is a hit, but nothing has been destroyed completely, the return
        # value will be
        # (True, None)

        # If it is a hit, and a "Cruiser" (1x3) has been destroyed, it will be
        # (True, 3)

        # For this demo we'll do it entirely randomly and ignore the return
        # value
        game.take_shot(random.randint(0, 9), random.randint(0, 9))
