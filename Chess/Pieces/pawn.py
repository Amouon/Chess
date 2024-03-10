from Chess.Pieces.piece import Piece
from Chess.utils.move_handlers import process_algebraic_notation

BOARD_SIZE = 8


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__("P", color, position)

    def get_legal_moves(self, board, move_history, pieces=None):
        """ Returns a list of legal moves for the pawn. """
        direction = 1 if self.color == "w" else -1
        moves = self._straight_moves(board, direction)
        moves.extend(self._diagonal_moves(board, direction))
        moves.extend(self._en_passant(board, move_history, direction))
        return moves

    def _straight_moves(self, board, direction):
        """ Returns a list of straight moves for the pawn. """
        moves = []
        row, col = self._position[0] + direction, self._position[1]

        if self._is_within_board(row, col) and board[row][col] is None:
            moves.append((row, col))

            # Double move from the starting position
            if self._at_starting_position():
                row += direction
                if board[row][col] is None:
                    moves.append((row, col))

        return moves

    def _diagonal_moves(self, board, direction):
        """ Returns a list of diagonal moves for the pawn. """
        moves = []
        for col_offset in [-1, 1]:
            row, col = self._position[0] + direction, self._position[1] + col_offset
            if self._is_within_board(row, col) and board[row][col] and board[row][col].color != self.color:
                moves.append((row, col))
        return moves

    def _en_passant(self, board, move_history, direction):
        """ Returns a list of en passant moves for the pawn. """
        moves = []
        if move_history:
            last_move_end, last_move_start = process_algebraic_notation(move_history[-1])
            if abs(last_move_end[0] - last_move_start[0]) == 2 \
                    and self._position[0] == last_move_end[0] \
                    and abs(self._position[1] - last_move_end[1]) == 1:
                moves.append((last_move_start[0], last_move_end[1]))
        return moves

    def _is_within_board(self, row, col):
        """ Returns True if the given row and column are within the board, False otherwise. """
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def _at_starting_position(self):
        """ Returns True if the pawn is at its starting position, False otherwise. """
        return (self.color == "w" and self._position[0] == 1) or \
            (self.color == "b" and self._position[0] == 6)

    def get_value(self, board, move_history):
        """ Returns the value of the pawn based on its position on the board """
        return 1 + self.positional_value(board, move_history)

    def positional_value(self, board, move_history) -> float:
        """ Returns the positional value of the pawn based on its position on the board
            :param board: The current board state
            :param move_history: The history of moves made in the game
            :return: The positional value of the pawn """
        pawn_file = self.position[1]
        pawn_rank = self.position[0]
        pawn_color = self.color
        pawn_structure_value = 0
        pawn_mobility_value = 0
        pawn_protection_value = 0
        pawn_advancement_value = 0
        pawn_center_control_value = 0
        # Pawn structure value
        if pawn_rank in [3, 4]:
            pawn_structure_value += 0.1
        if pawn_color == "w":
            if self.position in [(3, 3), (3, 4)]:
                pawn_center_control_value += 0.1
        else:
            if self.position in [(4, 3), (4, 4)]:
                pawn_center_control_value += 0.1
        # Pawn mobility value
        pawn_mobility_value = len(self.get_legal_moves(board, move_history)) * 0.1
        # Pawn advancement value
        if pawn_color == "w":
            pawn_advancement_value = (8 - pawn_rank) * 0.1
        else:
            pawn_advancement_value = pawn_rank * 0.1
        return pawn_structure_value + pawn_mobility_value + pawn_protection_value + pawn_advancement_value + \
            pawn_center_control_value
