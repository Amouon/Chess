import cProfile
import io
import pstats

import dill as pickle
import time

from Chess.Board.GameState import GameState
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Repository.ChessRepository import ChessRepository
from Chess.utils.move_handlers import print_board
from Common.hash_table import HashTable

class Minimax:
    def __init__(self, state: GameState, depth: int, color: str):
        """Minimax algorithm with alpha-beta pruning and transposition table."""
        self.state = state
        self.depth = depth
        self.hashtable = HashTable()
        self.color = 1 if color == "w" else -1

    def _min_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        fen = state.fen()
        hash_lookup = self.hashtable.lookup(fen)
        if hash_lookup is not None:
            return hash_lookup[0] * self.color
        if depth == 0 or state.game_over():
            return state.get_value() * self.color
        value = float('inf')
        best_move = None
        for move in state.possible_moves():
            child_state = pickle.loads(pickle.dumps(state, -1))
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if state.repository.turn == "w":
                    return float('inf')
                return float('-inf')
            child_value = self._max_value(child_state, depth - 1, alpha, beta)
            if child_value < value:
                value = child_value
                best_move = move
            if value <= alpha:
                break
            beta = min(beta, value)
        self.hashtable.store(fen, value, best_move)
        return value * self.color

    def _max_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        fen = state.fen()
        hash_lookup = self.hashtable.lookup(fen)
        if hash_lookup is not None:
            return hash_lookup[0] * self.color
        if depth == 0 or state.game_over():
            return state.get_value() * self.color
        value = float('-inf')
        best_move = None
        for move in state.possible_moves():
            child_state = pickle.loads(pickle.dumps(state, -1))
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if state.repository.turn == "w":
                    return float('-inf')
                return float('inf')
            child_value = self._min_value(child_state, depth - 1, alpha, beta)
            if child_value > value:
                value = child_value
                best_move = move
            if value >= beta:
                break
            alpha = max(alpha, value)
        self.hashtable.store(fen, value, best_move)
        return value * self.color

    def select_move(self, state: GameState) -> str:
        """ Select the best move from the current state
         :param state: The current state
         :return: The best move """
        self.state = state
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in self.state.possible_moves():
            child_state: GameState = pickle.loads(pickle.dumps(self.state, -1))
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if self.state.repository.turn == "w":
                    return move
                return move
            if self.hashtable.lookup(child_state.fen()):
                value = self.hashtable.lookup(child_state.fen())[0]
            else:
                value = self._min_value(child_state, self.depth - 1, alpha, beta)
            self.hashtable.store(child_state.fen(), value, move)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move  # , best_value


def profile_function(func, *args, label="PROFILE"):
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args)
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')  # Sort by total time spent in function
    ps.print_stats(20)  # Show top 20 functions
    print(f"\n[PROFILE: {label}]")
    print(s.getvalue())
    return result

if __name__ == "__main__":
    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    game_state = GameState(chess_repository)
    minimax_white = Minimax(game_state, 2, "w")
    minimax_black = Minimax(game_state, 2, "b")

    while not game_state.game_over():
        move_white = profile_function(minimax_white.select_move, game_state, label="White")
        print("White move:", move_white)
        game_state.make_move(move_white)

        move_black = profile_function(minimax_black.select_move, game_state, label="Black")
        print("Black move:", move_black)
        game_state.make_move(move_black)

        print_board(game_state.repository)

