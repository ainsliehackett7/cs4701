import gptapi
import csv_analyzer
import csv


def find_puzzle():
    file = "data/lichess_db_puzzle.csv"
    terms = gptapi.promptgpt()
    print(terms)
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
        print(csvreader[current_index][2])
        return csvreader[current_index][1]


print(find_puzzle())
