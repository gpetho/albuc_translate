# run with python3.10 or above

import sys

chapters = []

with open("hunalign_batch.txt") as f:
    for line in f:
        chapters.append(line.strip().split()[0].removeprefix("eng/"))

with (open(f"combined_aligned_{sys.argv[1]}.txt", "w") as combined_f,
      open(f"combined_path_{sys.argv[1]}.txt", "w") as combined_path):
    for chapter in chapters:
        with open(f"sentalign_input/output_{sys.argv[1]}/{chapter}.aligned") as aligned_f:
            print(chapter, file=combined_f)
            for line in aligned_f:
                combined_f.write(line)
            print(file=combined_f)
        with open(f"sentalign_input/output_{sys.argv[1]}/{chapter}.path") as path_f:
            print(chapter, file=combined_path)
            for line in path_f:
                combined_path.write(line)
            print(file=combined_path)
