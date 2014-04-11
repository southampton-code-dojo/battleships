""" This is a Demo AI to show how the game works.

This will be added by default into all servers so whatever is here will be
the behaviour of the "Demo" player on the server.

"""

from game import AI
import random
import math
import sys

class BattleshipsAI(AI):

    """ Your class name must be BattleshipsAI and must extend AI. """

    # Use something unique as team name. This will identify your bot
    # on the server
    TEAM_NAME = "ShittleBaps"

    def __init__(self):
        # 0 = nothing
        # 1 = miss
        # 2 = hit
        # 3 = destroyed
        self.cell_state = []

        for i in range(0, 100):
            self.cell_state.append(0)

    def place_ships(self, game):

        """ While we have ships to place, place ships. """
        while len(game.ships_to_place) > 0:
            try:
                x = random.randint(0, 9)
                y = random.choice([0, 9])
                if x==0|9:
                    game.place_ship(game.ships_to_place[0], x, y, game.VERTICAL)

                if x!=0|9:
                    game.place_ship(game.ships_to_place[0], x, y, game.HORIZONTAL)


            except game.CannotPlaceShip:
                pass


    def index_to_xy(self,i):
        x = int(math.floor(i/10))
        y = i % 10
        return (x,y)

    def xy_to_index(self, x, y):
        return (y*10)+x

    def choose_pos(self):
        for i in range(0,100):
            if self.cell_state[i] == 0:
                return i
            elif self.cell_state[i] == 1:
                continue
            elif self.cell_state[i] == 2:

                (x,y) = self.index_to_xy(i)
                if x<9 and self.cell_state[i+1] == 0:
                    return i+1
                elif y<9 and self.cell_state[i+10] == 0:
                    return i+10
                else:
                    self.cell_state[i] = 4
                    return i+2



    def dump_game(self):
        for y in range(0,9):
            for x in range(0,9):
                sys.stdout.write(str(self.cell_state[(y*10)+x]))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

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
        i = self.choose_pos()
        (x,y) = self.index_to_xy(i)
        print "x,y:"+str(x)+","+str(y)
        (hit,ship) = game.take_shot(x,y)
        if hit:
            if ship:
                self.cell_state[i] = 3
            else:
                self.cell_state[i] = 2
        else:
            self.cell_state[i] = 1

        self.dump_game()

