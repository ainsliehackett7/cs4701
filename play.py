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

# Configure the Stockfish engine
sf = Stockfish("stockfish/stockfish")


def prompt_move(board, expected_move_str):
    next_move_str = input(
        'Type your move UCI (or return empty string to automate):')
    if next_move_str == '':
        return chess.Move.from_uci(expected_move_str)
    next_move = chess.Move.from_uci(next_move_str)
    if next_move not in board.legal_moves:
        print('Illegal move! Try again.')
        return prompt_move(board, expected_move_str)
    if next_move_str != expected_move_str:
        print("wrong move! Try again.")
        return prompt_move(board, expected_move_str)
    return next_move


def play_ai_game(board, moves, ai_type, max_time):
    print(board)

    uci_move = chess.Move.from_uci(moves[0])
    board.push(uci_move)

    print()
    print('Opponent\'s move: ' + moves[0])
    print(board)

    # Game loop
    move_index = 1
    total_move_time = 0
    while not board.is_checkmate() and move_index < len(moves):
        start_time = time.time()  # Start timing

        best_move = None
        if ai_type == "mcts":
            best_move = mcts_move(board, max_time)
        elif ai_type == "minimax":
            # Assume max_depth correlates with max_time
            best_move = minimax_move(board, 4, max_time)
        elif ai_type == "stockfish":
            sf.set_fen_position(board.fen())
            sf.set_depth(max_time)  # Set Stockfish depth
            best_move = chess.Move.from_uci(sf.get_best_move())
        else:
            raise ValueError("Unknown AI type")

        move_time = time.time() - start_time  # Calculate move time
        total_move_time += move_time  # Add move time to total

        if not best_move or best_move not in board.legal_moves:
            print(
                f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
            print("AI cannot move?")
            print(board)
            # Calculate and print the average time per move
            avg_move_time = total_move_time / move_index if move_index > 0 else 0
            print(
                f'AI FAILED, error?? Average time per move: {avg_move_time:.2f} seconds')
            break

        board.push(best_move)
        print(f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
        print(board)

        uci_move = chess.Move.from_uci(moves[0])
        board.push(uci_move)

        print()
        print('Opponent\'s move: ' + moves[0])
        print(board.unicode())

        # Game loop
        move_index = 1
        total_move_time = 0
        while not board.is_checkmate() and move_index < len(moves):
            start_time = time.time()  # Start timing

            best_move = None
            if ai_type == "mcts":
                best_move = mcts_move(board, max_time)
            elif ai_type == "minimax":
                # Assume max_depth correlates with max_time
                best_move = minimax_move(board, 4, max_time)
            elif ai_type == "stockfish":
                sf.set_fen_position(board.fen())
                sf.set_depth(max_time)  # Set Stockfish depth
                best_move = chess.Move.from_uci(sf.get_best_move())

            else:
                raise ValueError("Unknown AI type")

            move_time = time.time() - start_time  # Calculate move time
            total_move_time += move_time  # Add move time to total

            if not best_move or best_move not in board.legal_moves:
                print(
                    f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
                print("AI cannot move?")
                print(board.unicode())
                # Calculate and print the average time per move
                avg_move_time = total_move_time / move_index if move_index > 0 else 0
                print(
                    f'AI FAILED, error?? Average time per move: {avg_move_time:.2f} seconds')
                break

            board.push(best_move)
            print(
                f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
            print(board.unicode())

            # Check if correct move was made
            if (moves[move_index] != str(best_move)):
                # Calculate and print the average time per move
                avg_move_time = total_move_time / move_index if move_index > 0 else 0
                print(
                    f'AI Lost. Average time per move: {avg_move_time:.2f} seconds')
                return

            move_index += 1

        print('AI wins!')
        # Calculate and print the average time per move
        avg_move_time = total_move_time / move_index if move_index > 0 else 0
        print(f'AI wins! Average time per move: {avg_move_time:.2f} seconds')


def play_human_game(board, moves):

    while not board.is_checkmate() and move_index < len(moves):
        board.push(prompt_move(board, moves[move_index]))
        print()
        print('Your move: ' + moves[move_index])
        print(board)

        print()
        print('Opponent\'s move: ' + moves[move_index])
        print(board)

        move_index = 1

        while not board.is_checkmate() and move_index < len(moves):
            board.push(prompt_move(board, moves[move_index]))
            print()
            print('Your move: ' + moves[move_index])
            print(board.unicode())

            move_index += 1
            if (move_index >= len(moves)):
                break

            time.sleep(0.2)
            board.push(chess.Move.from_uci(moves[move_index]))
            print()
            print('Opponent\'s move: ' + moves[move_index])
            print(board.unicode())

            move_index += 1

        print('Great job!')


def getStockfish(board, max_time):

    sf.set_fen_position(board)
    sf.set_depth(max_time)
    time.sleep(1)
    return chess.Move.from_uci(sf.get_best_move())


def play_ai_gameGUI(board, moves, ai_type, max_time):

    def handleAIMove(gameWindow):
        if gameWindow.isUserTurn():
            print("Waiting for AI move...")
            m = getStockfish(gameWindow.getCurrentFEN(), 5).uci()
            gameWindow.makeMove(m)
            print("AI move:", m)
            # Delay before the next puzzle move
            QTimer.singleShot(500, makeNextPuzzleMove)

    def makeNextPuzzleMove(gameWindow):
        QTimer.singleShot(500, handleAIMove(gameWindow))

        if __name__ == "__main__":
            app = QApplication([])

            gameWindow = gui.ChessGameWindow(
                board.fen(), moves, show_user_input=False)
            gameWindow.show()

            # Start with the first puzzle move
            QTimer.singleShot(1000, handleAIMove(gameWindow))

            app.exec()
            uci_move = chess.Move.from_uci(moves[0])
            board.push(uci_move)

    move_index = 1
    total_move_time = 0
    while not board.is_checkmate() and move_index < len(moves):
        start_time = time.time()  # Start timing

        best_move = None
        if ai_type == "mcts":
            best_move = mcts_move(board, max_time)
        elif ai_type == "minimax":
            # Assume max_depth correlates with max_time
            best_move = minimax_move(board, 4, max_time)
        elif ai_type == "stockfish":
            sf.set_fen_position(board.fen())
            sf.set_depth(max_time)  # Set Stockfish depth
            best_move = chess.Move.from_uci(sf.get_best_move())

        else:
            raise ValueError("Unknown AI type")

        move_time = time.time() - start_time  # Calculate move time
        total_move_time += move_time  # Add move time to total

        if not best_move or best_move not in board.legal_moves:
            print(
                f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
            print("AI cannot move?")
            print(board.unicode())
            # Calculate and print the average time per move
            avg_move_time = total_move_time / move_index if move_index > 0 else 0
            print(
                f'AI FAILED, error?? Average time per move: {avg_move_time:.2f} seconds')
            break

        board.push(best_move)
        print(f"AI's move: {best_move}, Time taken: {move_time:.2f} seconds")
        print(board.unicode())

        # Check if correct move was made
        if (moves[move_index] != str(best_move)):
            # Calculate and print the average time per move
            avg_move_time = total_move_time / move_index if move_index > 0 else 0
            print(
                f'AI Lost. Average time per move: {avg_move_time:.2f} seconds')
            return

        move_index += 1

    print('AI wins!')
    # Calculate and print the average time per move
    avg_move_time = total_move_time / move_index if move_index > 0 else 0
    print(f'AI wins! Average time per move: {avg_move_time:.2f} seconds')
