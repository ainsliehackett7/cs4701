import chess
import chess.svg
import time
from board import ChessBoard  # Import the ChessBoard class

# Import AI functions
from mcts_module import select_best_move as mcts_move
from minimax_module import find_best_move as minimax_move
from stockfish import Stockfish
import time

import gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import tkinter

# Configure the Stockfish engine
sf = Stockfish("stockfish/stockfish")


def getStockfish(board, max_time):

    sf.set_fen_position(board)
    sf.set_depth(max_time)
    time.sleep(1)
    return chess.Move.from_uci(sf.get_best_move())


def handleAIMove():
    if gameWindow.isUserTurn():
        print("Waiting for AI move...")
        m = getStockfish(gameWindow.getCurrentFEN(), 5).uci()
        gameWindow.makeMove(m)
        print("AI move:", m)
        # Delay before the next puzzle move
        QTimer.singleShot(500, makeNextPuzzleMove)


def makeNextPuzzleMove():
    QTimer.singleShot(500, handleAIMove)


if __name__ == "__main__":
    app = QApplication([])
    fen = "8/1r4pp/8/5kP1/1p3P2/5K2/2R3P1/8 b - - 5 45"
    moves = ['b4b3', 'c2c6', 'h7h5', 'g5h6', 'b3b2', 'g2g4']

    gameWindow = gui.ChessGameWindow(fen, moves, show_user_input=False)
    gameWindow.show()

    # Start with the first puzzle move
    QTimer.singleShot(1000, handleAIMove)

    app.exec()


# if __name__ == "__main__":
#     app = QApplication([])
#     fen = "8/1r4pp/8/5kP1/1p3P2/5K2/2R3P1/8 b - - 5 45"
#     moves = ['b4b3', 'c2c6', 'h7h5', 'g5h6', 'b3b2', 'g2g4']

#     gameWindow = gui.ChessGameWindow(fen, moves)
#     gameWindow.show()

#     for move in moves:
#         QApplication.processEvents()  # Process existing events
#         if gameWindow.isUserTurn():
#             # Here you can wait for user input or handle it however you wish
#             print("Waiting for AI move...")
#             m = getStockfish(gameWindow.getCurrentFEN(), 5).uci()
#             time.sleep(2)
#             print(m)
#             gameWindow.makeMove(m)
#         else:
#             gameWindow.makeMove(move)
#             print("Automatic move:", move)
#             print("Current FEN:", gameWindow.getCurrentFEN())
#     app.exec()
