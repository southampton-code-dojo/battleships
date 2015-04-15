from unittest import TestCase
from ..game import Board, VERTICAL


class TestBoard(TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_empty_state(self):
        """ Test the board's empty state is correct. """
        EMPTY_BOARD = [[None]*10]*10
        self.assertEquals(self.board.current_state(), EMPTY_BOARD)

    def test_board_displays_empty_output(self):
        """ Test that a board can output an empty display. """
        output = str(self.board)
        # 10 empty rows
        EMPTY_BOARD_STR = "          \n" * 9 + " " * 10
        self.assertEquals(output, EMPTY_BOARD_STR)

    def test_board_can_place_single_ship(self):
        """ Test that board can place a ship. """
        self.board.place_ship(1, 0, 0)
        self.assertEquals(self.board.ships[0]["size"], 1)
        self.assertEquals(self.board.ships[0]["coordinates"], [[0, 0]])

        self.assertEquals(self.board.ship_at_position(0, 0), self.board.ships[0])

        state = self.board.current_state()
        self.assertEquals(state[0][0], 1)

        self.assertEquals(str(self.board), "1         \n" +
                                           "          \n" * 8 +
                                           "          ")

    def test_board_can_place_large_ship(self):
        """ Test that the board can place a 5 width ship. """
        self.board.place_ship(5, 0, 0)
        self.assertEquals(self.board.ships[0]["size"], 5)

        expected_coordinates = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(self.board.ships[0]["coordinates"],
                          expected_coordinates)
        state = self.board.current_state()

        for x in range(5):
            self.assertEquals(self.board.ship_at_position(x, 0)['size'], 5)
            self.assertEquals(state[x][0], 5)

        self.assertEquals(str(self.board), "55555     \n" +
                                           "          \n" * 8 +
                                           "          ")

    def test_can_place_multiple_ships(self):
        """ Test that we can place multiple ships. """
        self.board.place_ship(1, 0, 0)
        self.board.place_ship(5, 2, 2)
        self.assertEquals(self.board.ships[0]["size"], 1)
        self.assertEquals(self.board.ships[0]["coordinates"], [[0, 0]])
        self.assertEquals(self.board.ships[1]["size"], 5)
        self.assertEquals(self.board.ships[1]["coordinates"], [[2, 2], [3, 2],
                                                               [4, 2], [5, 2],
                                                               [6, 2]])

        self.assertEquals(self.board.ship_at_position(0, 0),
                          self.board.ships[0])

        for x in range(2, 7):
            self.assertEquals(self.board.ship_at_position(x, 2),
                              self.board.ships[1])

        state = self.board.current_state()
        self.assertEquals(state[0][0], 1)

        self.assertEquals(state[2][2], 5)
        self.assertEquals(state[3][2], 5)
        self.assertEquals(state[4][2], 5)
        self.assertEquals(state[5][2], 5)
        self.assertEquals(state[6][2], 5)

        self.assertEquals(str(self.board), "1         \n" +
                                           "          \n" +
                                           "  55555   \n" +
                                           "          \n" * 6 +
                                           "          ")

    def test_can_place_vertical_ship(self):
        """ Test that a board can support vertical ships. """
        self.board.place_ship(5, 0, 0, VERTICAL)
        self.assertEquals(self.board.ships[0]["size"], 5)

        expected_coordinates = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]
        self.assertEquals(self.board.ships[0]["coordinates"],
                          expected_coordinates)
        state = self.board.current_state()

        for y in range(5):
            self.assertEquals(self.board.ship_at_position(0, y)['size'], 5)
            self.assertEquals(state[0][y], 5)

        self.assertEquals(str(self.board), "5         \n" * 5 +
                                           "          \n" * 4 +
                                           "          ")

    def test_board_cant_overlap_ships(self):
        """ Test that we can't overlap ships. """
        self.board.place_ship(1, 5, 5)

        # Simple version
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(1, 5, 5)

        # More complicated
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(5, 3, 5)

    def test_ships_cant_go_out_of_bounds(self):
        """ Test that ships can't go out of bounds. """

        # Simple tests
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(1, -1, 0)
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(1, 0, -1)
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(1, 10, 9)
        with self.assertRaises(self.board.CannotPlaceShip):
            self.board.place_ship(1, 9, 10)

        # Test that we can place at the boundary
        self.board.place_ship(1, 9, 9)
        self.assertEquals(self.board.ships[0]["size"], 1)

    def test_shoot_miss(self):
        """ Test that shooting and missing will have no effect. """
        self.board.place_ship(5, 0, 0)

        self.assertEquals(self.board.shoot(5, 5), None)

        # Check that this changed nothing
        self.assertEquals(self.board.ships[0]["size"], 5)
        expected_coordinates = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(self.board.ships[0]["coordinates"],
                          expected_coordinates)

    def test_shoot_ship(self):
        """ Test that shooting a ship will be recorded. """
        self.board.place_ship(5, 0, 0)

        self.assertEquals(self.board.shoot(3, 0)["size"], 5)
        expected_coordinates = [[0, 0], [1, 0], [2, 0], [4, 0]]
        self.assertEquals(self.board.ships[0]["coordinates"],
                          expected_coordinates)
        self.assertEquals(self.board.ships[0]["destroyed_coordinates"],
                          [[3, 0]])
        self.assertEquals(self.board.ship_at_position(3, 0), None)
        self.assertEquals(self.board.wreckage_at_position(3, 0)["size"], 5)

        self.assertEquals(self.board.current_state()[3][0], "5x")
        self.assertEquals(str(self.board), "555x5     \n" +
                                           "          \n" * 8 +
                                           "          ")

    def test_destroy_ship(self):
        """ Test that destroying a ship entirely will remove it. """
        self.board.place_ship(5, 0, 0)

        self.assertEquals(self.board.shoot(0, 0)["size"], 5)
        self.assertEquals(self.board.shoot(1, 0)["size"], 5)
        self.assertEquals(self.board.shoot(2, 0)["size"], 5)
        self.assertEquals(self.board.shoot(3, 0)["size"], 5)

        ship = self.board.shoot(4, 0)
        self.assertEquals(ship["size"], 5)

        self.assertEquals(len(self.board.ships), 0)
        self.assertEquals(len(self.board.destroyed_ships), 1)

        expected_destroyed = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
        self.assertEquals(ship["coordinates"], [])
        self.assertEquals(ship["destroyed_coordinates"], expected_destroyed)

        self.assertEquals(self.board.current_state()[0][0], "5x")
        self.assertEquals(self.board.current_state()[1][0], "5x")
        self.assertEquals(self.board.current_state()[2][0], "5x")
        self.assertEquals(self.board.current_state()[3][0], "5x")
        self.assertEquals(self.board.current_state()[4][0], "5x")

        self.assertEquals(str(self.board), "xxxxx     \n" +
                                           "          \n" * 8 +
                                           "          ")

    def test_has_lost(self):
        """ Board knows when it has lost. """

        # Board is in losing position until a ship is placed
        self.assertTrue(self.board.has_lost)

        self.board.place_ship(1, 0, 0)

        self.assertFalse(self.board.has_lost)

        self.board.shoot(0, 0)

        self.assertTrue(self.board.has_lost)
