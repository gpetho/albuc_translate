import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

with open(sys.argv[2]) as f:
    lines2 = f.readlines()

for i, (l1, l2) in enumerate(zip(lines, lines2)):
    if l1[:7] != l2[:7]:
        print(i)
        print(l1)
        break