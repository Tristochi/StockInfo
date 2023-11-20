import csv
import json

ticker_dictionary = {}
restricted_chars = ['.', '$', '#', '[',']', '/', '%']
with open('ticker_list.csv', newline='') as theList:
    ticker_reader = csv.reader(theList, delimiter=',')
    for row in ticker_reader:
        #print(' '.join(row[0:2]))
        for char in restricted_chars:
            if char in row[0]:
                row[0] = row[0].replace(char, "")
            if char in row[1]:
                row[1] = row[1].replace(char, "")
            #print(row[1])
        ticker_dictionary[row[0]] = row[1]

#print(ticker_dictionary)
with open("ticker_list.json", "w") as json_file:
    json.dump(ticker_dictionary, json_file, indent = 4)