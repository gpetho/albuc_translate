import os

with open("hunalign_batch.txt") as order_file:
    chapter_order = order_file.readlines()
    chapter_order = [line.strip().split()[0].removeprefix('eng/')
                    for line in chapter_order]
    print(chapter_order)
    chapter_order = [ch for ch in chapter_order if ch in os.listdir("ofr")]

with open("chatgpt_ofr/converted_all.txt") as chatgpt_all:
    chatgpt_all_text = chatgpt_all.readlines()

starting_line = 0
for chapter in chapter_order:
    with open(f"ofr/{chapter}") as occ_lines:
        chapter_lines = occ_lines.readlines()
        num_chapter_lines = len(chapter_lines)

    with open(f"sentalign_input/fr/{chapter}", "w") as chatgpt_chapter:
        for line in chatgpt_all_text[starting_line:
                                     starting_line + num_chapter_lines]:
            line_cols = line.split("\t")
            assert len(line_cols) == 2
            chatgpt_chapter.write(line_cols[1])

    starting_line += num_chapter_lines
