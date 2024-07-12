chapters = []

with open("hunalign_batch.txt") as f:
    for line in f:
        chapters.append(line.strip().split()[0].removeprefix("eng/"))

with (open("combined_aligned.txt", "w") as combined_f,
      open("combined_path.txt", "w") as combined_path):
    for chapter in chapters:
        with open(f"sentalign_input/output/{chapter}.aligned") as aligned_f:
            print(chapter, file=combined_f)
            for line in aligned_f:
                combined_f.write(line)
            print(file=combined_f)
        with open(f"sentalign_input/output/{chapter}.path") as path_f:
            print(chapter, file=combined_path)
            for line in path_f:
                combined_path.write(line)
            print(file=combined_path)
