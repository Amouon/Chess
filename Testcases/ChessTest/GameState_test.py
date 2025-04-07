import unittest

from Chess.Board.GameState import GameState
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Pieces.king import King
from Chess.Pieces.queen import Queen
from Chess.Repository.ChessRepository import ChessRepository


class GameStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ChessRepository()
        self.repository.initialize_board()
        self.game_state = GameState(self.repository)

    def test_possible_moves(self):
        self.assertEqual(len(self.game_state.possible_moves()), 20)  # 8 * 2 pawn moves + 2 * 2 knight moves

    def test_get_value(self):
        self.assertEqual(self.game_state.get_value(), 0.8000000000011367)

    def test_make_move(self):
        self.game_state.make_move("e2e4")

    def test_illegal_move(self):
        with self.assertRaises(IllegalMove):
            self.game_state.make_move("e2e5")

    def test_capture(self):
        self.game_state.make_move("e2e4")
        self.game_state.make_move("d7d5")
        self.game_state.make_move("e4d5")
        self.assertEqual(len(self.game_state.repository.pieces), 31)

    def test_king_check_simulation(self):
        self.game_state.make_move("f2f4")
        self.game_state.make_move("e7e5")
        self.game_state.make_move("h2h3")
        self.game_state.make_move("d8h4")
        with self.assertRaises(IllegalMove):
            self.game_state.make_move("a2a3")

    def test_checkmate(self):
        self.game_state.make_move("f2f4")
        self.game_state.make_move("e7e5")
        self.game_state.make_move("g2g4")
        with self.assertRaises(Checkmate):
            self.game_state.make_move("d8h4")

    def test_stalemate(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/3Q4/8/8/8/8/8/4K3 w - - 0 1")
        test_game_state = GameState(test_repository)
        with self.assertRaises(Checkmate):
            test_game_state.make_move("d7c7")

    def test_insufficient_material_kings(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/2K5/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), True)
        with self.assertRaises(Checkmate):
            test_game_state.make_move("c2c3")

    def test_insufficient_material_bishop(self):
        # With 3 pieces, draw
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/2KB4/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), True)

    def test_insufficient_material_pawn(self):
        # With 3 pieces, not a draw
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/2KP4/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), False)

    def test_insufficient_material_rook(self):
        # With 3 pieces, not a draw
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/2KR4/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), False)

    def test_insufficient_material_minor_vs_minor(self):
        # With 4 pieces, draw
        test_repository = ChessRepository()
        test_repository.initialize_board("kb6/8/8/8/8/8/2KN4/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), True)

    def test_insufficient_material_two_white_knights(self):
        # With 4 pieces, draw
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/2NNK3/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), True)

    def test_insufficient_material_two_black_knights(self):
        # With 4 pieces, draw
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/2nn4/8/8/8/8/2K5/8 b KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), True)

    def test_insufficient_material_more_than_two_pieces(self):
        # With 5 pieces, not a draw
        test_repository = ChessRepository()
        test_repository.initialize_board("kB6/8/8/8/8/8/2NBK3/8 w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        self.assertEqual(test_game_state.is_insufficient_material(), False)

    def test_castling(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        test_game_state = GameState(test_repository)
        test_game_state.make_move("e1g1")
        self.assertEqual(isinstance(test_game_state.repository.board[0][6], King), True)
        test_game_state.make_move("e8c8")
        self.assertEqual(isinstance(test_game_state.repository.board[7][2], King), True)

    def test_fen(self):
        self.assertEqual(self.game_state.fen(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_get_result(self):
        self.assertEqual(self.game_state.get_result(), None)

    def test_fifty_move_rule(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/8/8/8/8/8/8/KQ6 w - - 0 1")
        test_game_state = GameState(test_repository)
        with self.assertRaises(Checkmate):
            for move in ["a1a2", "a8a7", "a2a1", "a7a8"] * 25:
                test_game_state.make_move(move)

    def test_pawn_promotion(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/7P/8/8/8/8/8/4K3 w - - 0 1")
        test_game_state = GameState(test_repository)
        test_game_state.make_move("h7h8")
        self.assertEqual(isinstance(test_game_state.repository.board[7][7], Queen), True)

    def test_play_random_move(self):
        test_repository = ChessRepository()
        test_repository.initialize_board("k7/7p/7P/8/8/8/8/4K3 w - - 0 1")
        test_game_state = GameState(test_repository)
        test_game_state.play_random_move(["h6h7"])
        self.assertEqual(test_game_state.repository.board[0][0], None)


if __name__ == '__main__':
    unittest.main()
