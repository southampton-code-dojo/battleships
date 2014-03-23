from unittest import TestCase
from ..game import GameRunner, Player
from ..demo import BattleshipsAI


class TestBattleshipsAI(TestCase):
    def test_demo_ai_game_finishes(self):
        """ Test the the Demo AI finishes games. """
        player1 = Player(ai=BattleshipsAI())
        player2 = Player(opponent=player1, ai=BattleshipsAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        self.assertIsNot(game.play(), None)

    def test_demo_ai_doesnt_finish_immediately(self):
        """ Test that the Demo AI takes a few turns to finish. """
        player1 = Player(ai=BattleshipsAI())
        player2 = Player(opponent=player1, ai=BattleshipsAI())
        player1.opponent = player2

        game = GameRunner(player1, player2)
        game.place_ships()

        turns = 0

        while not game.winner:
            turns += 1
            game.next_turn()

        # 18 is absolute minimum unless something is wrong
        self.assertGreater(turns, 17)
