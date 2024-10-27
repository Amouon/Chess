## Monte Carlo Tree Search
- This contains the documentation for the MCTS class.

### Monte Carlo Tree Search (MCTS)
- The MCTS class implements the Monte Carlo Tree Search algorithm. The algorithm has alpha-beta pruning, hashtables and a transposition table implemented to speed up the search.

#### Properties
- `iterations`: The number of iterations that the algorithm will run.
- `exploration_constant`: The exploration constant that is used in the UCB1 formula, sqrt(2) by default.
- `root`: The root node of the tree. It is an object of the MCTSNode class.
- `hashtable`: An object of the HashTable class that is used to store the nodes of the tree.
- `current_node`: The current node of the tree. It is an object of the MCTSNode class.
- `depth_limit`: The depth limit of the tree. It is used to limit the depth of the tree.
- `use_opening_book`: A boolean value that indicates if the opening book will be used.
- `opening_book`: A dictionary that stores the opening book.

#### Methods
- `set_current_node(state)`: Sets the current node to the one corresponding to the given state
- `select(node, depth)`: Selects the next node to explore using the UCB1 algorithm
- `expand(node)`: Expands the selected node by adding all the possible children nodes
- `simulate(node)`: Simulates a random game from the selected node
- `backpropagate(node, result)`: Backpropagates the result of the simulation from the terminal node to the root node
- `select_move(state)`: Performs the MCTS algorithm and selects the best move
