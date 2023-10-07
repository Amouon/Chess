import pickle
from Chess.Pieces.piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__("K", color, position)
        self.castling_rights = [True, True]  # O-O, O-O-O

    def get_legal_moves(self, board, move_history, pieces):
        legal_moves = []
        enemy_pieces = [piece for piece in pieces if piece.color != self.color]
        row, col = self._position

        # Helper function to check if a move is valid for the king
        def check_move(new_row, new_col):
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                board_copy = pickle.loads(pickle.dumps(board, -1))
                if board_copy[new_row][new_col] is None or board_copy[new_row][new_col].color != self.color:
                    original_square = pickle.loads(pickle.dumps(self._position, -1))
                    board_copy[original_square[0]][original_square[1]], board_copy[new_row][new_col] = None, self
                    self._position = (new_row, new_col)
                    if not self.is_in_check(board_copy, enemy_pieces, move_history):
                        legal_moves.append((new_row, new_col))
                    self._position = original_square

        # Check the eight squares that the king can move to
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if not (row_offset == 0 and col_offset == 0):
                    check_move(row + row_offset, col + col_offset)

        # Check if the king can castle
        if self.castling_rights[0] and self.position == (row, 4):
            if all([board[row][i] is None for i in [col + 1, col + 2]]):
                check_move(row, col + 2)

        if self.castling_rights[1] and self.position == (row, 4):
            if all([board[row][i] is None for i in [col - 1, col - 2]]):
                check_move(row, col - 2)

        return legal_moves

    def is_in_check(self, board, pieces, move_history):
        enemy_moves = []
        for piece in pieces:
            if piece.color != self.color:
                enemy_moves.extend(piece.get_legal_moves(board, move_history, pieces))
        return self._position in enemy_moves

    def get_value(self):
        # TODO: Implement a better evaluation function
        return 1000  # Hard coded value for now
