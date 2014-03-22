""" Battleships game components. """

# Use a 10x10 board
BOARD_SIZE = 10


class Board(object):

    """ A game board that contains ships """
    
    def current_state(self):
        """ Return or output the state of the board. """
        rows = []
        for y in range(BOARD_SIZE):
            current_row = ""
            for x in range(BOARD_SIZE):
                # TODO: Check if there is a ship in this position
                current_row += " "
            rows.append(current_row)
        return "\n".join(rows)
