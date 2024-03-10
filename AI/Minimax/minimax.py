import pickle
import dill
import time
from typing import Tuple

from AI.hash_table import HashTable
from Chess.Board.GameState import GameState
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Repository.ChessRepository import ChessRepository
from Chess.utils.move_handlers import print_board


class Minimax:
    def __init__(self, state: GameState, depth: int, color: str):
        """ Minimax algorithm with alpha-beta pruning and transposition table
         :param state: The current state
         :param depth: The depth of the search tree
         :param color: The color of the player"""

        self.state = state
        self.depth = depth
        self.hashtable = HashTable(1009)
        self.color = 1 if color == "w" else -1

    def _min_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        """ Find the minimum value for the current state
            :param state: The current state
            :param depth: The depth of the search tree
            :param alpha: The alpha value
            :param beta: The beta value
            :return: The minimum value for the current state"""
        if depth == 0 or state.game_over():
            return state.get_value() * self.color
        value = float('inf')
        for move in state.possible_moves():
            child_state = dill.copy(state)
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if state.board.turn == "w":
                    return float('inf')
                return float('-inf')
            # if self.hashtable.lookup(child_state):
            #    value = min(value, self.hashtable.lookup(child_state)[0])
            # else:
            value = min(value, self._max_value(child_state, depth - 1, alpha, beta))
            # self.hashtable.store(child_state, value, move)
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value * self.color

    def _max_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        """ Find the maximum value for the current state
            :param state: The current state
            :param depth: The depth of the search tree
            :param alpha: The alpha value
            :param beta: The beta value
            :return: The maximum value for the current state"""

        if depth == 0 or state.game_over():
            return state.get_value() * self.color
        value = float('-inf')
        for move in state.possible_moves():
            child_state = dill.copy(state)
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if state.board.turn == "w":
                    return float('-inf')
                return float('inf')
            # if self.hashtable.lookup(child_state):
            #    value = max(value, self.hashtable.lookup(child_state)[0])
            # else:
            value = max(value, self._min_value(child_state, depth - 1, alpha, beta))
            # self.hashtable.store(child_state, value, move)
            if value >= beta:
                return value
            alpha = max(alpha, value)
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
            child_state = dill.copy(self.state)
            try:
                child_state.make_move(move)
            except IllegalMove:
                continue
            except Checkmate:
                if self.state.board.turn == "w":
                    return move  # , float('-inf')
                return move  # , float('inf')
            # if self.hashtable.lookup(child_state):
            #     value = self.hashtable.lookup(child_state)[0]
            # else:
            value = self._min_value(child_state, self.depth - 1, alpha, beta)
            # self.hashtable.store(child_state, value, move)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move  # , best_value


if __name__ == "__main__":
    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    game_state = GameState(chess_repository)
    minimax_white = Minimax(game_state, 10, "w")
    minimax_black = Minimax(game_state, 10, "b")
    while not game_state.game_over():
        start = time.time()
        move = minimax_white.select_move(game_state)
        print(time.time() - start)
        print("White move: ", move)
        game_state.make_move(move)
        move = minimax_black.select_move(game_state)
        game_state.make_move(move)
        print("Black move: ", move)
        print_board(game_state.board)
