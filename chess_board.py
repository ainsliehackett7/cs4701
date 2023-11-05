import chess
import chess.svg
import time


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


def create_game(fen, moves):
    board = chess.Board(fen)

    print(board.unicode())

    uci_move = chess.Move.from_uci(moves[0])
    board.push(uci_move)

    print()
    print('Opponent\'s move: ' + moves[0])
    print(board.unicode())

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
        print(board)

        move_index += 1

    print('Great job!')
