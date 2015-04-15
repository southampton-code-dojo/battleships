from unittest import TestCase
from ..game import Board, Player, AI


class TestBoard(TestCase):
    def test_player_can_place_ships(self):
        """ Test the player can place available ships. """
        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])

        y = 0
        while len(player.ships_to_place) > 0:
            player.place_ship(player.ships_to_place[0], 0, y)
            y += 1

    def test_player_cant_place_more_ships_than_allowed(self):
        """ Test the player can't place ships they're not allowed to. """
        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])

        y = 0
        while len(player.ships_to_place) > 0:
            player.place_ship(player.ships_to_place[0], 0, y)
            y += 1

        with self.assertRaises(Player.CannotPlaceShip):
            player.place_ship(1, 0, y)

    def test_player_cant_place_ships_after_finishing_ship_placing(self):
        """ Test that the player only has one chance to place ships. """
        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player.place_ship(1, 0, 0)
        player.end_ship_placement()

        with self.assertRaises(Player.CannotPlaceShip):
            player.place_ship(1, 0, 0)

    def test_player_can_request_ai_place_ships(self):
        """ Test the place_ships is passed to the AI. """
        # TODO: There has to be a way to get rid of global?
        global passed_game
        passed_game = None

        class TestAI(AI):
            def place_ships(self, game):
                global passed_game
                passed_game = game

        ai = TestAI()
        player = Player(ai=ai, starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player._place_ships()
        self.assertEquals(passed_game, player)

    def test_player_only_requests_ai_place_ships_once(self):
        """ Test the player won't request the ai place ships twice. """
        global amount_called
        amount_called = 0

        class TestAI(AI):
            def place_ships(self, game):
                global amount_called
                amount_called += 1

        player = Player(ai=TestAI(), starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player._place_ships()
        player._place_ships()
        self.assertEquals(amount_called, 1)

    def test_player_cannot_take_shot_out_of_turn(self):
        """ Test the player can take a shot when it is their turn. """
        player = Player(ai=AI(), starting_ships=[5, 4, 3, 2, 2, 1, 1])

        with self.assertRaises(Player.NotYourTurn):
            player.take_shot(0, 0)

    def test_player_can_take_shot_in_turn(self):
        """ Test the player can't take two shots. """
        board = Board()

        class TestAI(AI):
            def place_ships(self, game):
                game.place_ship(1, 0, 0)

            def take_shot(self, game):
                game.take_shot(0, 0)

        player2 = Player(board=board, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player = Player(opponent=player2, ai=TestAI(),
                        starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player2._place_ships()
        player._take_shot()

        state = board.current_state()

        self.assertEquals(state[0][0], "1x")

    def test_player_cannot_take_second_shot(self):
        """ Test the player can't take two shots. """
        board = Board()

        class TestAI(AI):
            def place_ships(self, game):
                game.place_ship(2, 0, 0)

            def take_shot(self, game):
                game.take_shot(0, 0)
                game.take_shot(1, 0)

        player2 = Player(board=board, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player = Player(opponent=player2, ai=TestAI(),
                        starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player2._place_ships()
        with self.assertRaises(player.NotYourTurn):
            player._take_shot()

        state = board.current_state()
        self.assertEquals(state[0][0], "2x")
        self.assertEquals(state[1][0], 2)

    def test_has_lost(self):
        """ Test the player knows when it has lost. """

        class TestAI(AI):
            def take_shot(self, game):
                game.take_shot(0, 0)

        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player2 = Player(opponent=player, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])

        self.assertTrue(player.has_lost)

        player.place_ship(1, 0, 0)

        self.assertFalse(player.has_lost)

        player2._take_shot()

        self.assertTrue(player.has_lost)

    def test_shot_informs_of_miss(self):
        """ Test that a shot returns False for miss. """
        global shot_result
        shot_result = None

        class TestAI(AI):
            def take_shot(self, game):
                global shot_result
                shot_result = game.take_shot(0, 0)

        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player2 = Player(opponent=player, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player.place_ship(1, 1, 0)

        player2._take_shot()

        self.assertFalse(shot_result[0])
        self.assertIsNone(shot_result[1])

    def test_shot_informs_of_hit(self):
        """ Test that a shot returns True, None for hit. """
        global shot_result
        shot_result = None

        class TestAI(AI):
            def take_shot(self, game):
                global shot_result
                shot_result = game.take_shot(0, 0)

        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player2 = Player(opponent=player, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player.place_ship(2, 0, 0)

        player2._take_shot()

        self.assertTrue(shot_result[0])
        self.assertIsNone(shot_result[1])

    def test_shot_informs_of_destroyed(self):
        """ Test that a shot returns True, ship for destroyed. """
        global shot_result
        shot_result = None

        class TestAI(AI):
            def take_shot(self, game):
                global shot_result
                shot_result = game.take_shot(0, 0)

        player = Player(starting_ships=[5, 4, 3, 2, 2, 1, 1])
        player2 = Player(opponent=player, ai=TestAI(),
                         starting_ships=[5, 4, 3, 2, 2, 1, 1])

        player.place_ship(1, 0, 0)

        player2._take_shot()

        self.assertTrue(shot_result[0])
        self.assertEqual(shot_result[1], 1)
