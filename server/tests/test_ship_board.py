from unittest import TestCase
from ..game import Board


class TestBoard(TestCase):
    def test_board_displays_empty_output(self):
        """ Test that a ship board can output an empty display. """
        board = Board()
        output = board.current_state()
        # 10 empty rows
        self.assertEquals(output, "          \n" * 9 + " " * 10)
