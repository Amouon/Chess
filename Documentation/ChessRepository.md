### ChessRepository
- The ChessRepository class is responsible for managing the game board and the pieces.

#### Properties
- `board`: A 2D array that represents the game board. Each element of the array is either a piece object or `None`.
- `pieces`: A list of all the pieces on the board.
- `history`: A list of all the moves that have been made in the game.
- `turn`: A string that indicates whose turn it is. It can be either `w` or `b`.
- `half_moves`: An integer that indicates the number of half moves that have been made since the last capture or pawn move.
- `number_of_moves`: An integer that indicates the number of moves that have been made in the game.
- `game_over`: A boolean that indicates whether the game is over or not.

#### Methods
- `initialize_board([fen])`: Initializes the board with the starting position or the position specified by the FEN string.
- `remove_piece(piece)`: Removes the piece from the board.
- `fen()`: Returns the FEN string of the current position.

#### Example

```python
chess_repository = ChessRepository()
chess_repository.initialize_board()
print(chess_repository.repository)
# Output: [[wR,   wN,   wB,   wQ,   wK,   wB,   wN,   wR  ],
#          [wP,   wP,   wP,   wP,   wP,   wP,   wP,   wP  ],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [bP,   bP,   bP,   bP,   bP,   bP,   bP,   bP  ],
#          [bR,   bN,   bB,   bQ,   bK,   bB,   bN,   bR  ]]

print(chess_repository.fen())
# Output: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

chess_repository.remove_piece(chess_repository.repository[0][0])
print(chess_repository.repository)
# Output: [[None, wN,   wB,   wQ,   wK,   wB,   wN,   wR  ],
#          [wP,   wP,   wP,   wP,   wP,   wP,   wP,   wP  ],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [None, None, None, None, None, None, None, None],
#          [bP,   bP,   bP,   bP,   bP,   bP,   bP,   bP  ],
#          [bR,   bN,   bB,   bQ,   bK,   bB,   bN,   bR  ]]
```