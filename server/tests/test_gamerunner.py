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
        class LoserAI(AI):
            def place_ships(self, game):
                game.place_ship(1, 0, 0)

            def take_shot(self, game):
                pass

        class TestAI(LoserAI):
            def take_shot(self, game):
                game.take_shot(0, 0)

        player1 = Player(ai=TestAI())
        player2 = Player(opponent=player1, ai=TestAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        game.place_ships()

        self.assertEquals(game.winner, None)
        game.next_turn()
        self.assertEquals(game.winner, player1)

        player1 = Player(ai=LoserAI())
        player2 = Player(opponent=player1, ai=TestAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        game.place_ships()

        self.assertEquals(game.winner, None)
        game.next_turn()
        self.assertEquals(game.winner, None)
        game.next_turn()
        self.assertEquals(game.winner, player2)

    def test_gamerunner_alternates_shots_until_game_over(self):
        """ Test gamerunner .play() alternates until end of game. """
        pass