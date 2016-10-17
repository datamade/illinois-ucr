import csv
import sys

naughty_chars = ['-1', ' ', '_Not a Census place', '888888888', '888']

# read csv from stdin
reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

# replace characters with None
for row in reader:
    cleanrow = []
    for col in row: 
        if col in naughty_chars:
            col = None
        cleanrow.append(col) 
    writer.writerow(cleanrow)

