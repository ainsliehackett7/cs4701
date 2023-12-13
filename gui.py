from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from stockfish import Stockfish
from minimax_module import find_best_move as minimax_move
from mcts_module import select_best_move as mcts_move
from board import ChessBoard  # Import the ChessBoard class
import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QByteArray, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QMessageBox, QPushButton
from test import getStockfish


class ChessGameWindow(QWidget):
    def __init__(self, fen=None, puzzle_moves=None, show_user_input=True):
        super().__init__()
        self.setGeometry(100, 100, 520, 620)

        self.svgDisplayWidget = QSvgWidget(parent=self)
        self.svgDisplayWidget.setGeometry(10, 10, 500, 500)

        self.gameBoard = chess.Board(fen) if fen else chess.Board()
        self.currentPuzzleIndex = 0  # Initialize currentPuzzleIndex here
        self.lastMove = None
        self.puzzleMoves = puzzle_moves
        # List to store board states as SVGs
        self.boardStates = []
        self.currentStateIndex = 0

        self.show_user_input = show_user_input

        self.setupLayout()

        # If it's a puzzle and the first move is automatic, make it
        if self.puzzleMoves:
            self.makePuzzleMove()
        self.refreshBoard()

    def setupLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.svgDisplayWidget)

        # Navigation buttons
        self.prevButton = QPushButton("Previous", self)
        self.prevButton.clicked.connect(self.showPreviousState)
        layout.addWidget(self.prevButton)

        self.nextButton = QPushButton("Next", self)
        self.nextButton.clicked.connect(self.showNextState)
        layout.addWidget(self.nextButton)

        self.moveEntry = QLineEdit(self)
        self.moveEntry.setPlaceholderText("Enter your move (e.g., e2e4)")
        self.moveEntry.returnPressed.connect(self.processMove)
        layout.addWidget(self.moveEntry)

        # Set visibility of moveEntry based on the flag
        self.moveEntry.setVisible(self.show_user_input)

    def processMove(self):
        move_uci = self.moveEntry.text()
        self.makeMove(move_uci)
        self.moveEntry.clear()

    def getCurrentFEN(self):
        return self.gameBoard.fen()

    def checkPuzzleCompletion(self):
        if self.currentPuzzleIndex >= len(self.puzzleMoves):
            QMessageBox.information(
                self, "Puzzle Completed", "Congratulations! You have completed the puzzle.")
            return True
        return False

    def makeMove(self, move_uci):
        if not self.gameBoard.is_checkmate():
            try:
                move = chess.Move.from_uci(move_uci)
                if self.gameBoard.is_legal(move):
                    if not self.puzzleMoves or self.isUserTurn():
                        if not self.puzzleMoves or move_uci == self.puzzleMoves[self.currentPuzzleIndex]:
                            self.gameBoard.push(move)
                            self.lastMove = move
                            self.currentPuzzleIndex += 1
                            self.refreshBoard()

                            if self.puzzleMoves:
                                self.makePuzzleMove()
                        else:
                            QMessageBox.warning(
                                self, "Incorrect Move", "This move is not correct for the puzzle. Skipping this move.")
                            move = self.puzzleMoves[self.currentPuzzleIndex]
                            self.gameBoard.push(move)
                            self.lastMove = move
                            self.currentPuzzleIndex += 1
                            self.refreshBoard()

                            if self.puzzleMoves:
                                self.makePuzzleMove()

                    else:
                        QMessageBox.warning(
                            self, "Not Your Turn", "It's not your turn to move.")
                else:
                    QMessageBox.warning(self, "Illegal Move",
                                        "The move you entered is not legal.")
            except ValueError:
                QMessageBox.warning(
                    self, "Invalid Move", "Invalid move format. Please enter moves in UCI format (e.g., e2e4).")

    def isUserTurn(self):
        if self.gameBoard.is_checkmate():
            return False
        return not self.puzzleMoves or self.currentPuzzleIndex % 2 == 1

    def makePuzzleMove(self):
        while self.puzzleMoves and self.currentPuzzleIndex < len(self.puzzleMoves) and not self.isUserTurn():
            move = chess.Move.from_uci(
                self.puzzleMoves[self.currentPuzzleIndex])
            self.gameBoard.push(move)
            self.lastMove = move
            self.currentPuzzleIndex += 1
            self.refreshBoard()

    def refreshBoard(self):
        # Check for checkmate first
        if self.gameBoard.is_checkmate():
            # If checkmate, store the board state without flipping
            self.storeCurrentBoardState()
            self.updateBoardDisplay()
            QMessageBox.information(
                self, "Checkmate", "Checkmate! The game is over.")
            return

        # Set flipping based on whose turn it is
        self.isFlipped = self.gameBoard.turn == chess.BLACK
        in_check = self.gameBoard.king(self.gameBoard.turn)

        # Generate the SVG representation of the board
        if self.gameBoard.is_check():
            self.gameBoardSvg = chess.svg.board(
                self.gameBoard, check=in_check, lastmove=self.lastMove, flipped=self.isFlipped).encode("UTF-8")
        else:
            self.gameBoardSvg = chess.svg.board(
                self.gameBoard, lastmove=self.lastMove, flipped=self.isFlipped).encode("UTF-8")

        # Load the SVG into the widget and clear the move entry
        self.svgDisplayWidget.load(self.gameBoardSvg)
        self.moveEntry.clear()

        # Store the current board state
        self.storeCurrentBoardState()

    def storeCurrentBoardState(self):
        svg = chess.svg.board(
            self.gameBoard, lastmove=self.lastMove, flipped=False)
        svg2 = chess.svg.board(
            self.gameBoard, lastmove=self.lastMove, flipped=True)
        self.boardStates.append((svg, svg2))
        self.currentStateIndex = len(self.boardStates) - 1

    def showPreviousState(self):
        if self.currentStateIndex > 0:
            self.currentStateIndex -= 1
            self.updateBoardDisplay()

    def showNextState(self):
        if self.currentStateIndex < len(self.boardStates) - 1:
            self.currentStateIndex += 1
            self.updateBoardDisplay()

    def updateBoardDisplay(self):
        b = 0
        if self.isFlipped:
            b = 1
        svg = self.boardStates[self.currentStateIndex][b]
        self.svgDisplayWidget.load(QByteArray(svg.encode('utf-8')))


# Import AI functions

# Configure the Stockfish engine
# sf = Stockfish("stockfish/stockfish")


# def getStockfish(board, max_time):

#     sf.set_fen_position(board)
#     sf.set_depth(max_time)
#     time.sleep(1)
#     return chess.Move.from_uci(sf.get_best_move())


# def handleAIMove():
#     if gameWindow.isUserTurn():
#         print("Waiting for AI move...")
#         m = getStockfish(gameWindow.getCurrentFEN(), 5).uci()
#         gameWindow.makeMove(m)
#         print("AI move:", m)
#         # Delay before the next puzzle move
#         QTimer.singleShot(500, makeNextPuzzleMove)


# def makeNextPuzzleMove():
#     QTimer.singleShot(500, handleAIMove)


# # if __name__ == "__main__":
# #     app = QApplication([])
# #     fen = "8/1r4pp/8/5kP1/1p3P2/5K2/2R3P1/8 b - - 5 45"
# #     moves = ['b4b3', 'c2c6', 'h7h5', 'g5h6', 'b3b2', 'g2g4']

# #     gameWindow = gui.ChessGameWindow(fen, moves, show_user_input=False)
# #     gameWindow.show()

# #     # Start with the first puzzle move
# #     QTimer.singleShot(1000, handleAIMove)

# #     app.exec()
