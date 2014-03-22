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

        self.assertEquals(board.ship_at_position(0, 0), board.ships[0])

        state = board.current_state()
        self.assertEquals(state[0][0], 1)

        self.assertEquals(str(board), "1         \n" +
                                      "          \n" * 8 +
                                      "          ")

    def test_board_can_place_large_ship(self):
        """ Test that the board can place a 5 width ship. """
        board = Board()
        board.place_ship(5, 0, 0)
        self.assertEquals(board.ships[0]["size"], 5)

        expected_coordinates = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(board.ships[0]["coordinates"], expected_coordinates)
        state = board.current_state()

        for x in range(5):
            self.assertEquals(board.ship_at_position(x, 0)['size'], 5)
            self.assertEquals(state[x][0], 5)

        self.assertEquals(str(board), "55555     \n" +
                                      "          \n" * 8 +
                                      "          ")

    def test_can_place_multiple_ships(self):
        """ Test that we can place multiple ships. """
        board = Board()
        board.place_ship(1, 0, 0)
        board.place_ship(5, 2, 2)
        self.assertEquals(board.ships[0]["size"], 1)
        self.assertEquals(board.ships[0]["coordinates"], [[0, 0]])
        self.assertEquals(board.ships[1]["size"], 5)
        self.assertEquals(board.ships[1]["coordinates"], [[2, 2], [3, 2],
                                                          [4, 2], [5, 2],
                                                          [6, 2]])

        self.assertEquals(board.ship_at_position(0, 0), board.ships[0])

        for x in range(2, 7):
            self.assertEquals(board.ship_at_position(x, 2), board.ships[1])

        state = board.current_state()
        self.assertEquals(state[0][0], 1)

        self.assertEquals(state[2][2], 5)
        self.assertEquals(state[3][2], 5)
        self.assertEquals(state[4][2], 5)
        self.assertEquals(state[5][2], 5)
        self.assertEquals(state[6][2], 5)

        self.assertEquals(str(board), "1         \n" +
                                      "          \n" +
                                      "  55555   \n" +
                                      "          \n" * 6 +
                                      "          ")

    def test_can_place_vertical_ship(self):
        """ Test that a board can support vertical ships. """
        pass

    def test_board_cant_overlap_ships(self):
        """ Test that we can't overlap ships. """
        pass

    def test_ships_cant_go_out_of_bounds(self):
        """ Test that ships can't go out of bounds. """
        pass

    def test_shoot_ship(self):
        """ Test that shooting a ship will be recorded. """
        pass

    def test_destroy_ship(self):
        """ Test that destroying a ship entirely will remove it. """
        pass
