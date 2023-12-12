import gptapi
import csv
from play import create_game, play_ai_game
import evaluate_ai  # Import your AI evaluation module
import random


def main():
    print("1. Play Puzzle")
    print("2. Watch AI Play")
    print("3. Evaluate AI Performance")
    choice = input("Enter your choice: ")

    if choice == '1':
        find_puzzle()  # Get a puzzle
    elif choice == '2':
        print()
        print("1. Random Puzzle")
        print("2. Text-Based Puzzle")
        choice2 = input("Enter your choice: ")
        if choice2 == '1':
            puzzle_fen, puzzle_moves = find_puzzle_ai()
        elif choice2 == '2':
            puzzle_fen, puzzle_moves = find_puzzle_ai(True)  # Get a puzzle
        else:
            print("Invalid Choice, doing random puzzle")
            puzzle_fen, puzzle_moves = find_puzzle_ai()
        ai_type = input("Choose AI type (mcts/minimax/stockfish): ")
        create_game(puzzle_fen, puzzle_moves, play_mode="ai", ai_type=ai_type)

    elif choice == '3':
        # AI Evaluation and Graph Generation
        # Assuming such a function exists in evaluate_ai.py
        evaluate_ai.run_evaluation_and_plot()


def find_puzzle_ai(is_text=False):
    puzzles = evaluate_ai.get_database()
    if is_text:
        terms = gptapi.promptgpt()
        puzzle = query(puzzles, terms)
    else:
        puzzle = random.choice(puzzles)
    moves = puzzle["Moves"].split()
    fen = puzzle["FEN"]
    return fen, moves


def query(puzzles, terms):
    weighted_puzzles = []

    for puzzle in puzzles:
        themes = puzzle["Themes"].split(", ")
        match_count = sum(theme in terms for theme in themes)

        # The more matches, the more times the puzzle is added (increasing its selection probability)
        for _ in range(match_count):
            weighted_puzzles.append(puzzle)

    # Randomly select from the weighted list
    if weighted_puzzles:
        return random.choice(weighted_puzzles)
    else:
        # Return a random puzzle if no matches found
        return random.choice(puzzles)


def find_puzzle():
    file = "data/lichess_db_puzzle.csv"
    terms = gptapi.promptgpt()
    print(terms)

    # df=pd.read_csv(file)
    # preprocess.preprocess(df)

    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        current_max_num = 0
        current_index = 1
        csvreader = list(csvreader)

        for row in range(len(csvreader)):
            acc = 0
            words_in_column = csvreader[row][7].split(" ")
            for word in words_in_column:
                if word in terms:
                    acc += 1
            if acc > current_max_num:
                current_max_num = acc
                current_index = row
        print(csvreader[current_index][7])

        moves = csvreader[current_index][2].split()

        print(moves)

        fen = csvreader[current_index][1]

        print(fen)
        print(moves)

        create_game(fen, moves)

        return 'Puzzle Exited'


main()
