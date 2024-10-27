## Monte Carlo Tree Search Node
- This contains the documentation for the MCTSNode class.

### MCTSNode (MCTSNode)
- The MCTSNode class implements a node in the Monte Carlo Tree Search tree.
- Each node contains information about the state of the game, the number of visits, the total value, the children nodes, and the parent node.
- The MCTSNode class is used by the MCTS class to build the search tree.
- The MCTSNode class also contains the `alpha` and `beta` values for the alpha-beta pruning algorithm.

#### Properties
- `state`: The GameState object that manages the game logic and the rules.
- `parent`: The parent node.
- `children`: A list of the children nodes.
- `move`: The move that was made to get to this node.
- `visits`: The number of times the node was visited.
- `wins`: The number of times the node was visited and the player won.
- `alpha`: The alpha value of the node.
- `beta`: The beta value of the node.

#### Methods
- `not_fully_expanded()`: Returns `True` if the node is not fully expanded and `False` otherwise.
- `ucb1(exploration_constant)`: Returns the UCB1 value of the node.