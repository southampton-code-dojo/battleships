from unittest import TestCase
from ..game import Board

EMPTY_BOARD_STR = "          \n" * 9 + " " * 10
EMPTY_BOARD = [[None]*10]*10


class TestBoard(TestCase):
    def test_board_empty_state(self):
        """ Test the board's empty state is correct. """
        board = Board()
        self.assertEquals(board.current_state(), EMPTY_BOARD)

    def test_board_displays_empty_output(self):
        """ Test that a board can output an empty display. """
        board = Board()
        output = str(board)
        # 10 empty rows
        self.assertEquals(output, EMPTY_BOARD_STR)

    def test_board_can_place_single_ship(self):
        """ Test that board can place a ship. """
        board = Board()
        board.place_ship(1, 0, 0)
        self.assertEquals(board.ships[0]["size"], 1)
        self.assertEquals(board.ships[0]["coordinates"], [[0, 0]])

        state = board.current_state()
        self.assertEquals(state[0][0], 1)
