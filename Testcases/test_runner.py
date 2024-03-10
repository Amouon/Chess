from unittest import TestSuite, TestLoader, TextTestRunner

from Testcases.AITest.mcts_test import MCTSTest
from Testcases.AITest.minimax_test import MinimaxTest
from Testcases.ChessTest.GameState_test import GameStateTest
from Testcases.ChessTest.PiecesTest.bishop_test import BishopTest
from Testcases.ChessTest.PiecesTest.king_test import KingTest
from Testcases.ChessTest.PiecesTest.knight_test import KnightTest
from Testcases.ChessTest.PiecesTest.pawn_test import PawnTest
from Testcases.ChessTest.PiecesTest.queen_test import QueenTest
from Testcases.ChessTest.PiecesTest.rook_test import RookTest
from Testcases.ChessTest.ChessRepository_test import ChessRepositoryTest
from Testcases.CommonTest.HashTable_test import HashTableTest
from Testcases.CommonTest.PrimeHandler_test import PrimeHandlerTest


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [
        # Tests the classes for the pieces
        RookTest, KnightTest, BishopTest, QueenTest, KingTest, PawnTest,
        # Test the classes for the board
        ChessRepositoryTest, GameStateTest,
        # Test the AI classes
        MCTSTest, MinimaxTest,
        # Test the classes from the Common package
        HashTableTest, PrimeHandlerTest
    ]

    loader = TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = TestSuite(suites_list)

    runner = TextTestRunner()
    results = runner.run(big_suite)


if __name__ == '__main__':
    run_some_tests()