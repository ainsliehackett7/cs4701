import csv

def terms_list(file_path):
    unique_terms = []
    unique_openings = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for row in csvreader:
            if len(row) > 6:
                words_in_column = row[7].split(" ")
                for word in words_in_column:
                    if word not in unique_terms:
                        unique_terms.append(word)

                words_in_column2 = row[9].split(" ")
                for word in words_in_column2:
                    if word not in unique_openings:
                        unique_openings.append(word)

    return [unique_terms, unique_openings]
# file = "data/lichess_db_puzzle.csv"
# info = terms_list(file)
# print("Terms/Themes: ")
# print(len(info[0]))
# print("Opening Tags: ")
# print(len(info[1]))
