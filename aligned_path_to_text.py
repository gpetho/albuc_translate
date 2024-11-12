from sys import argv, stdin

try:
    column = int(argv[1])
except:
    print("Usage: aligned_path_to_text.py <column> <language>")
    print("Column 1 is the SentAlign target language (should be eng), column 0 is the source language")

output_lines = []

with open(f"combined_path_{argv[2]}_all_text.txt") as path_f:
    for line in path_f:
        columns = line.strip().split(":")
        if columns[0] == '[]' or columns[1] == '[]':
            continue
        output_lines.append([int(l) for l
                             in columns[column][1:-1].split(", ")])

input_lines = [input_line.strip()
               for input_line in stdin.readlines()]

for sublines in output_lines:
    output_slice = input_lines[sublines[0]:(sublines[-1] + 1)]
    print(" ".join(output_slice))
