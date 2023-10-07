from Chess.Pieces.piece import Piece

BOARD_SIZE = 8


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__("B", color, position)

    def get_legal_moves(self, board, move_history=None, pieces=None):
        """ Generate the legal moves for the bishop """
        legal_moves = []
        direction_offsets = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for offset in direction_offsets:
            new_row, new_col = self._position[0] + offset[0], self._position[1] + offset[1]

            while self._is_within_board(new_row, new_col):
                if board[new_row][new_col] is None:
                    legal_moves.append((new_row, new_col))
                else:
                    if board[new_row][new_col].color != self.color:
                        legal_moves.append((new_row, new_col))
                    break  # Bishop's path is blocked by a piece (either friendly or enemy)

                new_row += offset[0]
                new_col += offset[1]

        return legal_moves

    def _is_within_board(self, row, col):
        """ Check if the given square is within the board """
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_value(self):
        # TODO: Implement a better evaluation function
        # Evaluate the value of the bishop based on its position and other factors
        return 3 # Hard coded value for now
