# cs4701

TLDR:

pip install openai

pip install python-dotenv

pip install stockfish

pip install python-chess

download lichess puzzle database
download stockfish executable and place in same directory as project's main inside a folder called stockfish

DEPENDENCIES
Database
The database we used for our puzzles is the Lichess Chess Puzzle Database, a collection of chess puzzles hosted on the Lichess platform.  It comprises a diverse set of puzzles extracted from games played by users on the platform. Each puzzle is represented by a unique position on the chessboard, along with the corresponding moves leading to a solution. These puzzles vary in difficulty and cover a wide range of tactical themes and strategic motifs. The dataset often includes metadata such as the Forsyth–Edwards Notation (FEN) of the puzzle position, the sequence of moves leading to the solution, the Elo rating of the player who encountered the puzzle during the game, and thematic labels identifying the key aspects of the puzzle. 
We use pandas to preprocess the database in a usable way that specifies certain headers that will be used. Rating, Themes, Moves, and FEN are selected for each row vector. This lets us query the puzzles faster and provide different puzzles from text input for the Watch AI Play a Text-Input Puzzle game setting.
Database must be physically installed in the data/ folder in the same location as the program.
data/lichess_db_puzzle.csv
	Stockfish must also be physically installed in stockfish/ folder in the same location as main.py:
stockfish/stockfish
	To avoid unnecessary installation confusion, we’ve pushed a stockfish.zip to the repository. Simply unzip it in the same location if you are running a mac and everything should work as intended. If you are not using a mac, you may need to navigate to the Stockfish GitHub12 and download stockfish from there. Make sure it’s in a folder stockfish/ and that the executable (that works with your system) is renamed to stockfish.
Imports
RUNNING Python 3.11
stockfish==3.28.0
python-chess==1.999
chess==1.10.0
openapi==1.1.0
python-dotenv==0.21.0
pandas (any version)
matplotlib (any version)
Startup
After installing proper dependencies and files, navigate to the same directory as main.py. To run, type
python3 main.py
After some time (to process the dataset) you will be prompted by
1. Play Puzzle
2. Watch AI Play
3. Evaluate AI Performance
Enter your choice: 
Simply type 1, 2, or 3 and press enter. Note that 3 is mostly used for evaluation metrics and are graphed below but will take a while to run. It’s likely you’ll prefer 2 or 1. After selecting
You’ll be again prompted to select what puzzle you want to play in an interactive chess window.
	User :
Whenever you see “User : ”, input a chess-puzzle related prompt or you won’t get your puzzle. For example,
	User : I want a mate in 4 with a queen sacrifice
You’ll be asked
	1. Random Puzzle
2. Text-Based Puzzle
Enter your choice: 
Selecting 1 immediately starts the User Interface sequence by randomly selecting a puzzle from the database.
Selecting 2 prompts you again to select which puzzle the ai should play.
User : 
Like in the 1. Play Puzzle sequence.
Then the User Interface should initiate.

