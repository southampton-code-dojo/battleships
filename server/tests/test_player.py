from unittest import TestCase
from ..game import Board, Player


class TestBoard(TestCase):
    def test_player_can_place_ships(self):
        """ Test the board can place available ships. """
        board = Board()
        player = Player(board=board)

        y = 0
        while len(player.ships_to_place) > 0:
            player.place_ship(player.ships_to_place[0], 0, y)
            y += 1

    def test_player_cant_place_more_ships_than_allowed(self):
        """ Test the player can't place ships they're not allowed to. """
        board = Board()
        player = Player(board=board)

        y = 0
        while len(player.ships_to_place) > 0:
            player.place_ship(player.ships_to_place[0], 0, y)
            y += 1

        with self.assertRaises(Player.CannotPlaceShip):
            player.place_ship(1, 0, y)
