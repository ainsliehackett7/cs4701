import pandas as pd

def preprocess_puzzles(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Extract relevant columns
    df = df[['FEN', 'Moves', 'Rating', 'Themes']]

    # Convert 'Rating' to integer
    df['Rating'] = df['Rating'].astype(int)

    # Optional: Process 'Moves' column (e.g., extract the first move)
    df['Solution'] = df['Moves'].apply(lambda x: x.split()[0])

    # Convert to a list of dictionaries
    puzzles_db = df.to_dict('records')
    return puzzles_db
