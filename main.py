from AI.CNN.ConvolutionalNeuralNetwork import ConvolutionalNeuralNetwork
from AI.MCTS.monte_carlo_tree_search import MCTS
from AI.Minimax.minimax import Minimax
from Chess.Board.GameState import GameState
from Chess.GUI.chess_gui import ChessGUI
from Chess.GUI.difficulty_gui import DifficultySelector
from Chess.Repository.ChessRepository import ChessRepository
from Chess.UI.console import UI

if __name__ == "__main__":
    use_gui = True
    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    game_state = GameState(chess_repository)
    cnn = ConvolutionalNeuralNetwork()
    cnn.load("AI/CNN/TrainedModels/cnn.h5")
    if use_gui is True:
        dif = DifficultySelector()
        difficulty, color = dif.get_difficulty()
        difficulty = difficulty.split(" ")
        algorithm = difficulty[0]
        difficulty = 2 if difficulty[1] == "Easy" else 5 if difficulty[1] == "Medium" else 10
        color = "w" if color == "White" else "b"

        print("Algorithm: ", algorithm)
        if algorithm == "Minimax":
            ai = Minimax(state=game_state, depth=difficulty, color="w")
        else:
            ai = MCTS(state=game_state, iterations=difficulty, depth_limit=None, use_opening_book=True, cnn=cnn)

        gui = ChessGUI(game_state, ai)
    else:
        ui = UI(game_state, cnn)
        ui.start()
