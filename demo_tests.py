# This is an example unit test suite for creating an AI
# 
# These are very simple because the demo AI is very simple
# You should mock the appropriate components from game.py and
# test your AI in different situations.
# 
# 
from game import GameRunner, Board, Player
from demo import BattleshipsAI
from unittest import TestCase

class TestPlayer(Player):
    """ Mock Player which records ships placed and shots taken """
    def __init__(self):
        super(TestPlayer, self).__init__()
        self.placed_ships = []
        self.shots_taken = 0

    def place_ship(self, size, x, y, direction):
        self.placed_ships.append(size)
        super(TestPlayer, self).place_ship(size, x, y, direction)

    def take_shot(self, x, y):
        self.shots_taken += 1


class TestBattleshipsAI(TestCase):
    def setUp(self):
        self.ai = BattleshipsAI()

    def test_places_all_ships(self):
        """ Test that all ships are placed. """
        player = TestPlayer()
        self.ai.place_ships(player)
        sorted_ships = sorted(player.placed_ships)
        self.assertEqual([2, 3, 3, 4, 5], sorted_ships)

    def test_takes_shot(self):
        """ Test that the AI takes a shot. """
        player = TestPlayer()
        self.ai.take_shot(player)
        self.assertEqual(1, player.shots_taken)
