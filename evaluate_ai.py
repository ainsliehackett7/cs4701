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
    return 10  # Less time for easier puzzles
  elif elo_rating > 2000:
    return 15  # More time for harder puzzles
  return 10  # Default time

def run_evaluation_and_plot(num_puzzles_to_evaluate=30):
    selected_puzzles = random.sample(puzzles_db, num_puzzles_to_evaluate)

    # Evaluate and plot success rates across rating classes
    plot_success_rate_comparisons(selected_puzzles)

    # Evaluate and plot Minimax performance at different depths
    depth_range = range(2, 7) # {2,3,4,5,6}
    depth_results = evaluate_minimax_at_different_depths(selected_puzzles, depth_range)
    plot_depth_results(depth_results)

def test_ai_on_puzzle(ai_type, puzzle_fen, expected_moves, max_time, max_depth=4):
  board = chess.Board(puzzle_fen)

  # Apply the opponent's first move (assuming it's always correct)
  opponent_move = chess.Move.from_uci(expected_moves.split()[0])
  if opponent_move in board.legal_moves:
    board.push(opponent_move)
  else:
    print(f"Invalid move in puzzle: {opponent_move}")
    return False

  # Now let the AI make its move
  if ai_type == "mcts":
    ai_move = mcts_move(board, max_time)
  elif ai_type == "minimax":
    ai_move = minimax_move(board, max_depth, max_time)
  elif ai_type == "stockfish":
    sf.set_fen_position(board.fen())
    sf.set_depth(max_time)
    ai_move = chess.Move.from_uci(sf.get_best_move())
  else:
    raise ValueError("Unknown AI type")

  # Check if AI's move matches the expected solution move
  return str(ai_move) == expected_moves.split()[1]  # Compare to the second move in the solution

def evaluate_ai(puzzles_db, ai_type, max_depth=4, group_by_rating=False):
  rating_ranges = [(0, 1000), (1001, 1500), (1501, 2000), (2001, float('inf'))]
  results = {range: {"puzzle_rating": [], "success": []} for range in rating_ranges} if group_by_rating else {"puzzle_rating": [], "success": []}

  for puzzle in puzzles_db:
    puzzle_rating = puzzle["Rating"]
    rating_range = categorize_rating(puzzle_rating)
    success = test_ai_on_puzzle(ai_type, puzzle["FEN"], puzzle["Moves"], get_max_time_for_puzzle(puzzle_rating), max_depth)
    results[rating_range]["puzzle_rating"].append(puzzle_rating)
    results[rating_range]["success"].append(success)

  return results

def categorize_rating(puzzle_rating):
  if puzzle_rating <= 1000:  # Ratings up to 1000
    return (0, 1000)
  elif puzzle_rating <= 1500:  # Ratings from 1001 to 1500
    return (1001, 1500)
  elif puzzle_rating <= 2000:  # Ratings from 1501 to 2000
    return (1501, 2000)
  else:  # Ratings above 2000
    return (2001, float('inf'))

def evaluate_minimax_at_different_depths(puzzles_db, depth_range):
    depth_results = {}
    for depth in depth_range:
        results = evaluate_ai(puzzles_db, "minimax", max_depth=depth)
        success_rate = sum(results["success"]) / len(results["success"]) * 100
        depth_results[depth] = success_rate
    return depth_results

def plot_depth_results(depth_results):
    plt.figure(figsize=(10, 6))
    plt.plot(list(depth_results.keys()), list(depth_results.values()), marker='o', linestyle='-')
    plt.xlabel("Max Depth")
    plt.ylabel("Success Rate (%)")
    plt.title("Minimax AI Performance at Different Depths")
    plt.grid(True)
    plt.show()

def plot_success_rate_comparisons(selected_puzzles):
    ai_types = ["stockfish", "minimax", "mcts"]  # Add "mcts" if needed
    rating_ranges = [(0, 1000), (1001, 1500), (1501, 2000), (2001, float('inf'))]

    for ai_type in ai_types:
        print(f"Running {ai_type} AI...")
        success_rates = []
        results_by_rating = evaluate_ai(selected_puzzles, ai_type, group_by_rating=True)
        for puzzle_rating in range(len(rating_ranges)):
            rating_range = rating_ranges[puzzle_rating]

            # Calculate the success rate for each rating range
            if rating_range in results_by_rating:
                success_rate = sum(results_by_rating[rating_range]["success"]) / len(results_by_rating[rating_range]["success"]) * 100 if results_by_rating[rating_range]["success"] else 0
            else:
                success_rate = 0
            success_rates.append(success_rate)

        rating_labels = [f"{r[0]}-{int(r[1]) if r[1] != float('inf') else 'inf'}" for r in rating_ranges]
        plt.plot(rating_labels, success_rates, label=f"{ai_type} AI")

    plt.xlabel("Puzzle Rating Range")
    plt.ylabel("Success Rate (%)")
    plt.legend()
    plt.show()

def evaluate_minimax_at_different_depths(puzzles_db, depth_range):
    depth_results = {}
    for depth in depth_range:
        print(f'minimax @ depth {depth}')
        results = evaluate_ai(puzzles_db, "minimax", max_depth=depth, group_by_rating=False)
        success_rate = sum(results["success"]) / len(results["success"]) * 100
        depth_results[depth] = success_rate
    return depth_results

