from random import choice
from typing import List

from Chess.Board.MoveRecord import MoveRecord
from Chess.Repository.ChessRepository import ChessRepository
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor
from Chess.Pieces.king import King
from Chess.Pieces.knight import Knight
from Chess.Pieces.pawn import Pawn
from Chess.Pieces.piece import Piece
from Chess.Pieces.queen import Queen
from Chess.Pieces.rook import Rook
from Chess.utils.move_handlers import process_algebraic_notation, process_location, convert_to_algebraic_notation, \
    print_board


class GameState:
    def __init__(self, chess_repository: ChessRepository):
        self.board: ChessRepository = chess_repository
        self.move_stack: List[MoveRecord]  = []
        self.king_pieces = self._find_kings()

    def _find_kings(self):
        """ Finds both kings on the board and stores them in the king_pieces dictionary

        :return: None
        """
        kings = {}

        for piece in self.board.pieces:
            if isinstance(piece, King):
                kings[piece.color] = piece

        return kings

    def make_move(self, move: str):
        """ Make a move on the board

        :param move: The move to make
        :return: None
        """
        # Update the half-move counter
        self.board.half_moves += 1

        # Calculate the start and end squares
        end, start = process_algebraic_notation(move)

        # Get the piece at the start square
        piece: Piece | King = self.board.board[start[0]][start[1]]

        # Check if the piece is the correct color
        if piece is None:
            raise IllegalMove(convert_to_algebraic_notation(start) + " is empty")
        if piece.color != self.board.turn:
            raise WrongColor("That's not your piece!")
        # Check if the move is legal
        if end not in piece.get_legal_moves(self.board.board, self.board.history, self.board.pieces):
            raise IllegalMove("That move is illegal!")

        captured_piece = self.board.board[end[0]][end[1]]
        old_castling_rights = tuple(piece.castling_rights) if isinstance(piece, King) else (False, False)

        move_record = MoveRecord(start_row=start[0], start_col=start[1], end_row=end[0], end_col=end[1],
                                 moved_piece=piece, captured_piece=captured_piece, old_castling_rights=old_castling_rights, old_en_passant_square=None, old_half_moves=self.board.half_moves, old_turn=self.board.turn)

        self._push_move(move_record)
        self._do_move(move_record)

        # Check if king is in check
        king = self.king_pieces[self.board.turn]
        if king.is_in_check(self.board.board, self.board.pieces, self.board.history):
            # Revert
            self._undo_move()
            raise IllegalMove("Move leaves your king in check")

        # Castling rights
        if isinstance(piece, Rook):
            # Remove the castling rights if the rook moves
            if start == (0, 0) or start == (7, 0):
                king.castling_rights[0] = False
            if start == (0, 7) or start == (7, 7):
                king.castling_rights[1] = False

        if (king.castling_rights[0] or king.castling_rights) and isinstance(piece, King):
            # Check if the move is a castling move
            if isinstance(piece, King) and abs(end[1] - start[1]) == 2 and (
                    king.castling_rights[0] or king.castling_rights[1]):
                # Check if there are pieces between the king and the rook
                if end[1] > 4 and self.board.board[end[0]][end[1] - 1] is not None and self.board.board[end[0]][
                    end[1] - 2] \
                        is not None:
                    raise IllegalMove("You can't castle through pieces!")
                if end[1] < 4 and self.board.board[end[0]][end[1] + 1] is not None and self.board.board[end[0]][
                    end[1] + 2] \
                        is not None:
                    raise IllegalMove("You can't castle through pieces!")
                # If there are no pieces between the king and the rook, check the castling rights
                elif end not in king.get_legal_moves(self.board.board, self.board.history, self.board.pieces):
                    raise IllegalMove(f'You don\'t have the right to castle '
                                      f'{"king" if king.castling_rights[0] else "queen"} side!')

                # If the king is not in check and there are no pieces between the king and the rook, castle
                else:
                    # Move the rook
                    if end[1] == 6:
                        if self.board.board[end[0]][7] is None:
                            raise IllegalMove("Something went wrong")
                        self.board.board[end[0]][7].position = (end[0], 5)
                        self.board.board[end[0]][5] = self.board.board[end[0]][7]
                        self.board.board[end[0]][7] = None
                    else:
                        if self.board.board[end[0]][0] is None:
                            raise IllegalMove("Something went wrong")
                        self.board.board[end[0]][0].position = (end[0], 3)
                        self.board.board[end[0]][3] = self.board.board[end[0]][0]
                        self.board.board[end[0]][0] = None

            # Remove the castling rights
            king.castling_rights[0] = False
            king.castling_rights[1] = False

        # Check if the move is an en passant capture
        if isinstance(piece, Pawn) and self.board.board[end[0]][end[1]] is None and end[1] != start[1]\
                and isinstance(self.board.board[start[0]][end[1]], Pawn) and self.board.board[start[0]][end[1]].color != \
                self.board.turn:
            # If the pawn moves diagonally and there is no piece at the end square, it is an en passant capture
            self.board.board[start[0]][end[1]] = None

        # Move the piece
        self.board.board[start[0]][start[1]] = None
        self.board.board[end[0]][end[1]] = piece
        piece.position = end
        if isinstance(piece, Pawn):
            self.board.half_moves = 0

        # Check if the move is a pawn promotion
        if isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7):
            # Check if the piece is a pawn and if it is on the last rank
            # If it is, promote it
            self.board.board[start[0]][start[1]] = None
            self.board.board[end[0]][end[1]] = Queen(piece.color, end)

        # Update the board.history
        self.board.history = move

        # Update the turn
        self.board.turn = "b" if self.board.turn == "w" else "w"

        # Update the list of pieces
        self.board.pieces = [piece for row in self.board.board for piece in row if piece is not None]
        self.board.number_of_moves += 1

        legal_moves_for_current_player = self.possible_moves()

        # Check if the game is over
        self._check_game_status()

        # Check if the game is over due to insufficient material
        if self.is_insufficient_material():
            self.board.game_over = True
            self.board.result = 0.5
            raise Checkmate(f'Game over: 1/2-1/2!')

        # Check if the game is over due to the 50-move rule
        if self.board.half_moves == 100:
            self.board.game_over = True
            self.board.result = 0.5
            raise Checkmate(f'Game over: 1/2-1/2!')

        # TODO: Check if the game is over due to threefold repetition

    def _push_move(self, move: MoveRecord):
        """ Push a move to the move stack

        :param move: The move to push
        :return: None
        """
        self.move_stack.append(move)

    def _pop_move(self):
        """ Pops a move from the move stack

        :return: The move popped
        """
        if not self.move_stack:
            raise Exception("There are no moves to pop!")
        return self.move_stack.pop()

    def _do_move(self, move: MoveRecord):
        """ Plays out a move on the board

        :param move: The move to play
        :return: None
        """
        # If the move is a capture, remove the captured piece from the board
        captured_piece = self.board.board[move.end_row][move.end_col]
        if captured_piece is not None:
            self.board.remove_piece(captured_piece)

        # Update the board
        self.board.board[move.end_row][move.end_col] = move.moved_piece
        self.board.board[move.start_row][move.start_col] = None

        # Parse the move (to get the algebraic notation)
        algebraic_notation = convert_to_algebraic_notation((move.start_row, move.start_col)) + convert_to_algebraic_notation((move.end_row, move.end_col))
        self.board.history.append(algebraic_notation)
        move.moved_piece.position = (move.end_row, move.end_col)


    def _undo_move(self):
        """ Undoes the last move on the board

        :return: None
        """
        if not self.move_stack:
            raise IllegalMove("There are no moves to undo!")

        move = self.move_stack.pop()
        # Undo the move
        self.board.board[move.start_row][move.start_col] = move.moved_piece
        move.moved_piece.position = (move.end_row, move.end_col)

        # Restore the captured piece (if any)
        self.board.board[move.end_row][move.end_col] = move.captured_piece

        if move.captured_piece is not None:
            self.board.pieces.append(move.captured_piece)
        move.moved_piece.position = (move.start_row, move.start_col)

        # Restore the turn
        self.board.turn = move.old_turn

        # Parse the move (to get the algebraic notation)
        algebraic_notation = convert_to_algebraic_notation((move.start_row, move.start_col)) + convert_to_algebraic_notation((move.end_row, move.end_col))
        self.board.history.remove(algebraic_notation)

    def _check_game_status(self):
        """ Check if the game is over

        :return: None
        """

        possible_moves_for_current_player = self.possible_moves()
        if not possible_moves_for_current_player:
            # Check if the game is over due to checkmate
            if self.king_pieces[self.board.turn].is_in_check(self.board.board, self.board.pieces, self.board.history):
                self.board.game_over = True
                self.board.result = 1 if self.board.turn == "b" else 0
                raise Checkmate(f'Game over: {"1-0" if self.board.turn == "b" else "0-1"}!')

            # Check if the game is over due to stalemate
            else:
                self.board.game_over = True
                self.board.result = 0.5
                raise Checkmate(f'Game over: 1/2-1/2!')



    def get_board(self):
        """ Returns the board

         :return: The board"""
        return self.board

    def get_legal_moves(self, start):
        """ Returns the legal moves for the piece at the start square

         :param start: The start square
         :return: The list of legal moves"""
        start = process_location(start)
        piece: Piece | King = self.board.board[start[0]][start[1]]
        if piece is None:
            raise IllegalMove("There is no piece at the start location!")
        return piece.get_legal_moves(self.board.board, self.board.history, self.board.pieces)

    def possible_moves(self):
        """
        Return all truly legal moves for the current player, filtering out any moves
        that would leave or keep that player's own king in check.
        """
        candidate_moves = []
        # 1) Gather all piece-level moves (all pseudo-legal moves)
        for piece in self.board.pieces:
            if piece.color == self.board.turn:
                start_algebraic = convert_to_algebraic_notation(piece.position)
                for end_pos in piece.get_legal_moves(
                        self.board.board,
                        self.board.history,
                        self.board.pieces
                ):
                    move_str = start_algebraic + convert_to_algebraic_notation(end_pos)
                    candidate_moves.append(move_str)

        # 2) Simulate each move and check if the king is in check
        legal_moves = []
        for move in candidate_moves:
            move_record = MoveRecord(
                start_row=process_location(move[:2])[0],
                start_col=process_location(move[:2])[1],
                end_row=process_location(move[2:])[0],
                end_col=process_location(move[2:])[1],
                moved_piece=self.board.board[process_location(move[:2])[0]][process_location(move[:2])[1]],
                captured_piece=self.board.board[process_location(move[2:])[0]][process_location(move[2:])[1]],
                old_castling_rights=(False, False),
                old_en_passant_square=None,
                old_half_moves=self.board.half_moves,
                old_turn=self.board.turn
            )

            # Simulate the move
            self._push_move(move_record)
            self._do_move(move_record)

            # Check if the king is in check
            if self.king_pieces[move_record.old_turn].is_in_check(self.board.board, self.board.pieces, self.board.history):
                # If yes, revert
                self._undo_move()
                continue

            # If the move was legal, add it to the list of legal moves
            self._undo_move()
            legal_moves.append(move)

        return legal_moves

    def play_random_move(self, moves=None):
        """ Play a random legal move

         :param moves: A list of moves to choose from"""
        if moves is None:
            moves = self.possible_moves()
        if moves:
            move = choice(moves)
            try:
                self.make_move(move)
            except IllegalMove:
                moves.remove(move)
                self.play_random_move(moves)

    def get_value(self) -> float:
        """ Return the value of the board. Positive if white is winning, negative if black is winning

         :return: The value of the board"""
        value = 0
        for piece in self.board.pieces:
            if piece.color == "w":
                if isinstance(piece, Pawn) or isinstance(piece, Knight):
                    value += piece.get_value(self.board.board, self.board.history)
                else:
                    value += piece.get_value()
            else:
                if isinstance(piece, Pawn) or isinstance(piece, Knight):
                    value -= piece.get_value(self.board.board, self.board.history)
                else:
                    value -= piece.get_value()
        return value

    def get_result(self):
        """ Returns the result of the game

         :return: The result of the game"""
        return self.board.result

    def is_insufficient_material(self):
        """ Checks if there is enough material on the board to checkmate

         :return: True if there is not enough material to checkmate, False otherwise"""
        # Check if there is a rook, queen or pawn
        for piece in self.board.pieces:
            if isinstance(piece, Rook) or isinstance(piece, Queen) or isinstance(piece, Pawn):
                return False

        # We will split the pieces into two lists, one for each color
        white_pieces = [piece for piece in self.board.pieces if piece.color == "w"]
        black_pieces = [piece for piece in self.board.pieces if piece.color == "b"]
        # If there are only two pieces left (the two kings), the game is over
        if len(white_pieces) + len(black_pieces) == 2:
            return True

        # King and a minor piece against a king is a draw
        elif len(white_pieces) + len(black_pieces) == 3:
            return True

        # King and bishop or knight against a king and bishop or knight is a draw
        if len(white_pieces) == 2 and len(black_pieces) == 2:
            return True

        # King against a king and two knights is a draw
        if len(white_pieces) == 1 and len(black_pieces) == 3:
            for piece in black_pieces:
                if not isinstance(piece, Knight) or not isinstance(piece, King):
                    return True

        if len(white_pieces) == 3 and len(black_pieces) == 1:
            for piece in white_pieces:
                if not isinstance(piece, Knight) or not isinstance(piece, King):
                    return True

        # If there's enough material, the game is not over
        return False

    def fen(self):
        """ Returns the FEN representation of the board
         :return: The FEN representation of the board"""
        return self.board.fen()

    def game_over(self):
        return self.board.game_over

    def get_turn(self):
        return self.board.turn

