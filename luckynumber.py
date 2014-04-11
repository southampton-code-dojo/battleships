""" This is a Demo AI to show how the game works.

This will be added by default into all servers so whatever is here will be
the behaviour of the "Demo" player on the server.

"""

from game import AI
import random
U,D,L,R = 0,1,2,3

def opposite(dir):
    if dir == R: return L
    if dir == L: return R
    if dir == U: return D
    if dir == D: return U
class BattleshipsAI(AI):

    """ Your class name must be BattleshipsAI and must extend AI. """

    # Use something unique as team name. This will identify your bot
    # on the server
    TEAM_NAME = "the magic number"
    mode = "search"
    to_try = [(x,y) for x in range(10) for y in range(10)]
    last_x,last_y = None,None
    trys_since_search = 0
    def place_ships(self, game):

        """ While we have ships to place, place ships. """

        

        try:

            if random.random() < .5:
                print "1"

                game.place_ship(1, 1, 6, game.HORIZONTAL)


                game.place_ship(2, 2, 2, game.VERTICAL)
                game.place_ship(2, 4, 2, game.VERTICAL)


                game.place_ship(3, 7, 2, game.VERTICAL) 


                game.place_ship(4, 4, 7, game.HORIZONTAL)

                game.place_ship(5, 2, 5, game.HORIZONTAL)



            else:
                print "2"

                game.place_ship(1, 6, 1, game.VERTICAL)


                game.place_ship(2, 2, 2, game.HORIZONTAL)
                game.place_ship(2, 2, 4, game.HORIZONTAL)


                game.place_ship(3, 2, 7, game.HORIZONTAL) 


                game.place_ship(4, 7, 4, game.VERTICAL)

                game.place_ship(5, 5, 2, game.VERTICAL)


        except:
            print "This didn't work"


        # while len(game.ships_to_place) > 0:
        #     try:
        #         x = random.randint(0, 9)
        #         y = random.randint(0, 9)

        #         # We need to tell the game which ship (size) we're
        #         # placing, the x and y co-ordinates, and the direction to place
        #         # it.
        #         game.place_ship(game.ships_to_place[0], x, y, game.HORIZONTAL)
        #     except game.CannotPlaceShip:
        #         # This will be raised if we try to overlap ships
        #         # or go outside the boundary (x0-9y0-9)

        #         # If it is raised, ships_to_place won't change
        #         # so we can just loop and try again
        #         pass

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
        hit,ship = None,None
        if self.trys_since_search >= 9:
            self.mode = "search"
        if self.mode == "attack_undirected" or self.mode == "attack_directed":

            if self.last_x > 9 or self.last_x < 0:
                self.next_search = opposite(self.next_search)
            if self.last_y > 9 or self.last_y <0:
                self.next_search = opposite(self.next_search)


            if self.next_search == R:
                self.last_x += 1
                self.last_y += 0
            elif self.next_search == L:
                self.last_x -= 1
                self.last_y += 0
            elif self.next_search == U:
                self.last_x += 0
                self.last_y -= 1
            elif self.next_search == D:
                self.last_x += 0
                self.last_y += 1

        else:
            trys_since_search = 0
            # self.last_x,self.last_y = random.randint(0, 9), random.randint(0, 9)
            self.last_x,self.last_y = random.sample(self.to_try,1)[0]
        point = (int(self.last_x),int(self.last_y))

        if self.mode != "search": self.trys_since_search += 1
        else: self.trys_since_search = 0
        if point not in self.to_try:
            return self.take_shot(game)
        else:
            self.to_try = [x for x in self.to_try if x != point]


        hit,ship = game.take_shot(self.last_x,self.last_y)



        if hit and ship:
            self.mode = "search"
        elif self.mode == "search":
            if hit:
                self.mode = "attack_undirected"
                self.next_search = R
        elif self.mode == "attack_undirected":
            if hit:
                self.mode = "attack_directed"
            else:
                self.next_search = (self.next_search + 1) % 4
                if self.next_search == R:
                    self.mode = "search" # fix this, be more clever
        elif self.mode == "attack_directed":
            if hit:
                pass
            else:
                self.next_search = opposite(self.next_search)


