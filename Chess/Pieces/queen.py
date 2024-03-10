from Chess.Pieces.piece import Piece

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__("Q", color, position)

    def get_legal_moves(self, board, move_history=None, pieces=None):
        """ Generate the legal moves for the queen """
        legal_moves = []

        # Using the movement patterns of Rook and Bishop combined
        for row_offset, col_offset in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            new_row = self._position[0] + row_offset
            new_col = self._position[1] + col_offset

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target:
                    # If the square is occupied by an enemy, add it as a legal move and then break
                    if target.color != self.color:
                        legal_moves.append((new_row, new_col))
                    break
                else:
                    legal_moves.append((new_row, new_col))

                new_row += row_offset
                new_col += col_offset

        return legal_moves
    def get_value(self):
        # TODO: Implement a better evaluation function
        # Evaluate the value of the queen based on its position and other factors
        return 9  # Hard coded value for now