if __name__ == "__main__":

    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    game = GameState(chess_repository)
    # game.make_move("d2d4")
    # Quick fool's mate to test
    moves = ["f2f4", "e7e5", "g2g4", "d8h4"]
    #moves = ["b1c3", "d7d5", "c3b5", "e7e5", "g1f3", "e5e4", "f3e5", "d8f6", "b5c7"]
    print(game.get_board())
    for move in moves: #['f2f3', 'e7e5', 'a2a3', 'd7d5', 'd2d4', 'g7g5', 'b1d2', 'd8e7', 'd2b1', 'e7e6', 'e2e3', 'b8d7', 'e1d2', 'f7f5', 'h2h4', 'f8c5', 'c2c3', 'c5b4', 'd1e1', 'e8f8', 'e1g3', 'b4d6', 'c3c4', 'd6a3', 'g3e5', 'e6e8', 'a1a2', 'g8e7', 'e5h2', 'f8g8', 'd2d3', 'd7c5', 'd3c3', 'c8e6', 'h2e5', 'a8b8', 'b1d2', 'a3b2', 'c3b2', 'c5a6', 'f1e2', 'e7g6', 'e3e4', 'a6b4', 'b2a3', 'b8a8', 'e5d5', 'f5e4', 'g1h3', 'e8a4', 'a3b2', 'b4d5', 'd2e4', 'a7a6', 'h1h2', 'a4a3', 'a2a3', 'a8e8', 'h3g1', 'd5c3', 'a3a4', 'a6a5', 'h2h1', 'e8d8', 'c4c5', 'c3b1', 'f3f4', 'e6f7', 'h1h3', 'd8a8', 'e2d3', 'g8g7', 'h3h2', 'f7e6', 'g1e2', 'b1d2', 'c1d2', 'g7h6', 'a4a3', 'e6g4', 'a3a5', 'g5h4', 'e4c3', 'a8a7', 'a5a2', 'g6e7', 'f4f5', 'h6h5', 'a2a5', 'h8c8', 'e2g3']:
       game.make_move(move)
       print_board(game.board)
    print(game.fen())

    while True:
        try:
            game.make_move(input("The move:"))
            print_board(game.board)
        except IllegalMove as e:
            print(e)
        except WrongColor as e:
            print(e)
        except Checkmate as e:
            print(e)
            break
