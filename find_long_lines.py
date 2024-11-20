from sys import argv

with open(argv[1]) as infile:
    for i, line in enumerate(infile):
        if len(line) > 2000:
            print(i, len(line))
