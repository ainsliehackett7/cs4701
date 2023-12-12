import chess
import time
from board_evaluation_functions import evaluate_board


def minimax_search(board, alpha, beta, depth):
  if board.is_checkmate():
    return -float('inf') if board.turn == chess.WHITE else float('inf')
  if board.is_stalemate() or board.is_insufficient_material():
    return 0
  if depth == 0:
    return evaluate_board(board)
  
  if board.turn == chess.WHITE:
    max_score = -float('inf')
    for move in board.legal_moves:
      board.push(move)
      score = minimax_search(board, alpha, beta, depth - 1)
      max_score = max(max_score, score)
      board.pop()
      alpha = max(alpha, score)
      if beta <= alpha:
        break
    return max_score
  else:
    min_score = float('inf')
    for move in board.legal_moves:
      board.push(move)
      score = minimax_search(board, alpha, beta, depth - 1)
      min_score = min(min_score, score)
      board.pop()
      beta = min(beta, score)
      if beta <= alpha:
        break
    return min_score

def find_best_move(board, max_depth=4, time_limit=None):
  best_move = None
  start_time = time.time()

  for depth in range(1, max_depth + 1):
    best_eval = -float('inf') if board.turn == chess.WHITE else float('inf')
    for move in board.legal_moves:
      board.push(move)
      score = minimax_search(board, -float('inf'), float('inf'), depth - 1)
      board.pop()

      if board.turn == chess.WHITE and score > best_eval:
        best_eval = score
        best_move = move
      elif board.turn == chess.BLACK and score < best_eval:
        best_eval = score
        best_move = move

    # If time limit exceeded, return current best move (and break the loop)
    if time_limit is not None and (time.time() - start_time) > time_limit:
      break

  return best_move