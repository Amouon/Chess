from Chess.Pieces.piece import Piece

BOARD_SIZE = 8
CENTRAL_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__("N", color, position)

    def get_legal_moves(self, board, move_history=None, pieces=None):
        """ Returns a list of legal moves for the knight. """
        legal_moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for offset in knight_moves:
            new_row, new_col = self._position[0] + offset[0], self._position[1] + offset[1]

            if self._is_within_board(new_row, new_col) and \
                    (board[new_row][new_col] is None or board[new_row][new_col].color != self.color):
                legal_moves.append((new_row, new_col))

        return legal_moves

    def _is_within_board(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_value(self, board, move_history=None) -> float:
        # TODO: Implement a better evaluation function
        # Evaluate the value of the knight based on its position and other factors
        return 3 + self.positional_value(board)

    def positional_value(self, board):
        """ Returns the positional value of the knight based on its position on the board"""
        knight_moves = self.get_legal_moves(board)
        knight_mobility_value = 0
        knight_control_value = 0
        knight_outpost_value = 0
        # Knight mobility value
        knight_mobility_value = len(knight_moves) * 0.1
        # Knight control value
        for square in knight_moves:
            if square in ["d4", "d5", "e4", "e5"]:
                knight_control_value += 0.1
        return knight_mobility_value + knight_control_value
