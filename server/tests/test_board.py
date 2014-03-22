from unittest import TestCase
from ..game import Board, VERTICAL

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
        board = Board()
        board.place_ship(5, 0, 0, VERTICAL)
        self.assertEquals(board.ships[0]["size"], 5)

        expected_coordinates = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        self.assertEquals(board.ships[0]["coordinates"], expected_coordinates)
        state = board.current_state()

        for y in range(5):
            self.assertEquals(board.ship_at_position(0, y)['size'], 5)
            self.assertEquals(state[0][y], 5)

        self.assertEquals(str(board), "5         \n" * 5 +
                                      "          \n" * 4 +
                                      "          ")

    def test_board_cant_overlap_ships(self):
        """ Test that we can't overlap ships. """
        board = Board()
        board.place_ship(1, 5, 5)

        # Simple version
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(1, 5, 5)

        # More complicated
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(5, 3, 5)

    def test_ships_cant_go_out_of_bounds(self):
        """ Test that ships can't go out of bounds. """
        board = Board()

        # Simple tests
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(1, -1, 0)
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(1, 0, -1)
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(1, 10, 9)
        with self.assertRaises(board.CannotPlaceShip):
            board.place_ship(1, 9, 10)

        # Test that we can place at the boundary
        board.place_ship(1, 9, 9)
        self.assertEquals(board.ships[0]["size"], 1)

    def test_shoot_miss(self):
        """ Test that shooting and missing will have no effect. """
        board = Board()
        board.place_ship(5, 0, 0)

        self.assertEquals(board.shoot(5, 5), None)

        # Check that this changed nothing
        self.assertEquals(board.ships[0]["size"], 5)
        expected_coordinates = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(board.ships[0]["coordinates"], expected_coordinates)

    def test_shoot_ship(self):
        """ Test that shooting a ship will be recorded. """
        board = Board()
        board.place_ship(5, 0, 0)

        self.assertEquals(board.shoot(3, 0)["size"], 5)
        expected_coordinates = [[0, 0], [1, 0], [2, 0], [4, 0]]
        self.assertEquals(board.ships[0]["coordinates"], expected_coordinates)
        self.assertEquals(board.ships[0]["destroyed_coordinates"], [[3, 0]])
        self.assertEquals(board.ship_at_position(3, 0), None)
        self.assertEquals(board.wreckage_at_position(3, 0)["size"], 5)

        self.assertEquals(board.current_state()[3][0], "5x")
        self.assertEquals(str(board), "555x5     \n" +
                              "          \n" * 8 +
                              "          ")      

    def test_destroy_ship(self):
        """ Test that destroying a ship entirely will remove it. """
        board = Board()
        board.place_ship(5, 0, 0)

        self.assertEquals(board.shoot(0, 0)["size"], 5)
        self.assertEquals(board.shoot(1, 0)["size"], 5)
        self.assertEquals(board.shoot(2, 0)["size"], 5)
        self.assertEquals(board.shoot(3, 0)["size"], 5)

        ship = board.shoot(4, 0)
        self.assertEquals(ship["size"], 5)

        self.assertEquals(len(board.ships), 0)
        self.assertEquals(len(board.destroyed_ships), 1)

        expected_destroyed = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(ship["coordinates"], [])
        self.assertEquals(ship["destroyed_coordinates"], expected_destroyed)

        self.assertEquals(board.current_state()[0][0], "5x")
        self.assertEquals(board.current_state()[1][0], "5x")
        self.assertEquals(board.current_state()[2][0], "5x")
        self.assertEquals(board.current_state()[3][0], "5x")
        self.assertEquals(board.current_state()[4][0], "5x")

        self.assertEquals(str(board), "xxxxx     \n" +
                              "          \n" * 8 +
                              "          ")    
