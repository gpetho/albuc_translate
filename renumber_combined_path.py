import sys

line_offsets = {'eng': {}, sys.argv[1]: {}}
chapters = []

with open("hunalign_batch.txt") as f:
    for line in f:
        chapters.append(line.strip().split()[0].removeprefix("eng/"))


for lang in ["eng", sys.argv[1]]:
    with open(f"{lang}/all_text.txt") as all_f:
        target_lines = len(all_f.readlines())
#        print(f"Target {lang}: {target_lines}")
    total_lines = 0
    for chapter in chapters:
        with open(f"{lang}/{chapter}") as f:
            line_offsets[lang][chapter] = total_lines
            f_lines = f.readlines()
            total_lines += len(f_lines)
    assert total_lines == target_lines, f"Total lines mismatch for {lang}: {total_lines} vs {target_lines}"

with (open(f"combined_path_{sys.argv[1]}_manual.txt") as path_f,
      open(f"combined_path_{sys.argv[1]}_all_text.txt", "w") as out_f):
    for line in path_f:
#        print(line)
        if not line[0] == '[':
            current_chapter = line.strip()
            continue
        occ_lines, eng_lines, score = line.strip().split(":")
        occ_lines = occ_lines[1:-1].split(",")
        eng_lines = eng_lines[1:-1].split(",")
        if occ_lines == ['']:
            occ_lines = []
        if eng_lines == ['']:
            eng_lines = []
        score = float(score)
#        print(eng_lines)
        occ_lines = [line_offsets[sys.argv[1]][current_chapter] + int(ol)
                     for ol in occ_lines]
        eng_lines = [line_offsets["eng"][current_chapter] + int(el)
                     for el in eng_lines]
        out_f.write(f"{occ_lines}:{eng_lines}:{score}\n")
