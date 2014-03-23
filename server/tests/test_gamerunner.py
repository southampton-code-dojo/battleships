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
            def place_ships(self, game):
                game.place_ship(1, 0, 0)

            def take_shot(self, game):
                global passed_game1
                passed_game1 = game

        class TestAI2(TestAI1):
            def take_shot(self, game):
                global passed_game2
                passed_game2 = game

        player1 = Player(ai=TestAI1())
        player2 = Player(ai=TestAI2())

        game = GameRunner(player1, player2)
        game.place_ships()
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

        with self.assertRaises(game.IsFinished):
            game.next_turn()

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
        class LoserAI(AI):
            def place_ships(self, game):
                game.place_ship(1, 0, 0)

            def take_shot(self, game):
                pass

        class TestAI(LoserAI):
            def take_shot(self, game):
                game.take_shot(0, 0)

        player1 = Player(ai=LoserAI())
        player2 = Player(opponent=player1, ai=TestAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        self.assertEquals(game.play(), player2)

    def test_play_extremes(self):
        """ Test .play() with hitting every point on the board. """
        class LoserAI(AI):
            def place_ships(self, game):
                # Placed all of our ships all over the board
                game.place_ship(1, 0, 0)
                game.place_ship(1, 9, 9)

                game.place_ship(2, 8, 0)
                game.place_ship(2, 0, 8, game.VERTICAL)

                game.place_ship(3, 1, 3)
                game.place_ship(4, 3, 5)
                game.place_ship(5, 5, 7)

            def take_shot(self, game):
                pass

        class WinnerAI(LoserAI):
            def __init__(self):
                import itertools
                self.moves = list(itertools.product(range(10), repeat=2))

            def take_shot(self, game):
                next_move = self.moves.pop()
                game.take_shot(next_move[0], next_move[1])

        player1 = Player(ai=LoserAI())
        player2 = Player(opponent=player1, ai=WinnerAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        self.assertEquals(game.play(), player2)

        # Now run the game manually to ensure we get the correct number
        # of turns

        player1 = Player(ai=LoserAI())
        player2 = Player(opponent=player1, ai=WinnerAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        game.place_ships()

        turns = 0

        while not game.winner:
            turns += 1
            game.next_turn()

        self.assertEquals(turns, 200)  # Maximum number of turns
