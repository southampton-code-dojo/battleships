from game import AI
import random


class DemoAI(AI):
    def place_ships(self, game):
        while len(game.ships_to_place) > 0:
            try:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                game.place_ship(game.ships_to_place[0], x, y)
            except game.CannotPlaceShip:
                pass

    def take_shot(self, game):
        game.take_shot(random.randint(0, 9), random.randint(0, 9))
