### Project overview
- This project is a fully functional chess game implemented in Python, that allows the users to play against a computer using various algorithms (MCTS and Minmax). It includes:
  - A chess repository class that manages the game board and the pieces
  - A game state class that handles the game logic
  - A MCTS class that implements the Monte Carlo Tree Search algorithm
  - A Minimax class that implements the Minimax algorithm
  - A GUI class that implements the graphical user interface
  - A UI class that implements the command line user interface
  - A CNN class that implements a convolutional neural network.
  
### Getting started
- Prerequisites:
  - Python 3.10.2 or newer
  - PyQT5.15 or newer
  - Tensorflow 2.6.0 or newer
- Running the project:
  - To run the project, you need to run the main.py file.
  - To switch between the command line and the graphical user interface, you need to change the value of the variable `use_gui` to `True` or `False` in the main.py file.
- Running the tests:
  - To run the tests, you need to run the test_runner.py file.
- Making moves:
  - To make moves in the command line interface, you need to enter the coordinates of the piece you want to move, and then the coordinates of the square you want to move it to.  For example, `d2d4` will move the piece on the `d2` square to the `d4` square.
  - To make moves in the graphical user interface, you need to click on the piece you want to move, and then click on the square you want to move it to.

### Code Structure
- [ChessRepository](Documentation/ChessRepository.md): Handles the game board and pieces, each chess piece has its own class.
- [GameState](Documentation/GameState.md): Implements game logic and rules.
- [MCTS](Documentation/MCTS.md): Implements Monte Carlo Tree Search algorithm for AI.
  - [MCTSNode](Documentation/MCTSNode.md): Implements the node of the MCTS tree.
- [Minimax](Documentation/Minimax.md): Implements Minimax algorithm for AI.
- [HashTable](Documentation/HashTable.md): Implements a hash table used for the MCTS & Minimax algorithms.
  - [PrimeHandler](Documentation/PrimeHandler.md): Implements a class that handles prime numbers needed for the hash table.
- `GUI`: Implements the graphical user interface.
- [UI](Documentation/UI.md): Implements the command line user interface.
- [Piece](Documentation/Pieces.md): Base class for all chess pieces.
  - `Pawn`: Implements Pawn's specific behavior.
  - `Rook`: Implements Rook's specific behavior.
  - `Knight`: Implements Knight's specific behavior.
  - `Bishop`: Implements Bishop's specific behavior.
  - `Queen`: Implements Queen's specific behavior.
  - `King`: Implements King's specific behavior.
- [ConvolutionalNeuralNetwork](Documentation/ConvolutionalNeuralNetwork.md): Implements a convolutional neural network.
  - [TensorConverter](Documentation/TensorConverter.md): Implements a class that converts a chess board to a tensor.

### Documentation
- For more information about the classes and methods, you can find their documentation in the Documentation folder, or by clicking on the links above.

### Achievements
- The original project was awarded the "Best of Fundamentals of Programming" distinction by my university, received only by seven projects that year (from a total of 620 projects).

