import os

chapters = [f for f in os.listdir('sentalign_input/deu')]

print(chapters)

all_lines = 0

for chapter in chapters:
    with open(f"sentalign_input/deu/{chapter}") as f:
        lines = f.readlines()
        all_lines += len(lines)

print(all_lines)