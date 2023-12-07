import chess
import matplotlib.pyplot as plt
import random
from mcts_module import select_best_move as mcts_move
from minimax_module import find_best_move as minimax_move
from stockfish import Stockfish
from preprocessing import preprocess_puzzles

# Configure the Stockfish engine
stockfish_path = "stockfish/stockfish"
sf = Stockfish(stockfish_path)

# Load and preprocess the puzzle database
raw_puzzles_db = "data/lichess_db_puzzle.csv"
puzzles_db = preprocess_puzzles(raw_puzzles_db) # pandas dataframe with headers: df[['FEN', 'Moves', 'Rating', 'Themes']] and with example row: {'FEN': 'r1bq1rk1/ppp2ppp/2n1pn2/3p4/2PP4/2NBPN2/PP3PPP/R1BQ1RK1 w - - 0 1', 'Moves': 'e2e4 d7d5 b1c3 g8f6 g1f3 e7e6 f1d3 f8e7 e1g1 e8g8 d2d4 c7c5', 'Rating': 1600, 'Themes': 'Discovered attack, Hanging piece, Pin, Skewer, X-ray attack'}

def get_database():
  return puzzles_db

def get_max_time_for_puzzle(elo_rating):
  if elo_rating < 1500:
    return 2  # Less time for easier puzzles
  elif elo_rating > 2000:
    return 5  # More time for harder puzzles
  return 3  # Default time

def run_evaluation_and_plot():
  # Select a random subset of puzzles (e.g., 100 puzzles)
  num_puzzles_to_evaluate = 100
  selected_puzzles = random.sample(puzzles_db, num_puzzles_to_evaluate)

  # Evaluate each AI on the selected subset of puzzles
  mcts_results = evaluate_ai(selected_puzzles, "mcts")
  minimax_results = evaluate_ai(selected_puzzles, "minimax")
  stockfish_results = evaluate_ai(selected_puzzles, "stockfish")

  # Plot the results
  plot_results(mcts_results, "MCTS AI")
  plot_results(minimax_results, "Minimax AI")
  plot_results(stockfish_results, "Stockfish AI")
  plt.xlabel("Puzzle ELO")
  plt.ylabel("Success Rate")
  plt.legend()
  plt.show()

def test_ai_on_puzzle(ai_type, puzzle_fen, expected_move, max_time):
  board = chess.Board(puzzle_fen)

  # Apply the opponent's first move (assuming it's always correct)
  opponent_move = chess.Move.from_uci(expected_move.split()[0])
  if opponent_move in board.legal_moves:
    board.push(opponent_move)
  else:
    print(f"Invalid move in puzzle: {opponent_move}")
    return False

  # Now let the AI make its move
  if ai_type == "mcts":
    ai_move = mcts_move(board, max_time)
  elif ai_type == "minimax":
    ai_move = minimax_move(board, max_time)
  elif ai_type == "stockfish":
    sf.set_fen_position(board.fen())
    sf.set_depth(max_time)
    ai_move = chess.Move.from_uci(sf.get_best_move())
  else:
    raise ValueError("Unknown AI type")

  # Check if AI's move matches the expected solution move
  return str(ai_move) == expected_move.split()[1]  # Compare to the second move in the solution

def evaluate_ai(puzzles_db, ai_type):
  results = {"puzzle_rating": [], "success": []}
  for puzzle in puzzles_db:
    max_time_for_ai = get_max_time_for_puzzle(puzzle["Rating"])  # Use "Rating" instead of "elo"
    success = test_ai_on_puzzle(ai_type, puzzle["FEN"], puzzle["Moves"].split()[1], max_time_for_ai)  # Assuming second move is the solution
    results["puzzle_rating"].append(puzzle["Rating"])
    results["success"].append(success)
  return results


# Plotting the results
def plot_results(results, label):
  plt.scatter(results["puzzle_rating"], results["success"], label=label)