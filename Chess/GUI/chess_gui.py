import sys

from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtCore import QEvent

from AI.MCTS.monte_carlo_tree_search import MCTS
from AI.Minimax.minimax import Minimax
from Chess.Repository.ChessRepository import ChessRepository
from Chess.Board.GameState import GameState
from Chess.utils.move_handlers import print_board
from Chess.Exceptions.Checkmate import Checkmate
from Chess.Exceptions.IllegalMoveException import IllegalMove
from Chess.Exceptions.WrongColor import WrongColor


class ChessGUI(QObject):
    def __init__(self, state: GameState, ai: MCTS | Minimax | None = None):
        super().__init__()
        self.chess = state
        self.ai = ai
        self.chess.make_move(ai.select_move(self.chess))
        self.app = QApplication(sys.argv)
        # Create the main window
        self.window = QMainWindow()
        self.window.setWindowTitle("ChessTest")
        self.window.setFixedSize(800, 800)

        # Create the central widget
        self.central_widget = QWidget(self.window)

        # Create the grid layout
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(0)

        # Create the instance variables to store the source and destination squares
        self.source = None
        self.destination = None

        self.source_square = None
        self.destination_square = None

        # Create the chess board
        self.characters = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

        for row in range(8):
            for col in range(8):
                square = QWidget(self.central_widget)
                square.setAccessibleDescription(self.characters[col] + str(8 - row))
                square.setStyleSheet("background-color: #F0D9B5;" if (col + row) % 2 == 0
                                     else "background-color: #B58863;")
                square.setFixedSize(100, 100)
                square.installEventFilter(self)
                self.grid_layout.addWidget(square, row, col)

        # Create the pieces
        self.pieces = []
        self.createPieces()

        # Set the central widget
        self.window.setCentralWidget(self.central_widget)

        # Show the main window
        self.window.show()

        # Run the application
        sys.exit(self.app.exec_())

    # ! This function is deprecated. And also it was quite cursed.
    # def unholyHandler(self, label, event):
    #     print('aaaaaaaaaaaaaa')
    #     if event.type() == QEvent.MouseButtonPress:
    #         print(label.text())

    def createPieces(self):
        """ Creates the pieces on the board """
        for col in self.chess.board.board:
            for element in col:
                if element is not None:
                    piece = QLabel(self.central_widget)

                    color_name = "white" if element.color == "w" else "black"
                    pixmap = QPixmap(f"Chess/Resources/{color_name}_{type(element).__name__.lower()}.png")
                    piece.setPixmap(pixmap)

                    piece.setAccessibleDescription(self.characters[element.position[1]] + str(element.position[0] + 1))
                    piece.installEventFilter(self)
                    self.grid_layout.addWidget(piece, 7 - element.position[0], element.position[1])
                    self.pieces.append(piece)
        return

    def recreate_pieces(self):
        """ Recreates the pieces on the board """
        for piece in self.pieces:
            self.grid_layout.removeWidget(piece)
        self.pieces = []
        self.createPieces()

    def eventFilter(self, source, event):
        """ Handles the events for the pieces and the squares

        :param source: The source of the event
        :param event: The event
        :return: True if the event was handled, False otherwise"""
        if event.type() == QEvent.MouseButtonPress:  # from PyQt5.QtCore import QEvent
            # print(source.accessibleDescription())
            if isinstance(source, QLabel):
                if self.source is None:
                    self.source = source
                    legal_moves = self.chess.get_legal_moves(source.accessibleDescription())
                    self.highlight_legal_moves(legal_moves)
                else:
                    error = None
                    self.remove_pending_moves()
                    try:
                        self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                    except IllegalMove as e:
                        error = e
                    except WrongColor as e:
                        error = e
                    except Checkmate as e:
                        print(e)
                        self.window.close()
                    # print_board(self.chess.get_board())
                    self.recreate_pieces()
                    # Clear the source square
                    self.source = None

                    if error is None and self.ai is not None:
                        from time import time
                        start = time()
                        move = self.ai.select_move(self.chess)
                        print(time() - start)
                        self.chess.make_move(move)
                        self.recreate_pieces()
                # self.grid_layout.removeWidget(source)
                # self.pieces.remove(source)
                # source.deleteLater()
            elif self.source is not None:
                self.remove_pending_moves()
                error = None
                try:
                    self.chess.make_move(self.source.accessibleDescription() + source.accessibleDescription())
                except IllegalMove as e:
                    error = e
                except WrongColor as e:
                    error = e
                except Checkmate as e:
                    print(e)
                    self.window.close()
                # print_board(self.chess.get_board())
                self.recreate_pieces()
                self.source = None

                if error is None and self.ai is not None:
                    from time import time
                    start = time()
                    move = self.ai.select_move(self.chess)
                    print(time() - start)
                    self.chess.make_move(move)
                    self.recreate_pieces()
            else:
                self.source = None

        return super().eventFilter(source, event)

    def highlight_legal_moves(self, legal_moves):
        """ Highlights the legal moves for the piece on the board

         :param legal_moves: A list of legal moves for the piece
         """
        for move in legal_moves:
            for i in range(self.grid_layout.count()):
                cell = self.grid_layout.itemAt(i)
                widget = cell.widget()
                row = i // 8
                col = i % 8

                if (7 - row, col) == move:
                    #widget.setStyleSheet(("background-color: #F0D9B5;" if (col + row) % 2 == 0 else "background-color: #B58863;") + "background-image: radial-gradient(10px circle at 10px 10px, rgb(0, 255, 0) 50%, transparent 50.2%); background-size: 20px 20px; background-position: center; background-repeat: no-repeat;")
                    widget.setStyleSheet("background-color:" + ("#F0D9B5" if (col + row) % 2 == 0 else "#B58863") + "; background-image: url(Chess/Resources/circle.png); background-position: center; background-repeat: no-repeat; background-size: 5px 5px; background-size: contain;")

    def remove_pending_moves(self):
        """ Removes the highlighted squares """
        for row in range(8):
            for col in range(8):
                index = row * 8 + col
                square = self.grid_layout.itemAt(index).widget()
                if square is not None:
                    color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                    square.setStyleSheet(f"background-color: {color};")


if __name__ == "__main__":
    chess_repository = ChessRepository()
    chess_repository.initialize_board()
    gui_state = GameState(chess_repository)
    gui = ChessGUI(gui_state)
