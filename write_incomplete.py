import replace_incomplete

with open('incomplete.txt', 'w') as f:
    for line in replace_incomplete.retranslate_lines.values():
        print(line, file=f)
