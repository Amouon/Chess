import json
import numpy as np


class TensorConverter:
    def __init__(self):
        # Create the mapping of the pieces
        self.piece_mapping = {'wR': 1, 'wN': 2, 'wB': 3, 'wQ': 4, 'wK': 5, 'wP': 6, None: 0,
                              'bR': 7, 'bN': 8, 'bB': 9, 'bQ': 10, 'bK': 11, 'bP': 12}

        # Create the mapping of the turns
        self.turn_mapping = {'w': 1, 'b': 0}

        # Create the mapping of the outcomes of the games
        self.result_mapping = {'1-0': 2, '0-1': 0, '1/2-1/2': 1}

        # Create the FEN mapping of the pieces
        self.fen_piece_mapping = {'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK', 'P': 'wP',
                                  'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK', 'p': 'bP'}

    def convert_board_from_fen(self, fen) -> list[list[str]]:
        """
        Convert the board from FEN notation to a 2D array
        :param fen: The FEN notation of the board
        :return: The 2D array of the board
        """
        fen = fen.split(' ')[0]
        converted_board = []
        for row in fen.split("/"):
            converted_row = []
            for piece in row:
                if piece.isdigit():
                    converted_row.extend([None] * int(piece))
                else:
                    converted_row.append(self.fen_piece_mapping[piece])
            converted_board = [converted_row] + converted_board
        return converted_board

    def load_and_convert_dataset(self, file_path):
        """
        Loads the dataset from a JSON file and converts the boards to 2D arrays
        :param file_path: The path to the JSON file containing the dataset
        :return: The dataset with the boards converted to 2D arrays
        """
        # Load the dataset from the JSON file
        with open(file_path, 'r') as f:
            dataset = json.load(f)
        # Convert the boards into 2D arrays
        for game in dataset["games"]:
            game["board"] = self.convert_board_from_fen(game["board"])

        # Return the dataset
        return dataset

    def convert(self, file_path):
        """
        Loads a dataset of games and creates the tensors of the boards, turns and outcome labels
        :return: The tensors of the board, the turns of the players and the outcome labels of the dataset
        """

        # Create the tensors
        board_tensor = []
        turn_tensor = []
        result_tensor = []

        # Load the dataset
        dataset = self.load_and_convert_dataset(file_path)

        # Iterate through the games
        for game in dataset["games"]:
            # Create a tensor of the board
            board_tensor.append(np.array([[self.piece_mapping[str(piece) if piece else None] for piece in row]
                                          for row in game["board"]]))

            # Create a tensor of the turn
            turn_tensor.append(np.array([self.turn_mapping[game["turn"]]]))

            # Create a tensor of the result labels
            result_tensor.append(np.array([self.result_mapping[game["result"]]]))

        # One-hot encode the result labels
        result_tensor = np.eye(3)[result_tensor]

        # Stack the board tensors, the turn tensors and the outcome tensors
        board_tensor = np.stack(board_tensor, axis=0)
        turn_tensor = np.stack(turn_tensor, axis=0)
        result_tensor = np.stack(result_tensor, axis=0)

        # Reshape the result tensor
        result_tensor = result_tensor.reshape((result_tensor.shape[0], -1))

        # Return the tensors
        return board_tensor, turn_tensor, result_tensor

    def convert_for_prediction(self, fen: str):
        """ Convert a board from FEN notation to a tensor for prediction.
        :param fen: The FEN notation of the board

        :return: The tensor of the board and the tensor of the turn
        """

        board_tensor = []

        # Obtain the turn from the FEN notation
        turn = fen.split(' ')[1]

        # Convert the FEN notation to a 2D array
        board = self.convert_board_from_fen(fen)

        # Create a tensor of the board
        board_tensor.append(np.array([[self.piece_mapping[str(piece) if piece else None] for piece in row]
                                      for row in board]))
        # Create a tensor of the turn
        turn_tensor = np.array([self.turn_mapping[turn]])

        # Stack the tensors
        board_tensor = np.stack(board_tensor, axis=0)
        turn_tensor = np.stack(turn_tensor, axis=0)

        # Return the tensors
        return board_tensor, turn_tensor

if __name__ == "__main__":
    converter = TensorConverter()
    print(converter.convert("Resources/testing_dataset.json"))
    print(converter.convert_for_prediction("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    # board_tensor, turn_tensor, result_tensor = converter.convert()