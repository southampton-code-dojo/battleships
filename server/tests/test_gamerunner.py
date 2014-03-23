from unittest import TestCase
from ..game import GameRunner, Board, Player, AI


class TestGameRunner(TestCase):
    def test_gamerunner_can_place_ships(self):
        """ Test the gamerunner can place ships. """

        # TODO: There has to be a way to get rid of global?
        global passed_game1
        passed_game1 = None
        global passed_game2
        passed_game2 = None

        class TestAI1(AI):
            def place_ships(self, game):
                global passed_game1
                passed_game1 = game
        class TestAI2(AI):
            def place_ships(self, game):
                global passed_game2
                passed_game2 = game

        player1 = Player(ai=TestAI1())
        player2 = Player(ai=TestAI2())

        game = GameRunner(player1, player2)
        game.place_ships()

        self.assertEquals(passed_game1, player1)
        self.assertEquals(passed_game2, player2)

    def test_gamerunner_places_ships_at_start_of_game(self):
        """ Test the gamerunner places ships at start of game. """

        # TODO: There has to be a way to get rid of global?
        global passed_game1
        passed_game1 = None
        global passed_game2
        passed_game2 = None

        class TestAI1(AI):
            def place_ships(self, game):
                global passed_game1
                passed_game1 = game
        class TestAI2(AI):
            def place_ships(self, game):
                global passed_game2
                passed_game2 = game

        player1 = Player(ai=TestAI1())
        player2 = Player(ai=TestAI2())

        game = GameRunner(player1, player2)
        game.play()

        self.assertEquals(passed_game1, player1)
        self.assertEquals(passed_game2, player2)