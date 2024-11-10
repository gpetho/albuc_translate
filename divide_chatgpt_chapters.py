import os
import sys

with open("hunalign_batch.txt") as order_file:
    chapter_order = order_file.readlines()
    chapter_order = [line.strip().split()[0].removeprefix('eng/')
                    for line in chapter_order]
    print(chapter_order)
    chapter_order = [ch for ch in chapter_order if ch in os.listdir(sys.argv[1])]

with open(sys.argv[2]) as chatgpt_all:
    chatgpt_all_text = chatgpt_all.readlines()

with open(f"{sys.argv[1]}/all_text.txt") as all_text_file:
    all_text = all_text_file.readlines()

assert len(all_text) == len(chatgpt_all_text)

os.makedirs(f"sentalign_input/{sys.argv[1]}", exist_ok=True)

starting_line = 0
for chapter in chapter_order:
    with open(f"{sys.argv[1]}/{chapter}") as occ_lines:
        chapter_lines = occ_lines.readlines()
        num_chapter_lines = len(chapter_lines)

    with open(f"sentalign_input/{sys.argv[1]}/{chapter}", "w") as chatgpt_chapter:
        for line in chatgpt_all_text[starting_line:
                                     starting_line + num_chapter_lines]:
            line_cols = line.split("\t")
            assert len(line_cols) == 2
            chatgpt_chapter.write(line_cols[1])

    starting_line += num_chapter_lines
