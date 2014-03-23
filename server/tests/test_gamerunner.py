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

    def test_gamerunner_takes_player1_shot_first_then_player2(self):
        """ Test gamerunner will get player 1 then 2 to take turn. """
        
        # TODO: There has to be a way to get rid of global?
        global passed_game1
        passed_game1 = None
        global passed_game2
        passed_game2 = None

        class TestAI1(AI):
            def take_shot(self, game):
                global passed_game1
                passed_game1 = game
        
        class TestAI2(AI):
            def take_shot(self, game):
                global passed_game2
                passed_game2 = game

        player1 = Player(ai=TestAI1())
        player2 = Player(ai=TestAI2())

        game = GameRunner(player1, player2)
        game.next_turn()

        self.assertEquals(passed_game1, player1)
        self.assertEquals(passed_game2, None)
        passed_game1 = None

        game.next_turn()

        self.assertEquals(passed_game1, None)
        self.assertEquals(passed_game2, player2)

    def test_gamerunner_can_recognise_game_over(self):
        """ Test gamerunner can recognise game over. """
        pass

    def test_gamerunner_alternates_shots_until_game_over(self):
        """ Test gamerunner .play() alternates until end of game. """
        pass