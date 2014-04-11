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
    TEAM_NAME = "Team5"
    
    def __init__(self):
        self.not_shot = []
        for i in range(10):
            for j in range(10):
                self.not_shot.append((i,j))
        self.hits = []
        self.just_hit = False

    def place_ships(self, game):

        """ While we have ships to place, place ships. """

        while len(game.ships_to_place) > 0:
            try:
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                # We need to tell the game which ship (size) we're
                # placing, the x and y co-ordinates, and the direction to place
                # it.
                game.place_ship(1, 2, 0, game.HORIZONTAL)
                game.place_ship(1, 8, 8, game.HORIZONTAL)
                game.place_ship(2, 1, 4, game.VERTICAL)
                game.place_ship(2, 7, 4, game.HORIZONTAL)
                game.place_ship(3, 7, 0, game.HORIZONTAL)
                game.place_ship(4, 1, 8, game.HORIZONTAL)
                game.place_ship(5, 5, 2, game.VERTICAL)
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
        shoot = random.choice(self.not_shot)
        self.just_hit = False
        if self.just_hit:
            shoot = self.hits[-1]
            shoot[0] += 1
            if shoot not in self.not_shot:
                shoot[0] += -2    
        shot = game.take_shot(shoot[0], shoot[1])
        self.not_shot.remove(shoot)
        if shot[0]:
            self.hits.append(shoot)
            self.just_hit = True
